# -*- coding: utf-8 -*-
"""
FastAPI 主服务 - 命题生成Agent API
"""
from fastapi import FastAPI, HTTPException, Query, UploadFile, File, Form, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, FileResponse, JSONResponse as _JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List
from collections import defaultdict
import json
import re
import base64
import os
import time
import hashlib

from config import DEEPSEEK_API_KEY, DEFAULT_DIFFICULTY
from question_generator import question_generator
from export_service import export_service
from llm_client import llm_client
from structure_renderer import renderer

# ==================== 安全配置 ====================

# 允许的域名（CORS白名单）
ALLOWED_ORIGINS = [
    "https://thioacetone-chemistry.top",
    "https://chem-question-agent-production.up.railway.app",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://localhost:8001",
]

# 速率限制配置
RATE_LIMIT_WINDOW = 60        # 时间窗口（秒）
RATE_LIMIT_MAX_REQUESTS = 30  # 每窗口最大请求数（普通API）
RATE_LIMIT_GENERATE_MAX = 10  # generate接口每窗口最大请求数（资源密集）
RATE_LIMIT_BURST = 5          # 突发允许额外请求数

# 请求体大小限制（字节）
MAX_BODY_SIZE = 2 * 1024 * 1024  # 2MB

# 查找前端 dist 目录
_BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
_FRONTEND_DIST = os.path.normpath(os.path.join(_BACKEND_DIR, "..", "frontend", "dist"))


class UTF8JSONResponse(_JSONResponse):
    """自定义 JSONResponse：强制 UTF-8 编码，防止中文乱码"""
    media_type = "application/json; charset=utf-8"

    def render(self, content) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")


app = FastAPI(
    title="高考有机化学命题Agent",
    description="基于AI的高考有机化学原创命题辅助工具",
    version="1.0.0",
    default_response_class=UTF8JSONResponse,
)

# CORS - 白名单模式
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
)

# 禁用前端静态资源缓存
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request as StarletteRequest

class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: StarletteRequest, call_next):
        response = await call_next(request)
        path = request.url.path
        if any(path.endswith(ext) for ext in ('.js', '.css', '.html')) or path == '/' or path == '':
            response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """速率限制中间件：基于IP的滑动窗口限流"""
    def __init__(self, app):
        super().__init__(app)
        self._requests = defaultdict(list)  # {ip: [timestamps]}

    def _get_client_ip(self, request: StarletteRequest) -> str:
        """获取客户端真实IP（优先取X-Forwarded-For，适配Railway代理）"""
        xff = request.headers.get("X-Forwarded-For")
        if xff:
            return xff.split(",")[0].strip()
        xri = request.headers.get("X-Real-IP")
        if xri:
            return xri.strip()
        client = request.client
        return client.host if client else "unknown"

    async def dispatch(self, request: StarletteRequest, call_next):
        ip = self._get_client_ip(request)
        now = time.time()
        window_start = now - RATE_LIMIT_WINDOW

        # 清理过期记录
        self._requests[ip] = [t for t in self._requests[ip] if t > window_start]

        # generate接口更严格限制
        if request.url.path == "/api/generate":
            max_req = RATE_LIMIT_GENERATE_MAX
        else:
            max_req = RATE_LIMIT_MAX_REQUESTS

        if len(self._requests[ip]) >= max_req + RATE_LIMIT_BURST:
            raise HTTPException(
                status_code=429,
                detail="请求过于频繁，请稍后再试",
                headers={"Retry-After": str(RATE_LIMIT_WINDOW)},
            )

        self._requests[ip].append(now)
        return await call_next(request)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """安全响应头中间件"""
    async def dispatch(self, request: StarletteRequest, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        # Content-Security-Policy：限制资源加载来源
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self'"
        )
        # 移除可能泄露服务器信息的头
        try:
            del response.headers["Server"]
        except (KeyError, TypeError):
            pass
        try:
            del response.headers["X-Powered-By"]
        except (KeyError, TypeError):
            pass
        return response


class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    """请求体大小限制中间件"""
    async def dispatch(self, request: StarletteRequest, call_next):
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_BODY_SIZE:
            raise HTTPException(status_code=413, detail="请求体过大")
        return await call_next(request)


