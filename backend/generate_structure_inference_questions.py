# -*- coding: utf-8 -*-
"""
批量生成结构简式推断题
从路线库中精选路线，调用 DeepSeek API 生成命题，强制第(2)题为结构推断
"""
import json
import os
import sys
import time
import re
import random

# 加载 .env
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()

from openai import OpenAI
import json5

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# 加载路线库
route_lib_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "src", "data", "routeLibrary.js")
with open(route_lib_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# 提取 JSON 数组
start = js_content.find("const ROUTE_LIBRARY = [")
if start == -1:
    print("无法找到 ROUTE_LIBRARY")
    sys.exit(1)
start = js_content.find("[", start)
export_pos = js_content.find("export default", start)
if export_pos == -1:
    export_pos = js_content.find("export {", start)
if export_pos == -1:
    print("无法找到 export 语句")
    sys.exit(1)
end = js_content.rfind("]", start, export_pos)
if end == -1:
    print("无法找到数组结束")
    sys.exit(1)
json_str = js_content[start:end+1]

# 清理 JS 中的注释
json_str = re.sub(r'//[^\n]*\n', '\n', json_str)
json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)

routes = json5.loads(json_str)
print(f"加载了 {len(routes)} 条路线")

# 精选适合结构推断的路线（步数适中、中间产物有意义）
selected_routes = []
for r in routes:
    steps = r.get("steps", [])
    n = len(steps)
    if 7 <= n <= 10:
        if n - 2 >= 3:
            selected_routes.append(r)

print(f"精选了 {len(selected_routes)} 条适合的路线")

# 随机打乱，确保多样性
random.shuffle(selected_routes)

# 已知信息反应类型库（确保多样性）
KNOWN_REACTION_TYPES = [
    "Wittig反应（醛酮→烯烃）",
    "Knoevenagel缩合（醛+活泼亚甲基→α,β-不饱和化合物）",
    "羟醛缩合Aldol（醛+醛→α,β-不饱和醛）",
    "Perkin反应（芳醛+酸酐→肉桂酸类）",
    "Claisen缩合（酯+酯→β-酮酸酯）",
    "Gabriel胺合成（邻苯二甲酰亚胺→伯胺）",
    "Clemmensen还原（羰基→亚甲基，Zn-Hg/HCl）",
    "Wolff-Kishner还原（羰基→亚甲基，NH₂NH₂/KOH）",
    "HVZ反应（羧酸α-卤代）",
    "Hofmann降解（酰胺→少一个碳的胺）",
    "黄鸣龙还原（羰基→亚甲基，改性Wolff-Kishner）",
    "格式试剂+CO₂（格式试剂→羧酸）",
    "格式试剂+醛酮（格式试剂→醇）",
    "苯炔中间体（卤代苯+强碱→苯炔→取代产物）",
    "Diels-Alder反应（双烯+亲双烯体→六元环）",
]

# 已使用的反应类型追踪
used_reaction_types = set()

# 生成参数
MAX_QUESTIONS = 20
all_questions = []
success_count = 0
fail_count = 0

# 已使用的hidden_structure追踪
used_hidden = set()

