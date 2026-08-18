# -*- coding: utf-8 -*-
"""修复生成题目中的问题"""
import json
import re
import os

path = os.path.join(os.path.dirname(__file__), "structure_inference_questions.json")
with open(path, "r", encoding="utf-8") as f:
    questions = json.load(f)

for i, q in enumerate(questions):
    q.pop("_warnings", None)
    for a in q.get("answers", []):
        content = a.get("content", "")
        # 清理LLM推理过程（答案过长且含推理关键词）
        if len(content) > 800 and any(kw in content for kw in ["鉴于", "实际上", "不，", "干脆", "算了"]):
            # 提取最后的路线部分
            lines = content.split("\n")
            route_lines = []
            for line in lines:
                line = line.strip()
                if "→" in line and re.search(r"[A-Za-z\u4e00-\u9fff]", line):
                    route_lines.append(line)
            if route_lines:
                a["content"] = "\n".join(route_lines[-7:])
            else:
                a["content"] = "（答案待补充）"
            print(f"题目{i+1} 答案{a['number']} 已清理")

    # 修复隐藏结构
    hidden = q.get("hidden_structure")
    if not hidden or hidden in ("null", "None"):
        questions_list = q.get("questions", [])
        if len(questions_list) > 1:
            q2 = questions_list[1].get("content", "")
            m = re.search(r"([A-Z])的", q2)
            if m:
                q["hidden_structure"] = m.group(1)
                print(f"题目{i+1} hidden_structure -> {m.group(1)}")

    # 补齐缺失答案
    answers = q.get("answers", [])
    questions_list = q.get("questions", [])
    while len(answers) < len(questions_list):
        answers.append({"number": len(answers) + 1, "content": "（答案待补充）"})
        print(f"题目{i+1} 补充答案{len(answers)}")

    # 清理答案和解析中的已知信息
    for a in answers:
        content = a.get("content", "")
        if "已知" in content:
            a["content"] = re.sub(r"已知[：:][^。；]+[。；]?\s*", "", content)
            print(f"题目{i+1} 答案{a['number']} 清理已知信息")
    analysis = q.get("analysis", "")
    if "已知" in analysis:
        analysis = re.sub(r"第\(5\)题\S*?运用已知信息\S*?[，。]", "", analysis)
        analysis = re.sub(r"第\(5\)题\S*?利用已知\S*?[，。]", "", analysis)
        analysis = re.sub(r"考查\S*?已知信息\S*?[，。]", "", analysis)
        analysis = re.sub(r"利用已知的\S*?[，。]", "", analysis)
        q["analysis"] = analysis
        print(f"题目{i+1} 解析清理已知信息")

with open(path, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)
print("所有修复完成")