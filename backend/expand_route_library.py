# -*- coding: utf-8 -*-
"""
扩增路线库 v2: 简化提示词，分批生成3条/批
"""
import json, os, re, time, random

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

client = OpenAI(api_key=os.environ.get("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")

route_lib_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "src", "data", "routeLibrary.js")
with open(route_lib_path, "r", encoding="utf-8") as f:
    js = f.read()

start = js.find("const ROUTE_LIBRARY = [")
start = js.find("[", start)
export_pos = js.find("export default", start)
end = js.rfind("]", start, export_pos)
json_str = js[start:end+1]
json_str = re.sub(r"//[^\n]*\n", "\n", json_str)
json_str = re.sub(r"/\*.*?\*/", "", json_str, flags=re.DOTALL)
existing = json5.loads(json_str)

existing_titles = set(r["title"] for r in existing)
existing_products = set(r["steps"][-1]["product"] for r in existing)

STARTING = ["苯","甲苯","苯酚","苯胺","苯甲醛","苯甲酸","硝基苯","间二甲苯","对二甲苯","邻二甲苯",
            "萘","吡啶","呋喃","噻吩","环己醇","环己酮","乙酸","乙醇","丙二酸二乙酯",
            "乙酰乙酸乙酯","苯乙烯","苯乙酮","氯苯","溴苯","水杨酸","对硝基甲苯","乙酸乙酯","丙酸","丙烯腈","丙烯酸甲酯"]

TARGET = 200
NEED = TARGET - len(existing)
BATCH = 3
new_routes = []
print(f"现有 {len(existing)} 条，需生成 {NEED} 条")

# 示例路线（简化）
SAMPLE = """[
{"title":"对硝基苯甲酸合成路线","desc":"甲苯 → 对硝基苯甲酸（7步），氧化→硝化→还原→重氮化→氰基化→水解→酯化→水解，染料中间体","steps":[
{"step_number":1,"reactant":"甲苯","reagent":"KMnO₄, H⁺, △","product":"苯甲酸","reaction_type":"氧化反应"},
{"step_number":2,"reactant":"苯甲酸","reagent":"浓HNO₃, 浓H₂SO₄, △","product":"间硝基苯甲酸","reaction_type":"硝化反应"},
{"step_number":3,"reactant":"间硝基苯甲酸","reagent":"Fe, HCl, △","product":"间氨基苯甲酸","reaction_type":"还原反应"},
{"step_number":4,"reactant":"间氨基苯甲酸","reagent":"NaNO₂, HCl, 0-5°C","product":"间重氮苯甲酸盐","reaction_type":"重氮化反应"},
{"step_number":5,"reactant":"间重氮苯甲酸盐","reagent":"CuCN, △","product":"间氰基苯甲酸","reaction_type":"取代反应"},
{"step_number":6,"reactant":"间氰基苯甲酸","reagent":"C₂H₅OH, 浓H₂SO₄, △","product":"间氰基苯甲酸乙酯","reaction_type":"酯化反应"},
{"step_number":7,"reactant":"间氰基苯甲酸乙酯","reagent":"NaOH, H₂O, △ 然后 H⁺","product":"间羧基苯甲酸","reaction_type":"水解反应"}]}]"""

for batch_idx in range(0, NEED, BATCH):
    bs = min(BATCH, NEED - len(new_routes))
    if bs <= 0:
        break
    print(f"\n批次 {batch_idx//BATCH + 1} ({bs}条)...")

    sm = random.sample(STARTING, 5)
    sm_str = "、".join(sm)

    prompt = f"""生成{bs}条高中化学有机合成路线，每条7步。输出JSON数组。

格式示例：
{SAMPLE}

约束：
- 每条恰好7步，step_number 1-7
- 起始原料从以下选：{sm_str}
- 试剂必须具体（含浓度、温度）
- 前后产物连贯一致
- 标题格式"XXX合成路线"
- 只输出JSON数组，不含markdown"""

    for attempt in range(3):
        try:
            resp = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "只输出JSON数组，不要解释。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.85,
                max_tokens=8192,
            )
            content = resp.choices[0].message.content.strip()
            content = re.sub(r"^```\w*\n?", "", content)
            content = re.sub(r"\n?```$", "", content)

            try:
                routes = json5.loads(content)
            except:
                m = re.search(r"\[.*\]", content, re.DOTALL)
                if m:
                    routes = json5.loads(m.group(0))
                else:
                    print(f"  无法解析JSON")
                    continue

            if isinstance(routes, dict):
                routes = [routes]

            added = 0
            for r in routes:
                steps = r.get("steps", [])
                if len(steps) != 7:
                    continue
                title = r.get("title", "")
                if title in existing_titles:
                    continue
                product = steps[-1]["product"]
                if product in existing_products:
                    continue
                # 验证字段完整性
                ok = True
                for s in steps:
                    if not all(k in s for k in ["step_number","reactant","reagent","product","reaction_type"]):
                        ok = False
                        break
                if not ok:
                    continue
                # 连贯性
                for i in range(len(steps) - 1):
                    if steps[i]["product"] != steps[i+1]["reactant"]:
                        ok = False
                        break
                if not ok:
                    continue

                r["id"] = len(existing) + len(new_routes) + 1
                existing_titles.add(title)
                existing_products.add(product)
                new_routes.append(r)
                added += 1
                print(f"  ✅ {title}")

            if added > 0:
                break
            else:
                print(f"  无有效路线，重试{attempt+1}...")

        except Exception as e:
            print(f"  ❌ 尝试{attempt+1}: {e}")
            time.sleep(2)

    time.sleep(1.5)