for i, route in enumerate(selected_routes[:MAX_QUESTIONS]):
    print(f"\n[{i+1}/{MAX_QUESTIONS}] 路线: {route['title']}")
    steps = route["steps"]
    n = len(steps)

    # 随机选择hidden_structure（B到倒数第二个产物，避免总是D）
    # 可选的中间产物代号: B, C, D, E, F, G, H, I
    possible_hidden = []
    for s in steps[1:-1]:  # 排除第一个(A)和最后一个(最终产物)
        step_num = s["step_number"]
        # 代号映射：step_number=1是A→B，所以产物是A+step_number
        # B = chr(65 + 1) = 'B', C = chr(65 + 2) = 'C'
        label = chr(65 + step_num)  # step_number 1 -> B, 2 -> C, etc.
        possible_hidden.append(label)

    # 优先选择没用过的
    unused = [h for h in possible_hidden if h not in used_hidden]
    if unused:
        hidden_structure = random.choice(unused)
    else:
        hidden_structure = random.choice(possible_hidden)
    used_hidden.add(hidden_structure)

    # 随机选择已知信息反应类型
    unused_types = [t for t in KNOWN_REACTION_TYPES if t not in used_reaction_types]
    if len(unused_types) >= 3:
        chosen_type = random.choice(unused_types)
    elif unused_types:
        chosen_type = random.choice(unused_types)
    else:
        chosen_type = random.choice(KNOWN_REACTION_TYPES)
    used_reaction_types.add(chosen_type)

    # 构建路线描述
    route_text = f"路线：{route['title']}\n描述：{route.get('desc', '')}\n"
    route_text += f"步数：{n}步\n"
    route_text += "步骤：\n"
    for s in steps:
        route_text += f"  第{s['step_number']}步：{s['reactant']} →[{s['reagent']}] {s['product']}（{s.get('reaction_type', '')}）\n"

    # 构建生成提示词
    system_prompt = f"""你是一位高考化学命题专家。请根据以下合成路线，创作一道完整的江苏高考有机化学大题（15分制）。

=== 🔴 硬性约束（必须严格遵守） ===

【题干】
- 仅一句话，≤50字，只描述最终产物的实际应用意义（如"XX是治疗XX的药物"），以句号结尾
- 🔴 绝对禁止出现："合成路线如下""可通过以下路线合成""请根据以下合成路线""请完成下列合成路线""请设计其合成路线""请完成其合成路线"等任何与路线描述相关的表述
- 🔴 禁止出现箭头、反应式、结构式
- 正确示例："苯巴比妥是一种经典镇静催眠药物。" "己二酸是合成尼龙-66的重要单体。"

【第(2)题 - 结构简式推断】
- 必须问"{{hidden_structure}}的结构简式为____"
- hidden_structure = "{hidden_structure}"
- {hidden_structure}是路线中的中间产物，不是起始原料

【第(1)题 - 1分】
- 官能团识别/分子式/反应类型/手性碳判断，任选其一

【第(3)题 - 2分】
- 试剂与条件/反应类型/方程式书写

【第(4)题 - 3分，同分异构体】
- 🔴 必须包含至少3项条件：官能团特征反应（如银镜反应/FeCl₃显色/NaHCO₃反应等）、核磁共振氢谱特征（峰组数、峰面积比）、苯环取代位置/手性碳/对称性等结构限制

【第(5)题 - 5分，有机合成】
- 🔴 必须明确写出"制备化合物X"（含"制备"或"合成"关键词）
- 已知信息使用：{chosen_type}
- 🔴 已知信息只能出现在第(5)题设问中（以"已知："开头），不得在题干、其他小题设问、答案、解析中重复
- 🔴 答案合成路线必须5-7步，使用→[条件]格式
- 答案路线不能与题干路线完全重合

【全部答案】
- 🔴 每道题都必须有答案，不能遗漏任何一道
- 方程式使用→[条件]格式，条件写在箭头上方方括号内
- 化学结构式用{{{{结构式:SMILES}}}}占位符

=== 输出JSON格式 ===
{{
  "target_compound": "目标化合物及用途",
  "stem": "题干（仅一句话，≤50字，只描述实际应用，以句号结尾）",
  "hidden_structure": "{hidden_structure}",
  "questions": [
    {{"number": 1, "content": "第(1)题设问", "score": 1}},
    {{"number": 2, "content": "{hidden_structure}的结构简式为____", "score": 2}},
    {{"number": 3, "content": "第(3)题设问", "score": 2}},
    {{"number": 4, "content": "第(4)题设问（同分异构体，至少3项条件）", "score": 3}},
    {{"number": 5, "content": "第(5)题设问（含'已知：...'和'制备化合物X'）", "score": 5}}
  ],
  "answers": [
    {{"number": 1, "content": "第(1)题完整答案"}},
    {{"number": 2, "content": "第(2)题答案（{hidden_structure}的结构简式）"}},
    {{"number": 3, "content": "第(3)题完整答案"}},
    {{"number": 4, "content": "第(4)题完整答案"}},
    {{"number": 5, "content": "第(5)题答案（5-7步合成路线，→[条件]格式，不含'已知：'）"}}
  ],
  "new_info": "第(5)题已知信息（含具体反应方程式）",
  "analysis": "试题解析（不含已知信息）"
}}

合成路线如下：
{route_text}
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一位高考化学命题专家。请严格按照要求生成题目。输出纯JSON，不要包含任何markdown标记。所有答案必须完整，不能遗漏。"},
                {"role": "user", "content": system_prompt}
            ],
            temperature=0.7,
            max_tokens=4096,
        )

        content = response.choices[0].message.content
        # 清理可能的 markdown 包裹
        content = content.strip()
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

        question_data = json.loads(content)
        question_data["route_id"] = route["id"]
        question_data["route_title"] = route["title"]
        question_data["route_steps"] = n

        # ===== 验证 =====
        issues = []
        stem = question_data.get("stem", "")

        # 1. 题干检查
        forbidden_phrases = ["合成路线如下", "可通过以下路线合成", "请根据以下合成路线",
                            "请完成下列合成路线", "请设计其合成路线", "请完成其合成路线",
                            "请根据合成路线", "路线如下", "合成路线"]
        for phrase in forbidden_phrases:
            if phrase in stem:
                issues.append(f"题干含禁止短语: '{phrase}'")

        if len(stem) > 60:
            issues.append(f"题干超长({len(stem)}字)")

        # 2. hidden_structure 检查
        hidden = question_data.get("hidden_structure")
        if not hidden or hidden == "null" or hidden == "None":
            issues.append("hidden_structure未设置")
        elif not re.match(r'^[A-Z]$', hidden):
            issues.append(f"hidden_structure格式无效: {hidden}")
        elif hidden == "A":
            issues.append("不能隐藏起始原料A")

        # 3. 第(2)题检查
        questions = question_data.get("questions", [])
        if len(questions) >= 2:
            q2_content = questions[1].get("content", "")
            if hidden and hidden not in q2_content:
                issues.append(f"第(2)题设问中未提及{hidden}")

        # 4. 第(5)题检查
        if len(questions) >= 5:
            q5_content = questions[4].get("content", "")
            if "制备" not in q5_content and "合成" not in q5_content:
                issues.append("第(5)题设问缺少'制备'或'合成'关键词")

        # 5. 答案完整性检查
        answers = question_data.get("answers", [])
        if len(answers) < 5:
            issues.append(f"答案不完整，只有{len(answers)}道")

        # 6. 第(5)题答案检查
        if len(answers) >= 5:
            a5 = answers[4].get("content", "")
            if "已知" in a5:
                issues.append("第(5)题答案含'已知'信息，已知信息只应在设问中出现")

        # 7. 解析检查
        analysis = question_data.get("analysis", "")
        if "已知" in analysis:
            issues.append("解析中不应重复已知信息")

        if issues:
            print(f"  ⚠️ 问题:")
            for iss in issues:
                print(f"    - {iss}")
            # 仍然保存，但标记
            question_data["_warnings"] = issues
            all_questions.append(question_data)
            success_count += 1
            print(f"  ✅ 已保存（有{len(issues)}个警告）")
        else:
            all_questions.append(question_data)
            success_count += 1
            print(f"  ✅ 完美通过")

        print(f"  hidden_structure: {hidden}")
        print(f"  题干: {stem[:50]}...")

    except Exception as e:
        fail_count += 1
        print(f"  ❌ 生成失败: {e}")

    # 避免限流
    time.sleep(2)

# 保存结果
output_path = os.path.join(os.path.dirname(__file__), "structure_inference_questions.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_questions, f, ensure_ascii=False, indent=2)

print(f"\n{'='*50}")
print(f"生成完成！成功: {success_count}, 失败: {fail_count}")
print(f"结果保存至: {output_path}")

# 统计
hidden_stats = {}
for q in all_questions:
    h = q.get("hidden_structure", "?")
    hidden_stats[h] = hidden_stats.get(h, 0) + 1
print(f"hidden_structure分布: {hidden_stats}")

warnings_count = sum(1 for q in all_questions if q.get("_warnings"))
print(f"有警告的题目: {warnings_count}/{len(all_questions)}")