# 添加安全中间件（顺序重要：先大小限制 → 速率限制 → 安全头 → 缓存控制）
app.add_middleware(BodySizeLimitMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(NoCacheMiddleware)


# ==================== 数据模型 ====================

class ReactionStep(BaseModel):
    step_number: int = Field(..., ge=1, le=20, description="步骤编号")
    reactant: str = Field(..., min_length=1, max_length=200, description="反应物名称或SMILES")
    reagent: str = Field(..., min_length=1, max_length=500, description="试剂与反应条件")
    product: str = Field(..., min_length=1, max_length=200, description="产物名称或SMILES")
    reaction_type: Optional[str] = Field(None, max_length=100, description="反应类型")
    reactant_smiles: Optional[str] = Field(None, max_length=500, description="反应物SMILES（前端自动解析）")
    product_smiles: Optional[str] = Field(None, max_length=500, description="产物SMILES（前端自动解析）")


class RouteInput(BaseModel):
    title: str = Field("", max_length=200, description="路线标题")
    steps: List[ReactionStep] = Field(..., min_length=1, max_length=20, description="反应步骤列表")


class GenerateRequest(BaseModel):
    route: RouteInput = Field(..., description="合成路线数据")
    difficulty: float = Field(DEFAULT_DIFFICULTY, ge=0.3, le=0.8, description="难度系数")


class RefineRequest(BaseModel):
    question_data: dict = Field(..., description="当前命题数据")
    feedback: str = Field(..., min_length=1, max_length=2000, description="教师修改意见")


class PaperExtractRequest(BaseModel):
    paper_text: str = Field(..., min_length=10, max_length=50000, description="论文文本内容")


class ParseTextRequest(BaseModel):
    raw_text: str = Field(..., min_length=10, max_length=50000, description="非结构化文本（论文、实验步骤、手写OCR结果等）")


class ParseImageRequest(BaseModel):
    image_base64: str = Field(..., min_length=1, max_length=10 * 1024 * 1024, description="图片的Base64编码")
    image_type: str = Field("png", max_length=20, description="图片格式（png/jpg/jpeg）")


# ==================== 辅助函数 ====================

def _parse_json_response(response: str) -> dict:
    """从LLM返回中提取JSON（增强版：处理markdown代码块、多JSON对象等）"""
    if not response:
        return {"raw_output": "", "parse_error": True, "steps": []}

    # 策略1：尝试直接解析整个响应
    try:
        return json.loads(response.strip())
    except json.JSONDecodeError:
        pass

    # 策略2：去除markdown代码块标记 ```json ... ``` 或 ``` ... ```
    cleaned = response.strip()
    # 匹配 ```json ... ``` 或 ``` ... ```
    code_block_match = re.search(r'```(?:json)?\s*\n?([\s\S]*?)\n?```', cleaned)
    if code_block_match:
        cleaned = code_block_match.group(1).strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

    # 策略3：查找第一个完整的JSON对象 { ... }
    # 使用栈匹配括号
    start_idx = cleaned.find('{')
    if start_idx >= 0:
        depth = 0
        for i in range(start_idx, len(cleaned)):
            if cleaned[i] == '{':
                depth += 1
            elif cleaned[i] == '}':
                depth -= 1
                if depth == 0:
                    json_str = cleaned[start_idx:i + 1]
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError:
                        break

    # 策略4：正则匹配（回退）
    json_match = re.search(r'\{[\s\S]*\}', cleaned)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    return {"raw_output": response, "parse_error": True, "steps": []}


# ==================== API 路由 ====================

@app.get("/")
def root():
    # 生产模式：如果前端 dist 存在，返回 index.html
    index_path = os.path.join(_FRONTEND_DIST, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "service": "高考有机化学命题Agent",
        "version": "1.0.0",
        "status": "running",
        "api_configured": bool(DEEPSEEK_API_KEY),
    }


@app.get("/api/health")
def health_check():
    api_available = llm_client.is_available
    return {
        "status": "healthy",
        "deepseek_api": "已配置" if api_available else "未配置（请设置 DEEPSEEK_API_KEY 环境变量）",
    }


@app.post("/api/generate")
def generate_question(request: GenerateRequest):
    """
    核心接口：根据合成路线生成完整命题
    """
    if not DEEPSEEK_API_KEY:
        raise HTTPException(
            status_code=400,
            detail="请先配置 DEEPSEEK_API_KEY 环境变量",
        )

    route_data = {
        "title": request.route.title,
        "steps": [step.model_dump() for step in request.route.steps],
    }

    result = question_generator.generate_from_route(route_data, request.difficulty)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    # 验证命题质量（generate_from_route内部已做验证重试，这里做最终检查）
    validation = question_generator.validate_question(result)
    result["validation"] = validation
    
    # 如果仍有未修复的错误，在结果中标注
    if result.get("_validation_issues"):
        result["validation"]["unfixed_issues"] = result["_validation_issues"]

    return result


@app.post("/api/refine")
def refine_question(request: RefineRequest):
    """
    根据教师反馈优化命题
    """
    if not DEEPSEEK_API_KEY:
        raise HTTPException(status_code=400, detail="请先配置 DEEPSEEK_API_KEY 环境变量")

    result = question_generator.refine_question(request.question_data, request.feedback)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@app.post("/api/extract")
def extract_from_paper(request: PaperExtractRequest):
    """
    从论文文本中提取合成路线
    """
    if not DEEPSEEK_API_KEY:
        raise HTTPException(status_code=400, detail="请先配置 DEEPSEEK_API_KEY 环境变量")

    result = question_generator.extract_from_paper(request.paper_text)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return result


@app.post("/api/parse/text")
def parse_route_text(request: ParseTextRequest):
    """
    智能解析：非结构化文本 → 结构化合成路线
    支持：论文摘要、实验步骤、反应式列表、OCR结果等
    """
    if not DEEPSEEK_API_KEY:
        raise HTTPException(status_code=400, detail="请先配置 DEEPSEEK_API_KEY 环境变量")

    if len(request.raw_text.strip()) < 10:
        raise HTTPException(status_code=400, detail="文本内容太短，请提供完整的合成路线描述")

    try:
        raw_response = llm_client.parse_route_text(request.raw_text)
        result = _parse_json_response(raw_response)
        return result
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="服务器内部错误，请稍后重试")


