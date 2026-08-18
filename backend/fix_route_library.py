# -*- coding: utf-8 -*-
"""修复路线库：去重、修复连贯性"""
import json5, re, os, json

path = os.path.join("frontend", "src", "data", "routeLibrary.js")
with open(path, "r", encoding="utf-8") as f:
    js = f.read()
start = js.find("const ROUTE_LIBRARY = [")
start = js.find("[", start)
export_pos = js.find("export default", start)
end = js.rfind("]", start, export_pos)
json_str = js[start:end+1]
json_str = re.sub(r"//[^\n]*\n", "\n", json_str)
json_str = re.sub(r"/\*.*?\*/", "", json_str, flags=re.DOTALL)
routes = json5.loads(json_str)

print(f"原始: {len(routes)} 条")

# 1. 去重标题
seen_titles = {}
deduped = []
for r in routes:
    title = r["title"]
    if title in seen_titles:
        print(f"  去重标题: {title}")
        continue
    seen_titles[title] = True
    deduped.append(r)
routes = deduped
print(f"去重标题后: {len(routes)} 条")

# 2. 去重产物
seen_products = {}
deduped = []
for r in routes:
    product = r["steps"][-1]["product"]
    if product in seen_products:
        print(f"  去重产物: {product} ({r['title']})")
        continue
    seen_products[product] = True
    deduped.append(r)
routes = deduped
print(f"去重产物后: {len(routes)} 条")

# 3. 修复连贯性问题 - 移除不连贯的路线
coherent = []
removed = []
for r in routes:
    ok = True
    for i in range(len(r["steps"]) - 1):
        if r["steps"][i]["product"] != r["steps"][i + 1]["reactant"]:
            ok = False
            break
    if ok:
        coherent.append(r)
    else:
        removed.append(r["title"])
        print(f"  移除不连贯: {r['title']}")

routes = coherent
print(f"修复连贯性后: {len(routes)} 条")

# 重新编号
for i, r in enumerate(routes):
    r["id"] = i + 1

# 保存
# 重建JS
lines = []
for i, r in enumerate(routes):
    lines.append("  {")
    lines.append(f'    id: {r["id"]},')
    lines.append(f'    title: "{r["title"]}",')
    desc = r.get("desc", "").replace('"', '\\"').replace('\n', ' ')
    lines.append(f'    desc: "{desc}",')
    lines.append("    steps: [")
    for j, s in enumerate(r["steps"]):
        comma = "," if j < len(r["steps"]) - 1 else ""
        reactant = s["reactant"].replace('"', '\\"')
        reagent = s["reagent"].replace('"', '\\"')
        product = s["product"].replace('"', '\\"')
        rtype = s.get("reaction_type", "").replace('"', '\\"')
        lines.append(f'      {{ step_number: {s["step_number"]}, reactant: "{reactant}", reagent: "{reagent}", product: "{product}", reaction_type: "{rtype}" }}{comma}')
    lines.append("    ]")
    comma = "," if i < len(routes) - 1 else ""
    lines.append(f"  }}{comma}")

new_js = "const ROUTE_LIBRARY = [\n" + "\n".join(lines) + "\n];\n\nexport default ROUTE_LIBRARY;\n"
with open(path, "w", encoding="utf-8") as f:
    f.write(new_js)

# 保存JSON备份
output_path = os.path.join(os.path.dirname(__file__), "expanded_routes.json")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(routes, f, ensure_ascii=False, indent=2)

print(f"\n最终: {len(routes)} 条路线")
print(f"移除: {removed}")