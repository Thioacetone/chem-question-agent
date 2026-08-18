# -*- coding: utf-8 -*-
"""补齐路线库到200条"""
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

STARTING = ["苯","甲苯","苯酚","苯胺","苯甲醛","苯甲酸","硝基苯","间二甲苯","对二甲苯","邻二甲苯","萘","吡啶","呋喃","噻吩","环己醇","环己酮","乙酸","乙醇","丙二酸二乙酯","乙酰乙酸乙酯","苯乙烯","苯乙酮","氯苯","溴苯","水杨酸","对硝基甲苯","乙酸乙酯","丙酸","丙烯腈","丙烯酸甲酯"]

current = len(existing)
target = 200
need = target - current
new_routes = []
print(f"当前 {current} 条，需补齐 {need} 条")

while len(new_routes) < need:
    bs = min(3, need - len(new_routes))
    sm = random.sample(STARTING, 5)
    sm_str = "、".join(sm)
    print(f"生成 {bs} 条...")

    prompt = f'生成{bs}条高中化学有机合成路线，每条7步。输出JSON数组。起始原料：{sm_str}。格式：[{{"title":"XXX合成路线","desc":"...","steps":[{{"step_number":1,"reactant":"原料","reagent":"条件","product":"产物","reaction_type":"类型"}},...]}}]'

    try:
        resp = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role":"system","content":"只输出JSON数组。"},{"role":"user","content":prompt}],
            temperature=0.9, max_tokens=8192,
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
                continue
        if isinstance(routes, dict):
            routes = [routes]
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
            ok = all(all(k in s for k in ["step_number","reactant","reagent","product","reaction_type"]) for s in steps)
            if not ok:
                continue
            for i in range(len(steps)-1):
                if steps[i]["product"] != steps[i+1]["reactant"]:
                    ok = False
                    break
            if not ok:
                continue
            r["id"] = current + len(new_routes) + 1
            existing_titles.add(title)
            existing_products.add(product)
            new_routes.append(r)
            print(f"  ✅ {title}")
    except Exception as e:
        print(f"  ❌ {e}")
    time.sleep(2)

print(f"新增: {len(new_routes)} 条")

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
    desc = r.get("desc","").replace('"', '\\"').replace('\n', ' ')
    lines.append(f'    desc: "{desc}",')
    lines.append("    steps: [")
    for j, s in enumerate(r["steps"]):
        comma = "," if j < len(r["steps"])-1 else ""
        reactant = s["reactant"].replace('"', '\\"')
        reagent = s["reagent"].replace('"', '\\"')
        product = s["product"].replace('"', '\\"')
        rtype = s.get("reaction_type","").replace('"', '\\"')
        lines.append(f'      {{ step_number: {s["step_number"]}, reactant: "{reactant}", reagent: "{reagent}", product: "{product}", reaction_type: "{rtype}" }}{comma}')
    lines.append("    ]")
    comma = "," if i < len(all_routes)-1 else ""
    lines.append(f"  }}{comma}")

new_js = "const ROUTE_LIBRARY = [\n" + "\n".join(lines) + "\n];\n\nexport default ROUTE_LIBRARY;\n"
with open(route_lib_path, "w", encoding="utf-8") as f:
    f.write(new_js)
print(f"总计: {len(all_routes)} 条")