@app.post("/api/parse/image")
async def parse_route_image(request: ParseImageRequest):
    """
    智能识别：合成路线图片 → 多策略OCR提取文字 → LLM解析为结构化合成路线
    支持：论文截图、板书照片、手写路线等
    """
    if not DEEPSEEK_API_KEY:
        raise HTTPException(status_code=400, detail="请先配置 DEEPSEEK_API_KEY 环境变量")

    try:
        image_data = request.image_base64
        if not image_data:
            raise HTTPException(status_code=400, detail="图片数据为空")

        raw_response = llm_client.parse_route_from_image(image_data, request.image_type)
        result = _parse_json_response(raw_response)
        return result
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="服务器内部错误，请稍后重试")


@app.post("/api/parse/image-upload")
async def parse_route_image_upload(file: UploadFile = File(...)):
    """
    上传图片文件 → MolScribe(结构识别) + 豆包(箭头/条件) + DeepSeek(串联)
    """
    if not DEEPSEEK_API_KEY:
        raise HTTPException(status_code=400, detail="请先配置 DEEPSEEK_API_KEY 环境变量")

    try:
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="文件为空")
        if len(content) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="文件大小超过10MB限制")

        filename = file.filename or ""
        if filename.lower().endswith(('.jpg', '.jpeg')):
            image_type = "jpeg"
        elif filename.lower().endswith('.png'):
            image_type = "png"
        elif filename.lower().endswith('.gif'):
            image_type = "gif"
        elif filename.lower().endswith('.webp'):
            image_type = "webp"
        else:
            image_type = "png"

        image_base64 = base64.b64encode(content).decode('utf-8')

        # 使用 v5.0 管线：MolScribe + 豆包 + DeepSeek
        raw_response = llm_client.parse_route_from_image_v5(image_base64, image_type)
        result = _parse_json_response(raw_response)
        return result
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="服务器内部错误，请稍后重试")


