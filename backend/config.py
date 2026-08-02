"""
配置文件 - DeepSeek API 设置和应用参数
"""
import os
from pathlib import Path

# 尝试加载 .env 文件
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                if key.strip() and key.strip() not in os.environ:
                    os.environ[key.strip()] = value.strip()

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"  # 使用精简提示词+chat模型，速度快且质量可控

# 豆包（火山引擎）视觉模型 API 配置
DOUBAO_API_KEY = os.getenv("DOUBAO_API_KEY", "")
DOUBAO_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"
DOUBAO_ENDPOINT_ID = os.getenv("DOUBAO_ENDPOINT_ID", "")  # 推理接入点ID
DOUBAO_VISION_MODEL = os.getenv("DOUBAO_VISION_MODEL", "doubao-1.5-vision-32k")

# MolScribe 模型路径
MOLSCRIBE_MODEL_PATH = os.getenv("MOLSCRIBE_MODEL_PATH", "")

# 命题生成参数
MAX_REACTION_STEPS = 8
MIN_REACTION_STEPS = 2
DEFAULT_DIFFICULTY = 0.55  # 默认难度系数 0.3-0.8

# 考试规范
TOTAL_SCORE = 15  # 江苏高考有机大题满分15分
QUESTION_COUNT_RANGE = (5, 5)  # 固定5小题