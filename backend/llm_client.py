"""
DeepSeek API 客户端 v4.0 — 命题思维驱动的原创命题引擎
核心理念：理解命题逻辑而非复制格式，形成独特命题风格
"""
import base64
from openai import OpenAI
from config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL
from knowledge_base import (
    HIGH_SCHOOL_REACTIONS, QUESTION_TEMPLATES, SCORING_GUIDELINES,
    TARGET_IDENTITIES, KNOWN_INFO_TEMPLATES, ISOMER_CONDITIONS,
    DIFFICULTY_PROGRESSION, PROMPT_STYLE_KEYWORDS,
)
import json


class LLMClient:
    """DeepSeek LLM 客户端（懒加载）"""

    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            if not DEEPSEEK_API_KEY:
                raise RuntimeError(
                    "未配置 DeepSeek API Key。请设置环境变量 DEEPSEEK_API_KEY。\n"
                    "获取API Key: https://platform.deepseek.com/api_keys"
                )
            self._client = OpenAI(
                api_key=DEEPSEEK_API_KEY,
                base_url=DEEPSEEK_BASE_URL,
            )
        return self._client

    @property
    def is_available(self) -> bool:
        return bool(DEEPSEEK_API_KEY)

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
        """通用生成方法"""
        kwargs = {
            "model": DEEPSEEK_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": 16384,
            "timeout": 180,
        }
        # deepseek-reasoner 不支持 temperature 参数
        if "reasoner" not in DEEPSEEK_MODEL:
            kwargs["temperature"] = temperature
        
        response = self.client.chat.completions.create(**kwargs)
        return response.choices[0].message.content

    # ================================================================
    # 核心：命题思维驱动的原创命题生成 v4.0
    # 不再仿照任何具体试卷，而是理解命题逻辑后自主创作
    # ================================================================

    def generate_question(self, route_info: str, difficulty: float = 0.55) -> str:
        """
        基于合成路线生成命题 v6.0 — 高质量原创命题
        """
        system = f"""你是高考化学命题专家。请根据给定的合成路线，命制一道有机化学大题（5小题，14或15分）。

=== 🔴 最高优先级：第5题答案必须5-7步！（违反此规则将被拒绝） ===
这是整个命题中最重要的一条规则，绝对不能违反：
- 第(5)题合成路线答案必须恰好5步、6步或7步反应
- 不能少于5步（1-4步的答案会被直接拒绝并重新生成）
- 不能多于7步（8步以上的答案也会被拒绝）
- 每步必须有明确的结构式和反应条件
- 答案路线必须与题干路线不同，不能照抄题干路线

=== 🔴 单步路线绝对禁止！（最高警告） ===
如果你生成的第(5)题答案只有1步反应（仅1个箭头），这将被视为严重错误！
你必须设计一条完整的5-7步合成路线，每一步对应一个→[条件]箭头。
出题思路：不要只写"原料→[条件]产物"这种1步路线，而是设计一条多步转化路径：
- 起始原料 → 官能团转化① → 中间体 → 官能团转化② → ... → 最终目标产物
- 每一步只做一个转化（氧化、还原、卤代、硝化、酯化、水解、酰化、缩合等）
- 只要最终产物正确，路线可以自由设计，不需要与题干路线相同

=== 🔴🔴 题干格式规则（最高警告！）🔴🔴 ===
题干（stem）中绝对不能描述合成路线步骤！
❌ 错误示例：化合物A经硝化反应生成B，B在Fe/HCl条件下还原得C，C与乙酸酐反应得D...
❌ 错误示例：A→[浓HNO₃, 浓H₂SO₄, △]B→[Fe, HCl]C→[(CH₃CO)₂O]D...
✅ 正确示例：化合物G是某抗炎药物的关键中间体，其合成路线如下：
✅ 正确示例：化合物H是一种新型香料的主要成分，可通过以下路线合成：

题干只需一句话交代背景（用途身份），然后直接说"合成路线如下"或"可通过以下路线合成"。
路线图在题干下方单独展示，所以题干里绝对不要重复描述路线步骤！

=== 🔴🔴 方程式和已知信息格式统一（最高警告！违反此规则将被拒绝）🔴🔴 ===
整个题目中所有含化学方程式的答案（第2题、第3题、第5题答案、已知信息）必须使用与路线图完全一致的格式：
✅ 唯一正确格式：{{{{结构式:SMILES}}}}→[条件] {{{{结构式:SMILES}}}}
✅ 多步格式：{{{{结构式:SMILES}}}}→[条件1] {{{{结构式:SMILES}}}}→[条件2] {{{{结构式:SMILES}}}}
✅ 条件写在箭头横线上方的方括号内：[条件]
❌ 绝对禁止格式：A＋B→C 或 A＋B→[条件]C（反应物＋反应物格式）
❌ 绝对禁止格式：A→B（无条件，箭头后没有[条件]方括号）
❌ 绝对禁止格式：文字描述反应 如"苯甲醛与乙酸酐在碱催化下反应生成肉桂酸"
❌ 绝对禁止格式：条件写在箭头下方或用文字描述条件

🔴 以下是错误答案示例（绝对不能出现）：
❌ 错误：苯甲醛与乙酸酐在碱催化下反应生成肉桂酸
❌ 错误：A＋B→[NaOH] C
❌ 错误：A在NaOH条件下反应得B

🔴 以下是正确答案示例（必须这样写）：
✅ Perkin反应：{{{{结构式:O=Cc1ccccc1}}}}→[(CH₃CO)₂O, CH₃COONa, △] {{{{结构式:O=C(O)/C=C/c1ccccc1}}}}
✅ Knoevenagel反应：{{{{结构式:O=Cc1ccccc1}}}}→[CH₂(COOEt)₂, 哌啶, △] {{{{结构式:CCOC(=O)/C=C/c1ccccc1}}}}
✅ 羟醛缩合：{{{{结构式:O=Cc1ccccc1}}}}→[CH₃CHO, NaOH, H₂O] {{{{结构式:O=C/C=C/c1ccccc1}}}}
✅ 硝化：{{{{结构式:c1ccccc1}}}}→[浓HNO₃, 浓H₂SO₄, △] {{{{结构式:O=[N+]([O-])c1ccccc1}}}}
✅ 氰化：{{{{结构式:ClCc1ccccc1}}}}→[KCN, C₂H₅OH] {{{{结构式:N#CCc1ccccc1}}}}

🔴 关键：双反应物反应（Perkin/Knoevenagel/羟醛缩合等），第二个反应物写入条件中！
例如Perkin反应中乙酸酐是反应物也是试剂，写进条件方括号内。

已知信息（new_info）格式示例：
"已知：{{{{结构式:O=Cc1ccccc1}}}}→[(CH₃CO)₂O, CH₃COONa, △] {{{{结构式:O=C(O)C=Cc1ccccc1}}}}"

第2题答案格式示例（必须用路线图格式！）：
"{{{{结构式:ClCc1ccccc1}}}}→[KCN, C₂H₅OH] {{{{结构式:N#CCc1ccccc1}}}}"
或含多步条件：
"{{{{结构式:ClCc1ccccc1}}}}→[(1) KCN, C₂H₅OH (2) H₂O, H⁺] {{{{结构式:O=C(O)Cc1ccccc1}}}}"

第3题答案若含方程式也必须用此格式：
"{{{{结构式:O=Cc1ccccc1}}}}→[NaBH₄] {{{{结构式:OCc1ccccc1}}}}"

第5题答案每步格式：
"第1步：{{{{结构式:SMILES}}}}→[条件] {{{{结构式:SMILES}}}}"

=== 输出JSON格式（严格遵守） ===

{{
  "target_compound": "目标化合物代号及用途",
  "stem": "题干（仅写背景用途，不描述路线步骤，以'合成路线如下'结尾）",
  "questions": [
    {{"number": 1, "content": "小题内容", "type": "官能团识别", "score": 2, "difficulty": "easy"}},
    {{"number": 2, "content": "小题内容", "type": "结构推断/方程式", "score": 2, "difficulty": "easy"}},
    {{"number": 3, "content": "小题内容", "type": "反应条件/试剂选择", "score": 2, "difficulty": "medium"}},
    {{"number": 4, "content": "小题内容（含①②③同分异构条件）", "type": "同分异构体", "score": 3, "difficulty": "hard"}},
    {{"number": 5, "content": "小题内容（含已知信息+制备化合物X）", "type": "合成路线设计", "score": 5, "difficulty": "hard"}}
  ],
  "answers": [
    {{"number": 1, "content": "答案", "scoring_points": ["踩分点"]}},
    {{"number": 2, "content": "答案（方程式用路线图格式：{{{{结构式:SMILES}}}}→[条件] {{{{结构式:SMILES}}}}，条件在箭头上方）", "scoring_points": ["踩分点"]}},
    {{"number": 3, "content": "答案", "scoring_points": ["踩分点"]}},
    {{"number": 4, "content": "答案（同分异构体结构式用{{{{结构式:SMILES}}}}标注）", "scoring_points": ["踩分点"]}},
    {{"number": 5, "content": "合成路线答案（每步：反应物在试剂/条件下得{{{{结构式:SMILES}}}}）", "scoring_points": ["每步产物1分", "每步条件1分"]}}
  ],
  "analysis": "逐题解析",
  "new_info": "第(5)题已知信息中的新反应说明",
  "estimated_difficulty": {difficulty}
}}

=== 各小题要求 ===
第(1)题：官能团名称/反应类型/分子式（针对路线中具体化合物设问）
第(2)题：结构简式推断或反应方程式书写（用{{{{结构式:SMILES}}}}标结构式）
  - 🔴 方程式格式必须与题干路线图一致：{{{{结构式:SMILES}}}}→[条件] {{{{结构式:SMILES}}}}，条件写在箭头上方方括号内
  - 🔴 不得使用传统 A＋B→C 格式，不得使用文字描述反应
  - 🔴 如果条件有多步，用(1)(2)编号，有(2)必须有(1)
第(3)题：反应所需试剂或条件选择（与路线实际反应对应）
  - 若答案含方程式，也必须用路线图格式：A→[条件]B
第(4)题：同分异构体，3个递进条件：①官能团特征反应 ②核磁共振氢谱 ③苯环取代位置/手性碳
第(5)题：合成路线设计，必须含"已知"信息（具体反应方程式），明确写"制备化合物X"，答案5-7步
  - 🔴 已知信息必须用路线图格式：{{{{结构式:SMILES}}}}→[条件] {{{{结构式:SMILES}}}}
  - 🔴 答案每步必须用 →[条件] 格式，条件在箭头上方

=== 第(5)题答案格式（高考标准） ===
答案每步一行，用箭头表示反应，条件写在箭头上方方括号内。这与题干路线图的格式完全一致——箭头上面是反应条件，箭头下方是产物：

第1步：{{结构式:起始原料SMILES}}（原料名）→[条件] {{结构式:产物SMILES}}（产物名）
第2步：{{结构式:上步产物SMILES}}（产物名）→[条件] {{结构式:产物SMILES}}（产物名）
...

重要：每步的→[条件]中，条件就是写在箭头上方的反应条件，格式与题干合成路线图中的箭头标注完全一致。

=== 条件标注规范（严格遵循高考真题格式） ===
条件必须极其简洁，仅写试剂名称/化学式+必要符号，逗号分隔。这是高考阅卷标准！

高考真题中常见的条件写法（请严格模仿）：
- 浓HNO₃, 浓H₂SO₄, △            （苯环硝化）
- H₂, Pd-C 或 H₂, Ni, △           （催化加氢）
- NaOH, H₂O, △                     （卤代烃/酯水解）
- NaOH, 醇, △                      （卤代烃消去）
- 浓H₂SO₄, △                       （醇消去/酯化）
- Br₂, FeBr₃                         （苯环溴代）
- Fe, HCl                             （硝基还原为氨基）
- KMnO₄, H⁺                         （氧化）
- O₂, Cu, △                          （醇催化氧化）
- NaBH₄                              （还原）
- SOCl₂                               （酰氯化）
- (1) O₃ (2) Zn, H₂O               （臭氧化-还原：①臭氧化②还原水解）
- (1) NaOH, H₂O, △ (2) H⁺         （先碱水解后酸化）
- (1) NaNO₂, HCl, 0-5℃ (2) H₂O, △  （重氮化后水解）
- (1) LiAlH₄, 无水乙醚 (2) H₂O     （LiAlH₄还原后水解）

记住：高考真题的条件就长这样！没有"加热回流""催化""反应""溶液中""作用下"等词语。
△就是加热符号，不要再写"加热""△加热"等。
=== 🔴 多步条件标号规则（最高优先级！违反将导致格式错误）🔴 ===
多步反应使用(1)(2)(3)编号，渲染时：
- (1) 显示在箭头上方
- (2) 显示在箭头下方
- (3) 也显示在箭头下方（与(2)同侧）
- 🔴 有(2)必须有(1)！绝不能出现只有(2)没有(1)的情况！
- 🔴 有(3)必须有(1)和(2)！不能跳过标号！

✅ 正确示例：
- →[(1) O₃ (2) Zn, H₂O]    →  (1)在上方，(2)在下方
- →[(1) NaNO₂, HCl, 0-5℃ (2) H₂O, △]  →  (1)在上方，(2)在下方
- →[(1) LiAlH₄, 无水乙醚 (2) H₂O, H⁺ (3) NaOH]  →  (1)在上方，(2)(3)在下方

❌ 错误示例（绝对不能出现）：
- →[(2) Zn, H₂O]    ← 有(2)无(1)，错误！
- →[(1) LiAlH₄ (3) NaOH]   ← 有(3)无(2)，错误！
- →[第一步: O₃ 第二步: Zn, H₂O]  ← 用"第一步""第二步"而非(1)(2)，错误！

🔴 所有含(2)的条件必须同时有(1)！这是硬性规则，没有任何例外！

严禁出现的冗余表述（这些在高考中从不出现）：
✗ "在浓硫酸催化下加热回流反应"  →  应写：浓H₂SO₄, △
✗ "在NaOH水溶液中加热条件下水解"  →  应写：NaOH, H₂O, △
✗ "反应条件为：Pd-C催化加氢"  →  应写：H₂, Pd-C
✗ "用酸性高锰酸钾溶液氧化"  →  应写：KMnO₄, H⁺

=== 第(5)题已知信息格式 ===
已知信息（new_info字段）必须包含具体反应方程式，化学结构式用{{{{结构式:SMILES}}}}标注以ChemDraw格式渲染。
格式必须与题干路线图一致：条件写在箭头上方方括号内，用箭头串联反应步骤。

示例：
"已知：{{结构式:O=Cc1ccccc1}}→[(CH₃CO)₂O, CH₃COONa, △] {{结构式:O=C(O)C=Cc1ccccc1}}"

🔴 关键规则：
- 已知信息的反应式格式必须与题干路线图一致：A→[条件]B→[条件]C
- 已知信息中给出的反应/条件不能与题干路线中的任何一步重复（必须提供全新反应）
- 若已知信息包含多步反应，用箭头串联，每步条件写在箭头上方
- 已知信息必须是题干路线中未出现过的反应，不能是题干路线某一步的复述

=== 化学正确性自检（生成前必须逐项确认） ===
你必须在生成题目后，逐项检查以下内容，确保100%化学正确：
1. 每步反应条件与反应类型匹配（如硝化必须有浓HNO₃+浓H₂SO₄，不能只用稀HNO₃）
2. 所有SMILES表达式有效（苯环c1ccccc1，羧基C(=O)O，硝基N(=O)=O，氨基N，羟基O，醛基C=O）
3. 反应产物与反应物、条件逻辑一致（如硝基还原为氨基必须用Fe/HCl或H₂/Pd-C，不能用NaBH₄）
4. 第(5)题答案路线必须与题干路线不同（不同起始原料或不同中间体或不同反应顺序）
5. 同分异构体条件之间不能互相矛盾
6. 已知信息必须是高中课本未学但学生能理解的新反应，不能是课本已有内容
7. 官能团名称必须准确（"醚键"不是"醚基"，"酯基"不是"酯键"，"酰胺基"不是"酰胺键"）
8. 反应类型判断必须准确（"取代反应""加成反应""消去反应""氧化反应""还原反应""酯化反应""水解反应"）

=== 硬性约束 ===
- 🔴 题干(stem)绝对不能描述合成路线步骤！只写背景用途+结尾"合成路线如下"
- 🔴 题干中绝不能出现"经...得...""→""[条件]"等路线描述
- 化合物用字母代号（A、B、C...），禁止长系统名（仅"苯""甲苯""苯酚""乙酸"等极简名可用）
- 分值：14分制=2+2+2+3+5，15分制=2+2+3+3+5
- 第(5)题已知信息必须包含{{结构式:SMILES}}占位符，以ChemDraw格式显示结构式
- 第(5)题已知信息格式必须与路线图一致：A→[条件]B→[条件]C（条件在箭头上方）
- 第(5)题已知信息中的反应/条件不能与题干路线重复，必须是全新反应
- 🔴 所有含化学方程式的答案（第2题、第3题、第5题）统一使用路线图格式：A→[条件]B（条件在箭头上方方括号内）
- 🔴 绝对禁止使用A＋B→C格式或文字描述反应
- 🔴 第(5)题答案路线必须与题干路线不同
- 🔴 第(5)题答案条件必须极简！只写试剂名+条件符号（如△），逗号分隔，严禁"在...条件下""加热回流""催化""反应"等冗余词
- 🔴 第(5)题答案多步条件用(1)(2)(3)编号，有(2)必须有(1)，有(3)必须有(1)(2)
- 🔴 所有答案中的条件如果包含(2)编号，必须同时有(1)编号，不能只有(2)没有(1)
- 所有结构式用{{{{结构式:SMILES}}}}标注
- SMILES规范：苯环c1ccccc1，羧基C(=O)O，硝基N(=O)=O，氨基N，羟基O，醛基C=O，氰基C#N，酯基C(=O)OC，酰胺基C(=O)N，酰氯C(=O)Cl，磺酸基S(=O)(=O)O

=== 难度：{difficulty} ===

请直接输出JSON，不要用markdown包裹。"""
        return self.generate(system, route_info)

    # ================================================================
    # 智能解析：非结构化文本 → 结构化合成路线
    # ================================================================

    def parse_route_text(self, raw_text: str) -> str:
        """智能解析合成路线文本——将非结构化文本转化为结构化步骤"""
        system = """你是一位有机化学专家。请从以下文本中提取合成路线，转化为严格的JSON格式。

输入可能是：论文摘要、实验步骤描述、反应式列表、手写OCR结果等任何包含化学合成路线信息的文本。

解析规则：
1. 识别化合物编号（A、B、C...或1、2、3...），统一用A、B、C...标记
2. 提取每步的反应物、试剂/条件、产物
3. 识别反应类型（取代/加成/消去/氧化/还原/酯化/水解/加聚/缩聚等）
4. 如果文本中没有明确某步的反应类型，根据反应物和产物推断，填写"推断：XX"
5. 只提取3-8步的合成片段
6. 对于非高中反应，在reaction_type中标注"新信息：XX"

输出严格JSON格式：
{
  "title": "合成路线标题（从文本中提取或自动生成）",
  "steps": [
    {
      "step_number": 1,
      "reactant": "反应物名称",
      "reagent": "试剂与反应条件",
      "product": "产物名称",
      "reaction_type": "反应类型"
    }
  ],
  "notes": "补充说明（如有不确定的地方或识别的难点）"
}"""
        return self.generate(system, raw_text)

    def ocr_image(self, image_base64: str, strategy: str = "auto") -> str:
        """
        使用 easyocr 从图片中提取文字（多策略增强版）
        
        策略：
        - "auto": 自动尝试多种预处理策略，选文字最多的结果
        - "default": 标准预处理（灰度+对比度+锐化）
        - "adaptive": 自适应阈值二值化（适合白底黑字）
        - "inverted": 反转+自适应（适合黑底白字/深色背景）
        - "scale2x": 2倍放大+标准预处理（适合小文字）
        """
        import base64 as b64
        import io
        import easyocr
        from PIL import Image, ImageEnhance, ImageFilter, ImageOps

        # 初始化 reader（只初始化一次，缓存为类变量）
        if not hasattr(LLMClient, '_ocr_reader'):
            LLMClient._ocr_reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        reader = LLMClient._ocr_reader

        # 解码图片
        image_bytes = b64.b64decode(image_base64)
        img = Image.open(io.BytesIO(image_bytes))

        def preprocess_and_ocr(pil_img, preprocess_fn, name="unknown"):
            """对图片执行预处理并OCR，返回提取的文本"""
            try:
                processed = preprocess_fn(pil_img.copy())
                buf = io.BytesIO()
                processed.save(buf, format='PNG')
                results = reader.readtext(buf.getvalue(), detail=0, paragraph=True)
                lines = []
                for r in results:
                    r = r.strip()
                    if len(r) >= 2 and not all(c in '.-_=~|/\\[](){}<>←→↑↓→←•·' for c in r):
                        lines.append(r)
                return '\n'.join(lines)
            except Exception:
                return ""

        # === 定义多种预处理策略 ===
        strategies = {}

        # 策略1：标准预处理（灰度+对比度+锐化+放大）
        def standard_preprocess(pil_img):
            if pil_img.mode != 'L':
                pil_img = pil_img.convert('L')
            w, h = pil_img.size
            if w < 800:
                ratio = 800 / w
                pil_img = pil_img.resize((800, int(h * ratio)), Image.LANCZOS)
            enhancer = ImageEnhance.Contrast(pil_img)
            pil_img = enhancer.enhance(2.0)
            return pil_img.filter(ImageFilter.SHARPEN)
        strategies["default"] = standard_preprocess

        # 策略2：自适应阈值二值化（适合白底黑字的清晰图片）
        def adaptive_preprocess(pil_img):
            if pil_img.mode != 'L':
                pil_img = pil_img.convert('L')
            w, h = pil_img.size
            if w < 1000:
                ratio = 1000 / w
                pil_img = pil_img.resize((1000, int(h * ratio)), Image.LANCZOS)
            enhancer = ImageEnhance.Contrast(pil_img)
            pil_img = enhancer.enhance(3.0)
            import numpy as np
            arr = np.array(pil_img)
            threshold = np.median(arr)
            pil_img = pil_img.point(lambda x: 0 if x < threshold * 0.8 else 255)
            return pil_img
        strategies["adaptive"] = adaptive_preprocess

        # 策略3：反转+自适应
        def inverted_preprocess(pil_img):
            if pil_img.mode != 'L':
                pil_img = pil_img.convert('L')
            w, h = pil_img.size
            if w < 1000:
                ratio = 1000 / w
                pil_img = pil_img.resize((1000, int(h * ratio)), Image.LANCZOS)
            pil_img = ImageOps.invert(pil_img)
            enhancer = ImageEnhance.Contrast(pil_img)
            pil_img = enhancer.enhance(2.5)
            import numpy as np
            arr = np.array(pil_img)
            threshold = np.median(arr)
            pil_img = pil_img.point(lambda x: 0 if x < threshold * 0.7 else 255)
            return pil_img
        strategies["inverted"] = inverted_preprocess

        # 策略4：2倍放大+轻度对比度
        def scale2x_preprocess(pil_img):
            if pil_img.mode != 'L':
                pil_img = pil_img.convert('L')
            w, h = pil_img.size
            ratio = max(1200 / w, 1.5)
            pil_img = pil_img.resize((int(w * ratio), int(h * ratio)), Image.LANCZOS)
            enhancer = ImageEnhance.Contrast(pil_img)
            pil_img = enhancer.enhance(1.5)
            return pil_img.filter(ImageFilter.SHARPEN)
        strategies["scale2x"] = scale2x_preprocess

        # === 执行OCR ===
        if strategy == "auto":
            best_text = ""
            for name, fn in strategies.items():
                text = preprocess_and_ocr(img, fn, name)
                if len(text) > len(best_text):
                    best_text = text
            return best_text
        elif strategy in strategies:
            return preprocess_and_ocr(img, strategies[strategy], strategy)
        else:
            return preprocess_and_ocr(img, standard_preprocess, "default")

    def ocr_image_detailed(self, image_base64: str) -> list:
        """
        OCR增强版：返回带位置信息的详细结果
        便于结构化提取标签、试剂、箭头
        """
        import base64 as b64
        import io
        import easyocr
        from PIL import Image, ImageEnhance, ImageFilter

        if not hasattr(LLMClient, '_ocr_reader'):
            LLMClient._ocr_reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
        reader = LLMClient._ocr_reader

        image_bytes = b64.b64decode(image_base64)
        img = Image.open(io.BytesIO(image_bytes))

        # 预处理：转灰度+放大+增强
        if img.mode != 'L':
            img = img.convert('L')
        w, h = img.size
        if w < 1000:
            ratio = 1000 / w
            img = img.resize((1000, int(h * ratio)), Image.LANCZOS)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.5)
        img = img.filter(ImageFilter.SHARPEN)

        buf = io.BytesIO()
        img.save(buf, format='PNG')

        # detail=1 返回位置信息: [bbox, text, confidence]
        results = reader.readtext(buf.getvalue(), detail=1, paragraph=False)

        detailed = []
        for bbox, text, conf in results:
            text = text.strip()
            if len(text) >= 1 and conf > 0.1:
                # 计算中心点Y坐标（用于判断行）
                ys = [p[1] for p in bbox]
                center_y = sum(ys) / len(ys)
                center_x = (bbox[0][0] + bbox[2][0]) / 2
                detailed.append({
                    "text": text,
                    "confidence": round(conf, 3),
                    "center_y": round(center_y, 1),
                    "center_x": round(center_x, 1),
                    "width": round(bbox[2][0] - bbox[0][0], 1),
                    "height": round(bbox[2][1] - bbox[0][1], 1),
                })

        return detailed

    def parse_route_from_ocr(self, image_base64: str) -> str:
        """
        OCR + LLM 解析：多策略OCR + 结构化提取 + LLM还原
        核心改进：先用详细OCR获取位置信息，结构化排列后再给LLM
        """
        # 第一步：详细OCR（带位置信息）
        detailed = self.ocr_image_detailed(image_base64)

        # 第二步：同时做多策略OCR获取纯文本
        ocr_text = self.ocr_image(image_base64, strategy="auto")

        # 第三步：结构化排列OCR结果
        structured_text = self._structure_ocr_results(detailed)

        # 第四步：合并所有OCR结果
        all_text = ocr_text
        if structured_text and structured_text not in all_text:
            all_text = all_text + "\n---\n" + structured_text if all_text else structured_text

        # 如果完全没有文字
        if not all_text or len(all_text.strip()) < 2:
            return json.dumps({
                "title": "",
                "steps": [],
                "notes": "图片中未检测到任何文字。请上传包含化合物名称和反应条件的文字图片。若图片为纯结构式，建议用文本粘贴方式输入合成路线。",
                "_ocr_text": "(未检测到文字)",
                "_ocr_detailed": detailed,
                "_debug": "OCR完全失败"
            }, ensure_ascii=False)

        # 第五步：LLM解析
        llm_response = self._parse_ocr_with_llm_v2(all_text, detailed)

        # 解析JSON
        try:
            result = json.loads(llm_response)
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{[\s\S]*\}', llm_response)
            if json_match:
                try:
                    result = json.loads(json_match.group())
                except json.JSONDecodeError:
                    result = {"steps": [], "notes": "LLM返回格式异常，请重试"}
            else:
                result = {"steps": [], "notes": "LLM返回格式异常，请重试"}

        result["_ocr_text"] = all_text
        result["_ocr_detailed_count"] = len(detailed)

        return json.dumps(result, ensure_ascii=False)

    def _structure_ocr_results(self, detailed: list) -> str:
        """将带位置信息的OCR结果按行排列，识别标签-试剂-标签的链条"""
        if not detailed:
            return ""

        # 按Y坐标分组（同一行）
        rows = {}
        for item in detailed:
            y = round(item["center_y"] / 10) * 10  # 10px容差分组
            if y not in rows:
                rows[y] = []
            rows[y].append(item)

        # 每行按X坐标排序
        lines = []
        for y in sorted(rows.keys()):
            row_items = sorted(rows[y], key=lambda x: x["center_x"])
            line_text = "  |  ".join([item["text"] for item in row_items])
            lines.append(f"[Y={y}] {line_text}")

        return "\n".join(lines)

    def _parse_ocr_with_llm_v2(self, ocr_text: str, detailed: list) -> str:
        """LLM解析OCR文字 V2：支持结构化位置信息"""
        # 统计OCR提取到的关键信息
        compound_labels = []
        reagent_keywords = []
        for item in detailed:
            t = item["text"]
            if len(t) <= 2 and (t.isalpha() or t.isalnum()):
                compound_labels.append(t)
            if any(kw in t.upper() for kw in ['HNO', 'H2SO', 'HCL', 'HCI', 'KMNO', 'NAOH', 'FE', 'CH3CO', 'AC2O', 'NABH', 'PD-C', 'SOCL', 'BR2', 'CL2', '浓', '酸', '碱', '氧化', '还原', '硝化', '酯化', '酰化', '水解']):
                reagent_keywords.append(t)

        system = f"""你是一位有机化学专家，专门从OCR识别出的碎片化文字中还原合成路线。

=== 当前OCR统计 ===
- 检测到 {len(detailed)} 个文字片段
- 其中可能的化合物标签: {compound_labels[:20] if compound_labels else '无'}
- 其中可能的试剂关键词: {reagent_keywords[:20] if reagent_keywords else '无'}

=== 核心任务 ===
从OCR文字中提取所有反应步骤。**即使信息不完整，只要有反应步骤的蛛丝马迹，就必须输出步骤！**

=== OCR文字格式说明 ===
你收到的文字中可能包含：
1. 普通OCR文本：多策略OCR提取的纯文本
2. 结构化文本：按Y坐标排列的文字，格式为"[Y=xxx] 文字1 | 文字2 | ..."
   - 同一行的文字在同一高度，可能是连续的内容
   - 不同行的文字可能对应不同的化合物或试剂

=== 解析规则 ===

规则1：识别"标签→试剂→标签→试剂→标签"的链条
- 合成路线图通常格式：A —试剂→ B —试剂→ C —试剂→ D
- 从OCR文字中找到标签和试剂的交替模式

规则2：试剂→反应类型映射
- HNO₃/H₂SO₄ 或 浓硝酸/浓硫酸 → 硝化反应
- Fe/HCl → 还原反应（硝基→氨基）
- KMnO₄/H⁺ → 氧化反应
- NaOH/H₂O → 水解反应
- 浓H₂SO₄/△ → 酯化/消去
- (CH₃CO)₂O 或 乙酸酐 → 酰化反应
- H₂/Pd-C → 催化加氢
- Br₂/Fe → 溴代反应
- SOCl₂ → 酰氯化
- CH₃OH/浓H₂SO₄ → 酯化

规则3：**只要有任意试剂信息，就必须输出步骤**
- 哪怕只有1个试剂，也要输出1步
- 哪怕化合物名称是A/B/C标签，也要输出
- 哪怕只能从试剂推断反应类型，也要输出
- 绝不要返回空数组！

=== 输出格式（严格JSON，不要用markdown包裹） ===
{{
  "title": "从图片识别的合成路线",
  "steps": [
    {{
      "step_number": 1,
      "reactant": "反应物",
      "reagent": "试剂与条件",
      "product": "产物",
      "reaction_type": "反应类型"
    }}
  ],
  "notes": "说明"
}}"""
        user_prompt = f"""以下是从合成路线图片中OCR识别出的文字，请提取合成路线步骤。

=== OCR文字 ===
{ocr_text}
=== 文字结束 ===

请提取合成路线。记住：**只要有任意的反应信息，就必须输出步骤！**"""
        return self.generate(system, user_prompt, temperature=0.2)

    # ================================================================
    # 化学结构图像识别（NCI/CADD API + PubChem fallback）
    # ================================================================

    def _recognize_structure_nci(self, image_bytes: bytes) -> str:
        """
        使用 NCI/CADD Chemical Identifier Resolver 将结构式图像转为 SMILES
        
        API: https://cactus.nci.nih.gov/chemical/structure
        支持 png, jpg, gif 等格式的结构式图片
        返回 SMILES 字符串，失败返回空字符串
        """
        import requests
        try:
            url = "https://cactus.nci.nih.gov/chemical/structure"
            files = {"file": ("structure.png", image_bytes, "image/png")}
            params = {"format": "smiles"}
            resp = requests.post(url, files=files, params=params, timeout=10)
            if resp.status_code == 200:
                smiles = resp.text.strip()
                if smiles and len(smiles) > 1:
                    return smiles
            return ""
        except Exception:
            return ""

    def _recognize_structure_pubchem(self, image_bytes: bytes) -> str:
        """
        使用 PubChem API 将结构式图像转为 SMILES（fallback）
        
        PubChem 支持通过图像搜索结构，使用 PUG-REST 的 /compound/fastsimilarity 或
        /compound/fastidentity 接口，但需要先上传图像获取结构标识符。
        
        这里使用 PubChem 的 ID 转换服务：先尝试通过图像识别获取 CID，再转 SMILES
        """
        import requests
        try:
            # PubChem 图像上传接口（需要 multipart）
            url = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/fastidentity"
            files = {"file": ("structure.png", image_bytes, "image/png")}
            params = {"format": "smiles"}
            resp = requests.post(url, files=files, params=params, timeout=10)
            if resp.status_code == 200:
                content = resp.text.strip()
                if content and len(content) > 1 and "<" not in content:
                    return content
            return ""
        except Exception:
            return ""

    def _split_image_to_grid(self, image_bytes: bytes, cols: int = 3, rows: int = 2) -> list:
        """
        将图片切分为网格，返回每个格子的字节数据
        
        Args:
            image_bytes: 原始图片字节
            cols: 列数
            rows: 行数
        
        Returns:
            [(col, row, cell_bytes), ...] 每个格子的位置和字节数据
        """
        import io
        from PIL import Image
        
        cells = []
        try:
            img = Image.open(io.BytesIO(image_bytes))
            w, h = img.size
            cell_w = w // cols
            cell_h = h // rows
            
            for row in range(rows):
                for col in range(cols):
                    left = col * cell_w
                    top = row * cell_h
                    right = min(left + cell_w, w)
                    bottom = min(top + cell_h, h)
                    
                    # 跳过太小的格子
                    if right - left < 100 or bottom - top < 100:
                        continue
                    
                    cell = img.crop((left, top, right, bottom))
                    buf = io.BytesIO()
                    cell.save(buf, format='PNG')
                    cells.append((col, row, buf.getvalue()))
        except Exception:
            pass
        
        return cells

    def recognize_structures_from_image(self, image_base64: str, image_type: str = "png") -> dict:
        """
        从图片中识别化学结构式（多策略 + 网格切分）
        
        Args:
            image_base64: 图片的 base64 编码
            image_type: 图片格式
        
        Returns:
            dict with keys:
            - smiles_list: 识别到的 SMILES 列表
            - source: 识别来源 (nci/pubchem/none)
            - error: 错误信息
        """
        import base64 as b64
        
        try:
            image_bytes = b64.b64decode(image_base64)
        except Exception as e:
            return {"smiles_list": [], "source": "none", "error": f"Base64解码失败: {str(e)}"}
        
        all_smiles = []
        sources = []
        
        # 策略1: 整图识别 → NCI
        smiles = self._recognize_structure_nci(image_bytes)
        if smiles:
            all_smiles.append(smiles)
            sources.append("nci_full")
        
        # 策略2: 整图识别 → PubChem（如果NCI失败）
        if not all_smiles:
            smiles = self._recognize_structure_pubchem(image_bytes)
            if smiles:
                all_smiles.append(smiles)
                sources.append("pubchem_full")
        
        # 策略3: 网格切分识别（适用于多结构路线图）
        # 尝试多种切分方案
        if len(all_smiles) <= 1:
            for grid_cols, grid_rows in [(3, 2), (2, 2), (4, 2), (3, 3)]:
                cells = self._split_image_to_grid(image_bytes, grid_cols, grid_rows)
                if not cells:
                    continue
                
                for col, row, cell_bytes in cells:
                    smiles = self._recognize_structure_nci(cell_bytes)
                    if smiles and smiles not in all_smiles:
                        all_smiles.append(smiles)
                        sources.append(f"nci_grid_{grid_cols}x{grid_rows}")
                
                # 如果已经识别到足够多的结构，停止切分
                if len(all_smiles) >= 3:
                    break
        
        # 去重并返回
        unique_smiles = list(dict.fromkeys(all_smiles))  # 保持顺序去重
        
        if unique_smiles:
            return {
                "smiles_list": unique_smiles,
                "source": "+".join(sources),
                "error": None,
            }
        
        return {"smiles_list": [], "source": "none", "error": "NCI和PubChem均无法识别图片中的结构式"}

    def parse_route_from_image(self, image_base64: str, image_type: str = "png") -> str:
        """
        从图片中识别合成路线（主入口）v4.0 — 快速版
        
        管线（简化）：
        1. EasyOCR 详细扫描（1次）→ 文字 + 位置信息
        2. NCI API 整图识别（10s超时）→ SMILES
        3. LLM 一次性解析：OCR文字 + SMILES → 结构化合成路线
        """
        # 第一步：OCR详细扫描（仅1次，带位置信息）
        detailed = self.ocr_image_detailed(image_base64)
        
        # 提取纯文本
        ocr_text = "\n".join([d["text"] for d in detailed])
        
        # 如果完全没有文字
        if not ocr_text or len(ocr_text.strip()) < 2:
            return json.dumps({
                "title": "",
                "steps": [],
                "notes": "图片中未检测到文字。请上传包含化合物名称和反应条件的文字图片。",
                "_ocr_text": "(未检测到文字)",
            }, ensure_ascii=False)
        
        # 第二步：NCI 结构式识别（仅整图，10s超时，快速失败）
        smiles_list = []
        try:
            import base64 as b64
            image_bytes = b64.b64decode(image_base64)
            smiles = self._recognize_structure_nci(image_bytes)
            if smiles:
                smiles_list.append(smiles)
        except Exception:
            pass
        
        # 第三步：一次性LLM解析（OCR + SMILES合并在一起）
        return self._parse_ocr_with_smiles(ocr_text, detailed, smiles_list)

    def _parse_ocr_with_smiles(self, ocr_text: str, detailed: list, smiles_list: list) -> str:
        """一次性LLM解析：OCR文字 + 结构式SMILES → 合成路线"""
        # 统计关键信息
        compound_labels = []
        reagent_keywords = []
        for item in detailed:
            t = item["text"]
            if len(t) <= 2 and (t.isalpha() or t.isalnum()):
                compound_labels.append(t)
            if any(kw in t.upper() for kw in ['HNO', 'H2SO', 'HCL', 'HCI', 'KMNO', 'NAOH', 'FE', 'CH3CO', 'AC2O', 'NABH', 'PD-C', 'SOCL', 'BR2', 'CL2', '浓', '酸', '碱', '氧化', '还原', '硝化', '酯化', '酰化', '水解']):
                reagent_keywords.append(t)

        smiles_info = ""
        if smiles_list:
            smiles_info = f"\n=== 识别到的结构式SMILES ===\n" + "\n".join(f"- {s}" for s in smiles_list)

        system = f"""你是一位有机化学专家，专门从OCR识别出的碎片化文字和化学结构式SMILES中还原合成路线。

=== 当前OCR统计 ===
- 检测到 {len(detailed)} 个文字片段
- 可能的化合物标签: {compound_labels[:20] if compound_labels else '无'}
- 可能的试剂关键词: {reagent_keywords[:20] if reagent_keywords else '无'}

=== 核心任务 ===
从OCR文字和结构式SMILES中提取所有反应步骤。**即使信息不完整，只要有反应步骤的蛛丝马迹，就必须输出步骤！**

=== 解析规则 ===
1. 识别"标签→试剂→标签→试剂→标签"的链条
2. 试剂→反应类型映射：HNO₃/H₂SO₄→硝化；Fe/HCl→还原；KMnO₄/H⁺→氧化；NaOH→水解；浓H₂SO₄/△→酯化/消去；(CH₃CO)₂O→酰化；H₂/Pd-C→加氢；Br₂→溴代；SOCl₂→酰氯化
3. **只要有任意试剂信息，就必须输出步骤，绝不要返回空数组！**
4. 如果有SMILES，将其与OCR文字中的化合物标签对应

=== 输出格式（严格JSON） ===
{{
  "title": "从图片识别的合成路线",
  "steps": [
    {{
      "step_number": 1,
      "reactant": "反应物",
      "reagent": "试剂与条件",
      "product": "产物",
      "reaction_type": "反应类型"
    }}
  ],
  "notes": "说明"
}}"""

        user_prompt = f"""以下是从合成路线图片中提取的信息，请还原合成路线。

=== OCR文字 ===
{ocr_text}
=== 文字结束 ===
{smiles_info}

请提取合成路线。**只要有任意的反应信息，就必须输出步骤，绝不要返回空steps！**"""
        
        llm_response = self.generate(system, user_prompt, temperature=0.2)
        
        # 解析JSON
        try:
            result = json.loads(llm_response)
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{[\s\S]*\}', llm_response)
            if json_match:
                try:
                    result = json.loads(json_match.group())
                except json.JSONDecodeError:
                    result = {"steps": [], "notes": "LLM返回格式异常，请重试"}
            else:
                result = {"steps": [], "notes": "LLM返回格式异常，请重试"}
        
        result["_ocr_text"] = ocr_text
        return json.dumps(result, ensure_ascii=False)

    # ================================================================
    # v5.0 图片识别管线：MolScribe(结构) + 豆包(箭头/条件) + DeepSeek(串联+命题)
    # ================================================================

    # MolScribe 模型缓存
    _molscribe_model = None
    _molscribe_ckpt = None

    def _init_molscribe(self):
        """懒加载 MolScribe 模型"""
        if LLMClient._molscribe_model is not None:
            return LLMClient._molscribe_model
        
        import torch
        from molscribe import MolScribe
        from huggingface_hub import hf_hub_download
        import os
        
        # 下载/加载模型
        ckpt_path = os.environ.get("MOLSCRIBE_MODEL_PATH", "")
        if not ckpt_path or not os.path.exists(ckpt_path):
            os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
            ckpt_path = hf_hub_download('yujieq/MolScribe', 'swin_base_char_aux_1m.pth')
        
        LLMClient._molscribe_model = MolScribe(ckpt_path, device=torch.device('cpu'))
        LLMClient._molscribe_ckpt = ckpt_path
        return LLMClient._molscribe_model

    # 豆包客户端缓存
    _doubao_client = None

    def _init_doubao_client(self):
        """懒加载豆包视觉模型客户端"""
        from config import DOUBAO_API_KEY, DOUBAO_BASE_URL, DOUBAO_ENDPOINT_ID
        
        if LLMClient._doubao_client is not None:
            return LLMClient._doubao_client
        
        if not DOUBAO_API_KEY:
            raise RuntimeError("未配置豆包API Key，请在.env中设置DOUBAO_API_KEY和DOUBAO_ENDPOINT_ID")
        
        LLMClient._doubao_client = OpenAI(
            api_key=DOUBAO_API_KEY,
            base_url=DOUBAO_BASE_URL,
        )
        return LLMClient._doubao_client

    def recognize_structures_molscribe(self, image_bytes: bytes) -> list:
        """
        使用 MolScribe 识别图片中的化学结构式
        
        策略：将图片切分为网格，逐格识别，去重返回SMILES列表
        """
        import io
        from PIL import Image
        
        model = self._init_molscribe()
        img = Image.open(io.BytesIO(image_bytes))
        w, h = img.size
        
        smiles_set = set()
        results = []
        
        # 策略1：整图识别（适合单结构图片）
        try:
            buf = io.BytesIO()
            img.save(buf, format='PNG')
            output = model.predict_image_file(buf, return_confidence=True)
            smiles = output.get('smiles', '')
            confidence = output.get('confidence', 0)
            if smiles and len(smiles) > 2 and confidence > 0.5:
                if smiles not in smiles_set:
                    smiles_set.add(smiles)
                    results.append({'smiles': smiles, 'confidence': confidence, 'source': 'full'})
        except Exception:
            pass
        
        # 策略2：网格切分识别（适合多结构路线图）
        for grid_cols, grid_rows in [(3, 2), (2, 2), (4, 2), (3, 1)]:
            if len(results) >= 4:
                break
            cell_w = w // grid_cols
            cell_h = h // grid_rows
            if cell_w < 100 or cell_h < 100:
                continue
            
            for row in range(grid_rows):
                for col in range(grid_cols):
                    if len(results) >= 8:
                        break
                    left = col * cell_w
                    top = row * cell_h
                    right = min(left + cell_w, w)
                    bottom = min(top + cell_h, h)
                    
                    cell = img.crop((left, top, right, bottom))
                    # 跳过空白格子（检查是否主要是白色背景）
                    try:
                        import numpy as np
                        cell_arr = np.array(cell.convert('L'))
                        if np.mean(cell_arr) > 240:  # 太白的格子跳过
                            continue
                    except Exception:
                        pass
                    
                    try:
                        buf = io.BytesIO()
                        cell.save(buf, format='PNG')
                        output = model.predict_image_file(buf, return_confidence=True)
                        smiles = output.get('smiles', '')
                        confidence = output.get('confidence', 0)
                        if smiles and len(smiles) > 2 and confidence > 0.3:
                            if smiles not in smiles_set:
                                smiles_set.add(smiles)
                                results.append({
                                    'smiles': smiles,
                                    'confidence': confidence,
                                    'source': f'grid_{grid_cols}x{grid_rows}_{row}_{col}'
                                })
                    except Exception:
                        pass
        
        return results

    def recognize_route_doubao(self, image_base64: str) -> dict:
        """
        使用豆包视觉模型识别箭头和反应条件
        
        Returns:
            {
                "compounds": [{"label": "A", "position": "left"}, ...],
                "arrows": [{"from": "A", "to": "B", "conditions": "浓HNO₃, 浓H₂SO₄, △"}, ...],
                "route_order": ["A", "B", "C", ...]
            }
        """
        from config import DOUBAO_ENDPOINT_ID, DOUBAO_VISION_MODEL
        
        client = self._init_doubao_client()
        model = DOUBAO_ENDPOINT_ID or DOUBAO_VISION_MODEL
        
        system_prompt = """你是一位有机化学专家，专门从合成路线图中识别化合物、箭头和反应条件。

请仔细分析图片，识别以下信息：
1. 每个化合物的标签（A、B、C等字母编号）
2. 化合物之间的箭头方向（从哪个化合物到哪个化合物）
3. 箭头上方/下方的反应条件（试剂、温度等）
4. 整个路线的顺序（从起始原料到最终产物）

请以JSON格式返回，不要用markdown包裹。"""

        user_prompt = """请识别这张合成路线图中的：
1. 所有化合物标签（A、B、C等）
2. 箭头方向（从X到Y）
3. 每个箭头对应的反应条件
4. 路线顺序

输出JSON格式：
{
  "compounds": [{"label": "A", "description": "苯"}, ...],
  "arrows": [{"from": "A", "to": "B", "conditions": "浓HNO₃, 浓H₂SO₄, △"}, ...],
  "route_order": ["A", "B", "C", ...],
  "notes": "补充说明"
}"""

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": [
                        {"type": "text", "text": user_prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
                    ]},
                ],
                max_tokens=4096,
                timeout=60,
            )
            content = response.choices[0].message.content
            
            # 解析JSON
            import re
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                return json.loads(json_match.group())
            return {"compounds": [], "arrows": [], "route_order": [], "notes": "豆包返回格式异常"}
        except Exception as e:
            return {"compounds": [], "arrows": [], "route_order": [], "notes": f"豆包识别失败: {str(e)}"}

    def parse_route_from_image_v5(self, image_base64: str, image_type: str = "png") -> str:
        """
        图片识别管线 v5.0 — 豆包(箭头/条件) + MolScribe(结构) + DeepSeek(串联)
        
        管线（豆包优先，确保不阻塞）：
        1. 豆包视觉模型：识别箭头、反应条件、路线顺序
        2. MolScribe：识别所有化合物结构 → SMILES列表
        3. DeepSeek：合并SMILES + 条件信息 → 结构化合成路线
        """
        import base64 as b64
        from config import DOUBAO_API_KEY
        
        image_bytes = b64.b64decode(image_base64)
        
        results = {
            "molscribe_smiles": [],
            "doubao_route": {},
            "error": None,
        }
        
        # === 第一步：豆包识别箭头和条件（优先，快速完成） ===
        if DOUBAO_API_KEY:
            try:
                doubao_result = self.recognize_route_doubao(image_base64)
                results["doubao_route"] = doubao_result
            except Exception as e:
                results["doubao_error"] = str(e)
        else:
            results["doubao_skip"] = "未配置豆包API Key，跳过视觉识别"
        
        # === 第二步：MolScribe 识别化合物结构（耗时长，放后面） ===
        try:
            smiles_results = self.recognize_structures_molscribe(image_bytes)
            results["molscribe_smiles"] = [r["smiles"] for r in smiles_results]
            results["molscribe_detail"] = smiles_results
        except Exception as e:
            results["molscribe_error"] = str(e)
            # MolScribe 失败时，回退到 NCI/PubChem API
            try:
                nci_result = self.recognize_structures_from_image(image_base64, image_type)
                if nci_result.get("smiles_list"):
                    results["molscribe_smiles"] = nci_result["smiles_list"]
                    results["molscribe_fallback"] = "NCI/PubChem"
                    results["molscribe_error"] = None
            except Exception:
                pass
        
        # === 第三步：DeepSeek 合并所有信息 ===
        return self._merge_v5_with_deepseek(results)

    def _merge_v5_with_deepseek(self, results: dict) -> str:
        """DeepSeek合并MolScribe SMILES + 豆包条件 → 结构化合成路线"""
        smiles_list = results.get("molscribe_smiles", [])
        doubao = results.get("doubao_route", {})
        
        smiles_info = ""
        if smiles_list:
            smiles_info = "=== MolScribe识别到的结构式SMILES ===\n" + "\n".join(
                f"- 化合物{chr(65+i)}: {s}" for i, s in enumerate(smiles_list)
            )
        
        doubao_info = ""
        if doubao.get("compounds") or doubao.get("arrows"):
            doubao_info = "=== 豆包识别到的路线信息 ===\n"
            if doubao.get("compounds"):
                doubao_info += "化合物标签:\n" + "\n".join(
                    f"- {c.get('label', '?')}: {c.get('description', '')}" for c in doubao["compounds"]
                ) + "\n"
            if doubao.get("arrows"):
                doubao_info += "反应步骤:\n" + "\n".join(
                    f"- {a.get('from', '?')} → {a.get('to', '?')} [{a.get('conditions', '')}]"
                    for a in doubao["arrows"]
                ) + "\n"
            if doubao.get("route_order"):
                doubao_info += f"路线顺序: {' → '.join(doubao['route_order'])}\n"
            if doubao.get("notes"):
                doubao_info += f"备注: {doubao['notes']}\n"
        
        if not smiles_info and not doubao_info:
            return json.dumps({
                "title": "识别失败",
                "steps": [],
                "notes": "MolScribe和豆包均未能识别图片中的内容。请确保图片清晰且包含化学结构式。",
                "_molscribe": results,
            }, ensure_ascii=False)
        
        system = """你是一位有机化学专家，专门从化学结构识别和视觉分析结果中还原合成路线。

=== 核心任务 ===
结合 MolScribe 识别的结构式 SMILES 和豆包视觉模型识别的路线信息，还原完整的合成路线。

=== 解析规则 ===
1. 将SMILES与化合物标签对应（SMILES[0]→A, SMILES[1]→B, ...）
2. 结合豆包识别的箭头和条件，构建完整的反应步骤
3. 从试剂推断反应类型
4. 每个步骤都要包含试剂和条件（高考格式：逗号分隔，如"浓HNO₃, 浓H₂SO₄, △"）

=== 输出格式（严格JSON） ===
{
  "title": "从图片识别的合成路线",
  "steps": [
    {
      "step_number": 1,
      "reactant": "化合物A",
      "reagent": "试剂, 条件",
      "product": "化合物B",
      "reaction_type": "反应类型"
    }
  ],
  "notes": "识别说明"
}"""

        user_prompt = f"""请根据以下信息还原合成路线。

{smiles_info}

{doubao_info}

请提取合成路线。将SMILES按顺序对应到化合物标签，结合豆包的条件信息构建完整步骤。"""

        llm_response = self.generate(system, user_prompt, temperature=0.2)
        
        try:
            result = json.loads(llm_response)
        except json.JSONDecodeError:
            import re
            json_match = re.search(r'\{[\s\S]*\}', llm_response)
            if json_match:
                try:
                    result = json.loads(json_match.group())
                except json.JSONDecodeError:
                    result = {"steps": [], "notes": "LLM返回格式异常"}
            else:
                result = {"steps": [], "notes": "LLM返回格式异常"}
        
        result["_molscribe"] = {
            "smiles": smiles_list,
            "detail": results.get("molscribe_detail", []),
        }
        result["_doubao"] = doubao
        result["_ocr_text"] = f"MolScribe: {smiles_list}\nDoubao: {json.dumps(doubao, ensure_ascii=False)}"
        return json.dumps(result, ensure_ascii=False)

    def extract_route_from_paper(self, paper_text: str) -> str:
        """从论文文本中提取合成路线"""
        system = """你是一位有机化学专家。请从以下论文内容中提取全合成路线。
对每条反应步骤，以结构化格式输出：
步骤编号 | 反应物(SMILES) | 试剂与条件 | 产物(SMILES) | 反应类型 | 高中知识点匹配度(高/中/低)

注意：
1. 只提取3-8步的合成片段
2. 优先提取包含高中必会反应类型的步骤
3. 对于非高中反应，标注为"新信息"并给出简要解释
4. 确保SMILES格式正确"""
        return self.generate(system, paper_text)

    # ================================================================
    # 质量验证
    # ================================================================

    def validate_reaction(self, reaction_info: str) -> str:
        """验证反应方程式配平和原子守恒"""
        system = """你是一位有机化学专家。请验证以下反应信息的化学正确性：
1. 检查原子守恒（反应前后原子种类和数量是否一致）
2. 检查方程式配平是否正确
3. 检查SMILES格式是否正确
4. 检查反应条件是否合理
5. 标注任何发现的错误

请以JSON格式输出：
{
  "is_valid": true/false,
  "atom_balanced": true/false,
  "equation_balanced": true/false,
  "smiles_valid": true/false,
  "issues": ["问题1", "问题2"],
  "corrections": {"field": "修正值"}
}"""
        return self.generate(system, reaction_info)

    def evaluate_novelty(self, question: str) -> str:
        """评估题目新颖度（与高考真题对比）"""
        system = """你是一位高考化学命题研究专家。请评估以下题目与近5年高考真题的相似度。
分析维度：
1. 合成路线是否与高考真题雷同
2. 设问角度是否新颖
3. 考查知识点组合是否独特

输出JSON：
{
  "novelty_score": 0-100,
  "similar_questions": ["相似真题描述"],
  "unique_points": ["独特之处"],
  "risk_level": "低/中/高"
}"""
        return self.generate(system, question)


# 全局单例
llm_client = LLMClient()
