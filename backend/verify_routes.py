# -*- coding: utf-8 -*-
"""验证路线库质量"""
import json5, re, os, random
from collections import Counter

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

print(f"总路线: {len(routes)}")

# 步数分布
step_counts = Counter(len(r["steps"]) for r in routes)
print(f"步数分布: {dict(sorted(step_counts.items()))}")

# 标题重复
titles = [r["title"] for r in routes]
title_counts = Counter(titles)
dups = {k: v for k, v in title_counts.items() if v > 1}
print(f"标题重复: {len(dups)}个" if dups else "无标题重复")

# ID连续性
ids = sorted(r["id"] for r in routes)
expected = list(range(1, len(routes) + 1))
id_ok = ids == expected
print(f"ID连续: {'✅' if id_ok else '❌ 不连续'}")

# 产物重复
products = [r["steps"][-1]["product"] for r in routes]
prod_counts = Counter(products)
prod_dups = {k: v for k, v in prod_counts.items() if v > 1}
print(f"产物重复: {len(prod_dups)}个")

# 抽样检查连贯性
issues = 0
for r in routes:
    for i in range(len(r["steps"]) - 1):
        if r["steps"][i]["product"] != r["steps"][i + 1]["reactant"]:
            issues += 1
            if issues <= 5:
                print(f"❌ 不连贯: {r['title']} 步骤{i+1}->{i+2}")
print(f"连贯性: {'✅ 全部通过' if issues == 0 else f'❌ {issues}个问题'}")

# 抽样检查
for idx in random.sample(range(len(routes)), min(2, len(routes))):
    r = routes[idx]
    print(f"\n路线{idx+1}: {r['title']}")
    for s in r["steps"]:
        print(f"  {s['step_number']}. {s['reactant']} ->[{s['reagent']}] {s['product']}")

print(f"\n✅ 验证完成")