@app.post("/api/export/docx")
def export_docx(question_data: dict = Body(...), include_answer: bool = True):
    """
    导出Word文档
    """
    try:
        docx_bytes = export_service.export_to_docx(question_data, include_answer)
        filename = "化学命题_教师版.docx" if include_answer else "化学命题_学生版.docx"
        return Response(
            content=docx_bytes,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception:
        raise HTTPException(status_code=500, detail="服务器内部错误，请稍后重试")


@app.get("/api/knowledge/reactions")
def get_reactions(category: Optional[str] = Query(None, description="按类别筛选")):
    """
    获取高中必会反应清单
    """
    from knowledge_base import HIGH_SCHOOL_REACTIONS
    if category:
        return [r for r in HIGH_SCHOOL_REACTIONS if r["category"] == category]
    return HIGH_SCHOOL_REACTIONS


@app.get("/api/knowledge/templates")
def get_question_templates():
    """
    获取常见设问模板
    """
    from knowledge_base import QUESTION_TEMPLATES
    return QUESTION_TEMPLATES


@app.get("/api/knowledge/reaction-types")
def get_reaction_types():
    """
    获取反应类型分类
    """
    from knowledge_base import REACTION_TYPES
    return REACTION_TYPES


# ==================== 题库 API ====================

@app.get("/api/questions/structure-inference")
def get_structure_inference_questions(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=50, description="每页数量"),
):
    """
    获取结构简式推断题题库
    """
    import json as _json
    import os as _os
    q_path = _os.path.join(_os.path.dirname(__file__), "structure_inference_questions.json")
    if not _os.path.exists(q_path):
        return {"questions": [], "total": 0, "page": page, "page_size": page_size}
    with open(q_path, "r", encoding="utf-8") as f:
        all_questions = _json.load(f)
    total = len(all_questions)
    start = (page - 1) * page_size
    end = start + page_size
    return {
        "questions": all_questions[start:end],
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size,
    }


@app.get("/api/questions/structure-inference/{index}")
def get_structure_inference_question(index: int):
    """
    获取单道结构简式推断题
    """
    import json as _json
    import os as _os
    q_path = _os.path.join(_os.path.dirname(__file__), "structure_inference_questions.json")
    if not _os.path.exists(q_path):
        raise HTTPException(status_code=404, detail="题库文件不存在")
    with open(q_path, "r", encoding="utf-8") as f:
        all_questions = _json.load(f)
    if index < 0 or index >= len(all_questions):
        raise HTTPException(status_code=404, detail="题目序号超出范围")
    return all_questions[index]


# ==================== 结构式渲染 API ====================

class RenderRequest(BaseModel):
    smiles: str = Field(..., min_length=1, max_length=1000, description="SMILES字符串")
    label: str = Field("", max_length=20, description="化合物标签")
    width: int = Field(400, ge=100, le=2000, description="宽度")
    height: int = Field(200, ge=50, le=2000, description="高度")


class RenderMultipleRequest(BaseModel):
    compounds: List[dict] = Field(..., min_length=1, max_length=50, description="化合物列表 [{'smiles': '...', 'label': 'A'}, ...]")
    per_width: int = Field(300, ge=100, le=2000, description="每个结构宽度")
    per_height: int = Field(180, ge=50, le=2000, description="每个结构高度")


class NameToSmilesRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="化合物名称")


class RouteDiagramRequest(BaseModel):
    steps: List[dict] = Field(..., min_length=1, max_length=20, description="合成路线步骤数据")
    title: str = Field("", max_length=200, description="路线标题")
    hidden_structure: Optional[str] = Field(None, description="结构推断题：隐藏指定化合物的结构式，仅显示字母代号")


@app.post("/api/render/svg")
def render_structure_svg(request: RenderRequest):
    """
    SMILES → SVG 结构式
    """
    svg = renderer.render_svg(
        request.smiles, request.width, request.height, label=request.label
    )
    return Response(content=svg, media_type="image/svg+xml")


@app.post("/api/render/png")
def render_structure_png(request: RenderRequest):
    """
    SMILES → PNG base64 结构式
    """
    b64 = renderer.render_png_base64(
        request.smiles, request.width, request.height, label=request.label
    )
    return {"image": b64}


@app.post("/api/render/multiple")
def render_multiple_structures(request: RenderMultipleRequest):
    """
    批量渲染多个化合物结构式
    """
    svg = renderer.render_multiple_svg(
        request.compounds, request.per_width, request.per_height
    )
    return Response(content=svg, media_type="image/svg+xml")


