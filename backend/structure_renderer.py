        def _split_reagent(text):
            """分行试剂文本，支持：
            - (1)试剂A (2)试剂B: (1)在箭头上方，(2)在箭头下方
            - (1)试剂A (2)试剂B (3)试剂C: (1)在上方，(2)(3)在下方
            - "然后"分隔：前部分在上，后部分在下
            返回 {"above": [...], "below": [...]}"""
            import re
            # === 检测"然后"分隔：前→箭头上方，后→箭头下方 ===
            if '然后' in text:
                parts = text.split('然后', 1)
                # 清洗前部分：去掉"第一步""第1步"等前缀，统一加(1)序号
                before = re.sub(r'第[一二三1-9]步[：:]*\s*', '', parts[0]).strip()
                before = re.sub(r'^\(\d+\)\s*', '', before).strip()  # 去掉已有的(1)序号避免重复
                # 清洗后部分：去掉"第二步""第2步"等前缀，统一加(2)序号
                after = re.sub(r'第[一二三1-9]步[：:]*\s*', '', parts[1]).strip()
                after = re.sub(r'^\(\d+\)\s*', '', after).strip()
                above = [f"(1) {before}"] if before else [text]
                below = [f"(2) {after}"] if after else []
                return {"above": above, "below": below}
            # 匹配 (1)xxx (2)xxx (3)xxx 格式的编号步骤
            # 规则：(1)在箭头上方，(2)和(3)在箭头下方
            numbered = re.findall(r'(?:\(\d+\)|\d+\))\s*[^()]+?(?=(?:\(\d+\)|\d+\))|$)', text)
            if len(numbered) >= 2:
                above = [numbered[0].strip()]           # (1) → 上方
                below = [s.strip() for s in numbered[1:]]  # (2)(3) → 下方
                return {"above": above, "below": below}
            # 分号分隔的多步反应
            parts = [p.strip() for p in text.replace('；', ';').split(';') if p.strip()]
            if len(parts) >= 2:
                return {"above": parts[:2], "below": []}
            # 单步条件：不拆分逗号（如 "浓HNO₃, 浓H₂SO₄, △" 应保持一行）
            return {"above": [text], "below": []}
