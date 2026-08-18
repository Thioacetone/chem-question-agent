# -*- coding: utf-8 -*-
"""清理路线库：移除9步和10步的路线"""
import json5
import re
import os

path = os.path.join(os.path.dirname(__file__), "..", "frontend", "src", "data", "routeLibrary.js")
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

# 过滤：只保留7-8步
filtered = [r for r in routes if len(r["steps"]) <= 8]
print(f"过滤后: {len(filtered)} 条 (去掉 {len(routes)-len(filtered)} 条)")

# 重新编号
for i, r in enumerate(filtered):
    r["id"] = i + 1

# 重建JS文件
output_lines = []
for i, r in enumerate(filtered):
    output_lines.append("  {")
    output_lines.append(f'    id: {r["id"]},')
    output_lines.append(f'    title: "{r["title"]}",')
    desc = r.get("desc", "").replace('"', '\\"')
    output_lines.append(f'    desc: "{desc}",')
    output_lines.append("    steps: [")
    for j, s in enumerate(r["steps"]):
        comma = "," if j < len(r["steps"]) - 1 else ""
        reactant = s["reactant"].replace('"', '\\"')
        reagent = s["reagent"].replace('"', '\\"')
        product = s["product"].replace('"', '\\"')
        rtype = s.get("reaction_type", "").replace('"', '\\"')
        output_lines.append(f'      {{ step_number: {s["step_number"]}, reactant: "{reactant}", reagent: "{reagent}", product: "{product}", reaction_type: "{rtype}" }}{comma}')
    output_lines.append("    ]")
    comma = "," if i < len(filtered) - 1 else ""
    output_lines.append(f"  }}{comma}")

new_js = "const ROUTE_LIBRARY = [\n" + "\n".join(output_lines) + "\n];\n\nexport default ROUTE_LIBRARY;\n"

with open(path, "w", encoding="utf-8") as f:
    f.write(new_js)

print("路线库已更新")