@app.post("/api/render/name-to-smiles")
def name_to_smiles(request: NameToSmilesRequest):
    """
    化合物名称 → SMILES（内置词典 → PubChem → LLM 三级回退）
    """
    # 先检查内置词典
    name = request.name
    source = "unknown"
    if name in renderer.BUILTIN_NAMES:
        smiles = renderer.BUILTIN_NAMES[name]
        source = "builtin"
    elif name in renderer._cache:
        smiles = renderer._cache[name]
        source = "cache"
    else:
        smiles = renderer.name_to_smiles(name)
        if smiles:
            # 判断来源
            if name in renderer.BUILTIN_NAMES:
                source = "builtin"
            else:
                source = "pubchem"  # 默认，LLM回退也标记为llm

    if smiles:
        return {"name": name, "smiles": smiles, "source": source}
    return {"name": name, "smiles": None, "error": "未找到该化合物，请尝试使用英文名称或SMILES直接输入"}


@app.post("/api/render/batch-name-to-smiles")
def batch_name_to_smiles(names: List[str] = Body(..., description="化合物名称列表")):
    """
    批量解析：多个化合物名称 → SMILES
    一次请求解析所有化合物名称，避免多次网络调用
    """
    results = {}
    for name in names:
        name = name.strip()
        if not name:
            continue
        if name in renderer.BUILTIN_NAMES:
            results[name] = {"smiles": renderer.BUILTIN_NAMES[name], "source": "builtin"}
        elif name in renderer._cache:
            results[name] = {"smiles": renderer._cache[name], "source": "cache"}
        else:
            smiles = renderer.name_to_smiles(name)
            if smiles:
                results[name] = {"smiles": smiles, "source": "pubchem"}
            else:
                results[name] = {"smiles": None, "error": "未找到"}
    return {"results": results}


@app.get("/api/render/search")
def search_compounds(q: str = Query(..., description="搜索关键词"), limit: int = Query(10, ge=1, le=20)):
    """
    搜索化合物（PubChem在线）
    """
    results = renderer.search_compounds(q, limit)
    return {"keyword": q, "results": results}


@app.post("/api/render/route-diagram")
def render_route_diagram(request: RouteDiagramRequest):
    """
    渲染合成路线流程图 SVG（仿高考真题格式）
    格式：结构A → 结构B → 结构C → ...
    每个箭头上方标注试剂/条件，结构下方标注化合物编号
    """
    steps = request.steps
    if not steps:
        raise HTTPException(status_code=400, detail="路线步骤为空")

    # 构建路线图步骤数据：将名称转换为SMILES
    diagram_steps = []
    for i, step in enumerate(steps):
        # 第一个化合物只需要reactant
        if i == 0:
            reactant_name = step.get("reactant", "")
            reactant_smiles = renderer.name_to_smiles(reactant_name)
            if not reactant_smiles:
                raw = step.get("reactant", "")
                if renderer.smiles_to_mol(raw):
                    reactant_smiles = raw
            diagram_steps.append({
                "smiles": reactant_smiles or "",
                "label": chr(65 + i),  # A, B, C...
                "name": reactant_name,
            })

        # 产物
        product_name = step.get("product", "")
        product_smiles = renderer.name_to_smiles(product_name)
        if not product_smiles:
            raw = step.get("product", "")
            if renderer.smiles_to_mol(raw):
                product_smiles = raw

        reagent = step.get("reagent", "")
        diagram_steps.append({
            "smiles": product_smiles or "",
            "label": chr(65 + i + 1),
            "reagent": reagent,
            "name": product_name,
        })

    if len(diagram_steps) < 2:
        raise HTTPException(status_code=400, detail="至少需要2个化合物才能生成路线图")

    svg = renderer.render_route_diagram_svg(diagram_steps, request.title, request.hidden_structure)
    if not svg:
        raise HTTPException(status_code=500, detail="路线图渲染失败")

    return Response(content=svg, media_type="image/svg+xml")


class InlineSvgRequest(BaseModel):
    name: str = Field(..., description="化合物名称或SMILES字符串")
    width: int = Field(200, description="SVG宽度")
    height: int = Field(120, description="SVG高度")


