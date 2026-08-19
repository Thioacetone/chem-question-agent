# ============================================
# Stage 1: 构建前端
# ============================================
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci 2>/dev/null || npm install
# Force cache bust: 2026-08-19-v10
COPY frontend/ ./
RUN npm run build

# ============================================
# Stage 2: 后端运行环境
# ============================================
FROM python:3.11-slim

WORKDIR /app

# 安装 RDKit 系统依赖
RUN apt-get update && apt-get install -y --no-install-recommends \
    libxrender1 libxext6 libfontconfig1 libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖（先单独装 rdkit，再装其他）
COPY requirements-docker.txt ./
RUN pip install --no-cache-dir rdkit>=2023.9.0 \
    && pip install --no-cache-dir fastapi==0.115.0 uvicorn==0.30.6 gunicorn==23.0.0 \
    pydantic==2.9.2 python-docx==1.1.2 python-multipart==0.0.12 httpx==0.27.2 'openai>=1.50.0'

# 复制后端代码 (cache bust: 2026-08-19-v10)
COPY backend/ ./backend/
COPY runtime.txt ./

# 复制前端构建产物
COPY --from=frontend-builder /app/frontend/dist/ ./frontend/dist/

# 设置工作目录
WORKDIR /app/backend

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]