# 补齐
while len(new_routes) < NEED:
    bs = min(BATCH, NEED - len(new_routes))
    print(f"\n补充 {bs}条...")
    sm = random.sample(STARTING, 5)
    sm_str = "、".join(sm)

    prompt = f"""生成{bs}条高中化学有机合成路线，每条7步。输出JSON数组。起始原料：{sm_str}。格式：[{{"title":"XXX合成路线","desc":"...","steps":[{{"step_number":1,"reactant":"原料","reagent":"条件","product":"产物","reaction_type":"类型"}},...]}}]"""

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "system", "content": "只输出JSON数组。"}, {"role": "user", "content": prompt}],
            temperature=0.9, max_tokens=8192,
        )
        content = resp.choices[0].message.content.strip()
        content = re.sub(r"^```\w*\n?", "", content)
        content = re.sub(r"\n?```$", "", content)
        try:
            routes = json5.loads(content)
        except:
            m = re.search(r"\[.*\]", content, re.DOTALL)
            if m: routes = json5.loads(m.group(0))
            else: continue
        if isinstance(routes, dict): routes = [routes]
        for r in routes:
            steps = r.get("steps", [])
            if len(steps) != 7: continue
            title = r.get("title", "")
            if title in existing_titles: continue
            product = steps[-1]["product"]
            if product in existing_products: continue
            ok = all(all(k in s for k in ["step_number","reactant","reagent","product","reaction_type"]) for s in steps)
            if not ok: continue
            for i in range(len(steps)-1):
                if steps[i]["product"] != steps[i+1]["reactant"]: ok = False; break
            if not ok: continue
            r["id"] = len(existing) + len(new_routes) + 1
            existing_titles.add(title)
            existing_products.add(product)
            new_routes.append(r)
            print(f"  ✅ {title}")
    except Exception as e:
        print(f"  ❌ {e}")
    time.sleep(2)

total = len(existing) + len(new_routes)
print(f"\n总计: {total} 条")

# 合并
all_routes = existing + new_routes
for i, r in enumerate(all_routes):
    r["id"] = i + 1

# 保存JSON备份
output_path = os.path.join(os.path.dirname(__file__), "expanded_routes.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(all_routes, f, ensure_ascii=False, indent=2)

# 重建JS
lines = []
for i, r in enumerate(all_routes):
    lines.append("  {")
    lines.append(f'    id: {r["id"]},')
    lines.append(f'    title: "{r["title"]}",')
    desc = r.get("desc","").replace('"','\\"').replace('\n',' ')
    lines.append(f'    desc: "{desc}",')
    lines.append("    steps: [")
    for j, s in enumerate(r["steps"]):
        comma = "," if j < len(r["steps"])-1 else ""
        reactant = s["reactant"].replace('"','\\"')
        reagent = s["reagent"].replace('"','\\"')
        product = s["product"].replace('"','\\"')
        rtype = s.get("reaction_type","").replace('"','\\"')
        lines.append(f'      {{ step_number: {s["step_number"]}, reactant: "{reactant}", reagent: "{reagent}", product: "{product}", reaction_type: "{rtype}" }}{comma}')
    lines.append("    ]")
    comma = "," if i < len(all_routes)-1 else ""
    lines.append(f"  }}{comma}")

new_js = "const ROUTE_LIBRARY = [\n" + "\n".join(lines) + "\n];\n\nexport default ROUTE_LIBRARY;\n"
with open(route_lib_path, "w", encoding="utf-8") as f:
    f.write(new_js)
print(f"路线库已更新: {len(all_routes)} 条")