@app.post("/api/render/enrich-route")
def enrich_route(request: RouteInput):
    """
    将路线中的化合物名称解析为SMILES，用于前端渲染结构式
    返回与原路线相同结构，但每个步骤增加了 reactant_smiles 和 product_smiles 字段
    """
    enriched_steps = []
    for step in request.steps:
        enriched = dict(step)

        # 解析反应物SMILES
        reactant_name = step.reactant
        reactant_smiles = None
        if reactant_name in renderer.BUILTIN_NAMES:
            reactant_smiles = renderer.BUILTIN_NAMES[reactant_name]
        elif reactant_name in renderer._cache:
            reactant_smiles = renderer._cache[reactant_name]
        elif renderer.smiles_to_mol(reactant_name):
            reactant_smiles = reactant_name
        else:
            reactant_smiles = renderer.name_to_smiles(reactant_name)
        enriched["reactant_smiles"] = reactant_smiles or ""

        # 解析产物SMILES
        product_name = step.product
        product_smiles = None
        if product_name in renderer.BUILTIN_NAMES:
            product_smiles = renderer.BUILTIN_NAMES[product_name]
        elif product_name in renderer._cache:
            product_smiles = renderer._cache[product_name]
        elif renderer.smiles_to_mol(product_name):
            product_smiles = product_name
        else:
            product_smiles = renderer.name_to_smiles(product_name)
        enriched["product_smiles"] = product_smiles or ""

        enriched_steps.append(enriched)

    return {
        "title": request.title,
        "steps": enriched_steps,
    }


@app.post("/api/render/inline-svg")
def render_inline_svg(request: InlineSvgRequest):
    """
    渲染内联结构式SVG（用于答案中的结构式展示）
    支持：化合物名称（如"苯酚"、"对硝基苯甲酸"）或SMILES字符串
    以及化合物代号（如"化合物A"）——会从内置映射中查找
    """
    name = request.name.strip()
    smiles = None

    # 处理"化合物X"格式：提取代号
    compound_match = re.match(r'化合物([A-Z])', name)
    if compound_match:
        code = compound_match.group(1)
        name = code  # 尝试用代号查找

    # 多级查找SMILES
    if name in renderer.BUILTIN_NAMES:
        smiles = renderer.BUILTIN_NAMES[name]
    elif name in renderer._cache:
        smiles = renderer._cache[name]
    elif renderer.smiles_to_mol(name):  # 可能是SMILES
        smiles = name
    else:
        smiles = renderer.name_to_smiles(name)

    if not smiles:
        raise HTTPException(status_code=404, detail=f"无法解析化合物: {name}")

    svg = renderer.render_svg(smiles, request.width, request.height, label="")
    return Response(content=svg, media_type="image/svg+xml")


# ==================== 全局异常处理 ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """统一HTTP异常响应格式"""
    return UTF8JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """全局未捕获异常处理器：不泄露内部错误详情"""
    return UTF8JSONResponse(
        status_code=500,
        content={"detail": "服务器内部错误，请稍后重试"},
    )


# ==================== 生产模式：托管前端静态文件 ====================

if os.path.exists(_FRONTEND_DIST):
    # 挂载静态资源（JS/CSS/图片等）
    app.mount("/assets", StaticFiles(directory=os.path.join(_FRONTEND_DIST, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        """
        SPA 回退：所有非 API 路由返回 index.html
        """
        # 跳过 API 路由
        if full_path.startswith("api/"):
            raise HTTPException(status_code=404, detail="Not found")

        index_path = os.path.join(_FRONTEND_DIST, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        raise HTTPException(status_code=404, detail="Frontend not built. Run: cd frontend && npm run build")


if __name__ == "__main__":
    import uvicorn
    import socket
    import threading
    port = int(os.environ.get("PORT", 8000))
    # 尝试绑定端口，如果被占用则尝试下一个端口
    for attempt in range(5):
        test_port = port + attempt
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("0.0.0.0", test_port))
            sock.close()
            port = test_port
            break
        except OSError:
            if attempt == 4:
                print(f"警告：端口 {port}-{port+4} 均被占用，强制使用端口 {port}")
            continue

    print(f"启动服务器于端口 {port}")
    print(f"本地访问: http://localhost:{port}")
    print(f"公网隧道: 请运行 python run_tunnel.py (在项目根目录)")
    uvicorn.run(app, host="0.0.0.0", port=port)