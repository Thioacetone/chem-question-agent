"""
命题生成引擎 v4.0 - 命题思维驱动的原创命题
核心理念：理解命题逻辑 → 形成独特风格 → 创造原创好题
"""
import json
import re
from typing import Optional
from knowledge_base import (
    HIGH_SCHOOL_REACTIONS, REACTION_TYPES, QUESTION_TEMPLATES,
    SCORING_GUIDELINES, TARGET_IDENTITIES, KNOWN_INFO_TEMPLATES,
    ISOMER_CONDITIONS, DIFFICULTY_PROGRESSION, PROMPT_STYLE_KEYWORDS,
)
from llm_client import llm_client
from config import (
    MAX_REACTION_STEPS, MIN_REACTION_STEPS, DEFAULT_DIFFICULTY,
    TOTAL_SCORE, QUESTION_COUNT_RANGE,
)


class QuestionGenerator:
    """命题生成引擎 v4.0"""

    def __init__(self):
        self.llm = llm_client

    def build_context_prompt(self, route_data: dict) -> str:
        """
        构建命题上下文 v5.0 — 精简聚焦，提供路线相关的知识参考
        """
        import random

        # 提取反应类型
        reaction_types_in_route = set()
        for step in route_data.get("steps", []):
            if "reaction_type" in step:
                reaction_types_in_route.add(step["reaction_type"])

        # 构建相关反应知识（只选取最相关的几个）
        relevant_reactions = []
        for rxn in HIGH_SCHOOL_REACTIONS:
            if rxn["type"] in reaction_types_in_route or rxn["category"] in str(route_data):
                relevant_reactions.append(
                    f"- {rxn['name']}：{rxn['template']}"
                )

        # 随机选择用途身份
        identity = random.choice(TARGET_IDENTITIES)

        context = f"""【用户输入的合成路线】
{json.dumps(route_data, ensure_ascii=False, indent=2)}

【建议的目标化合物用途身份】
{identity}

【路线中涉及的反应类型】
{', '.join(reaction_types_in_route) if reaction_types_in_route else '未指定'}

【相关高中反应参考】
{chr(10).join(relevant_reactions[:8])}

【重要提醒】
第(5)题合成路线答案必须恰好5-7步，不能少于5步，也不能多于7步。这是硬性要求！
🔴 单步路线（仅1步反应）绝对禁止！必须设计5-7步的完整合成路线。
请基于以上合成路线，创作一道有机化学大题。命题要求已在系统提示中详细说明，请严格遵守。"""
        return context

    def generate_from_route(self, route_data: dict, difficulty: float = DEFAULT_DIFFICULTY) -> dict:
        """
        从合成路线生成完整命题 v3.0

        Args:
            route_data: 合成路线数据
            difficulty: 难度系数 0.3-0.8

        Returns:
            完整的命题数据
        """
        # 验证输入
        steps = route_data.get("steps", [])
        if len(steps) < MIN_REACTION_STEPS:
            return {"error": f"合成路线至少需要{MIN_REACTION_STEPS}步反应"}
        if len(steps) > MAX_REACTION_STEPS:
            return {"error": f"合成路线最多{MAX_REACTION_STEPS}步反应"}

        # 构建上下文
        context = self.build_context_prompt(route_data)

        # 调用DeepSeek生成命题
        try:
            raw_response = self.llm.generate_question(context, difficulty)
            self._last_raw = raw_response
            question_data = self._parse_json_response(raw_response)
            question_data["raw_route"] = route_data
            question_data["generated_by"] = "DeepSeek-Chemistry-Agent-v3.0"

            # 检查答案是否包含 {{结构式:...}} 占位符和SMILES有效性
            # 步骤数问题是最高优先级，必须修复
            answers = question_data.get("answers", [])
            if isinstance(answers, list) and len(answers) > 0:
                # 先检查步骤数（最高优先级）
                wrong_steps = self._check_answer_step_count(answers)
                retry_count = 0
                max_retries = 3  # 提升到3次重试，确保步骤数问题被彻底修复
                
                while wrong_steps and retry_count < max_retries:
                    retry_count += 1
                    retry_response = self._retry_step_count(context, raw_response, wrong_steps, retry_count)
                    retry_data = self._parse_json_response(retry_response)
                    if retry_data and not retry_data.get("parse_error"):
                        if retry_data.get("answers"):
                            question_data["answers"] = retry_data["answers"]
                            answers = retry_data["answers"]
                        if retry_data.get("questions"):
                            question_data["questions"] = retry_data["questions"]
                        if retry_data.get("analysis"):
                            question_data["analysis"] = retry_data["analysis"]
                        raw_response = retry_response
                    wrong_steps = self._check_answer_step_count(answers)
                
                # 如果步骤数仍然不对，标记错误
                if wrong_steps:
                    question_data["_step_error"] = f"第5题答案步骤数({wrong_steps}步)不符合5-7步要求，已重试{max_retries}次仍无法修复"

                # 然后检查结构式占位符和SMILES
                missing = self._check_structure_placeholders(answers)
                invalid_smiles = self._validate_smiles_in_answers(answers)
                
                if missing or invalid_smiles:
                    issues = []
                    if missing:
                        issues.append(f"第{', '.join(str(n) for n in missing)}题答案缺少结构式占位符")
                    if invalid_smiles:
                        issues.append(f"以下SMILES无效: {', '.join(i['smiles'] for i in invalid_smiles)}")
                    
                    retry_response = self._retry_combined(context, raw_response, issues, invalid_smiles)
                    retry_data = self._parse_json_response(retry_response)
                    if retry_data and not retry_data.get("parse_error"):
                        if retry_data.get("answers"):
                            question_data["answers"] = retry_data["answers"]
                        if retry_data.get("questions"):
                            question_data["questions"] = retry_data["questions"]
                        if retry_data.get("analysis"):
                            question_data["analysis"] = retry_data["analysis"]

            # 后处理：清洗答案中的冗余条件表述
            question_data = self._clean_answer_conditions(question_data)

            # === 验证重试：基于validate_question结果自动修复错误 ===
            validation = self.validate_question(question_data)
            validation_retry_count = 0
            max_validation_retries = 2
            
            while validation.get("issues") and len(validation["issues"]) > 0 and validation_retry_count < max_validation_retries:
                validation_retry_count += 1
                retry_response = self._retry_validation_issues(
                    context, raw_response, validation["issues"], validation_retry_count
                )
                retry_data = self._parse_json_response(retry_response)
                if retry_data and not retry_data.get("parse_error"):
                    if retry_data.get("answers"):
                        question_data["answers"] = retry_data["answers"]
                    if retry_data.get("questions"):
                        question_data["questions"] = retry_data["questions"]
                    if retry_data.get("analysis"):
                        question_data["analysis"] = retry_data["analysis"]
                    if retry_data.get("stem"):
                        question_data["stem"] = retry_data["stem"]
                    if retry_data.get("new_info") is not None:
                        question_data["new_info"] = retry_data["new_info"]
                    raw_response = retry_response
                    # 再次清洗条件
                    question_data = self._clean_answer_conditions(question_data)
                validation = self.validate_question(question_data)
            
            # 如果仍有错误，记录到结果中
            if validation.get("issues") and len(validation["issues"]) > 0:
                question_data["_validation_issues"] = validation["issues"]
                question_data["_validation_retries"] = validation_retry_count

            return question_data
        except Exception as e:
            return {"error": f"命题生成失败: {str(e)}", "raw_response": getattr(self, '_last_raw', '')}

    def _check_structure_placeholders(self, answers: list) -> list:
        """检查哪些答案缺少 {结构式:...} 或 {{结构式:...}} 占位符"""
        import re
        missing = []
        for a in answers:
            content = a.get("content", "")
            number = a.get("number", "?")
            # 检查是否包含结构式占位符（支持单双大括号）
            has_placeholder = re.search(r'\{结构式:', content) is not None
            if not has_placeholder:
                # 检查是否确实需要结构式（涉及化合物结构描述的答案）
                needs_structure = any(kw in content for kw in [
                    "结构式", "结构简式", "结构简", "化合物", "合成路线",
                    "第1步", "第2步", "第3步", "第4步", "第5步", "第6步", "第7步",
                ])
                if needs_structure:
                    missing.append(number)
        return missing

    def _check_answer_step_count(self, answers: list) -> int:
        """检查第5题答案步骤数是否在5-7范围内，返回实际步骤数（不符合时），符合时返回0
        
        检测策略（双重兜底）：
        1. 优先匹配"第X步"格式（标准格式）
        2. 兜底：统计 →[条件] 箭头数量（防止LLM不用"第X步"格式写出1步路线）
        """
        for a in answers:
            if a.get("number") == 5 or a.get("number") == "5":
                content = a.get("content", "")
                # 策略1：匹配"第X步"或"步骤X"格式
                step_matches = re.findall(r'第(\d+)步|步骤(\d+)', content)
                step_count = len(step_matches)
                
                # 策略2：兜底——如果"第X步"格式匹配不到，统计箭头数量
                if step_count == 0:
                    # 统计 →[条件] 箭头数量（每个箭头代表一步反应）
                    arrow_count = len(re.findall(r'→\s*\[', content))
                    if arrow_count > 0:
                        # 箭头数量就是实际步骤数
                        step_count = arrow_count
                
                if step_count < 5 or step_count > 7:
                    return step_count
        return 0

    def _retry_validation_issues(self, context: str, previous_response: str, issues: list, retry_num: int) -> str:
        """专门重试：修复validate_question检测到的所有错误"""
        urgency = "🔴 这是最后一次修复机会！" if retry_num >= 2 else "🔴 请务必修复以下所有问题！"
        issues_text = "\n".join(f"  {i+1}. {issue}" for i, issue in enumerate(issues))
        
        retry_prompt = f"""【严重错误】你生成的命题存在以下问题，必须全部修复！

{urgency}

=== 原始合成路线数据 ===
{context}

=== 需要修复的问题 ===
{issues_text}

=== 修复指南 ===
- 第(1)题必须是基础识记题（官能团名称/反应类型/分子式），难度easy
- 第(2)题若含方程式，必须用路线图格式：{{{{结构式:SMILES}}}}→[条件] {{{{结构式:SMILES}}}}
- 第(3)题若含方程式，也必须用路线图格式
- 第(4)题必须是同分异构体题，含3个递进条件（①②③），难度hard
- 第(5)题必须是合成路线设计题，含"已知"信息，明确写"制备化合物X"，难度hard
- 分值严格按14分(2+2+2+3+5)或15分(2+2+3+3+5)分配
- 所有化学方程式必须用A→[条件]B格式，条件在箭头上方方括号内
- 条件中有(2)编号必须同时有(1)编号，不能只有(2)没有(1)
- 条件必须极简！只写试剂名+条件符号，逗号分隔，严禁冗余词
- 题干必须包含目标化合物的用途身份描述
- 已知信息必须包含{{{{结构式:SMILES}}}}占位符，格式与路线图一致
- 已知信息的反应不能与题干路线重复
- 同分异构体条件①必须含官能团特征反应，②必须含谱学特征，③必须含结构限制
- 第(5)题答案必须是5-7步，每步用→[条件]格式，条件在箭头上方
- 答案路线必须与题干路线不同

请修复以上所有问题，重新输出完整的JSON命题（包含所有字段：stem, questions, answers, analysis, new_info）。"""
        return self.llm.generate(
            system_prompt="你是一位高考化学命题专家。请严格按照要求修复命题中的所有错误。必须修复全部问题，一条都不能遗漏！",
            user_prompt=retry_prompt,
            temperature=0.2,
        )

    def _retry_combined(self, context: str, previous_response: str, issues: list, invalid_smiles: list) -> str:
        """合并重试：一次性修复结构式占位符缺失和SMILES无效问题"""
        issues_text = "\n".join(f"  - {i}" for i in issues)
        
        smiles_fix = ""
        if invalid_smiles:
            invalid_list = "\n".join(
                f"  第{i['number']}题: {{{{结构式:{i['smiles']}}}}}"
                for i in invalid_smiles
            )
            smiles_fix = f"""
=== SMILES书写规范（务必遵守） ===
- 苯环：c1ccccc1
- 单取代苯：取代基在1位，如甲苯 Cc1ccccc1
- 对位二取代苯：如对硝基甲苯 Cc1ccc(N(=O)=O)cc1
- 间位二取代苯：如间硝基甲苯 Cc1cccc(N(=O)=O)c1
- 邻位二取代苯：如邻硝基甲苯 Cc1ccccc1N(=O)=O
- 羧基：C(=O)O（不是COOH）
- 醛基：C=O
- 羟基：O（不是OH）
- 氨基：N（不是NH2）
- 硝基：N(=O)=O
- 氰基：C#N
- 酯基：C(=O)OC
- 酰胺基：C(=O)N
- 醚键：COC
- 双键：C=C
- 三键：C#C"""

        retry_prompt = f"""你刚才生成的命题有以下问题需要修复：

{issues_text}
{smiles_fix}

请修复以上所有问题，重新输出完整的JSON（包含所有字段）。"""
        return self.llm.generate(
            system_prompt="你是一位高考化学命题专家。请修复命题中的问题。",
            user_prompt=retry_prompt,
            temperature=0.1,
        )

    def _retry_step_count(self, context: str, previous_response: str, wrong_steps: int, retry_num: int) -> str:
        """专门重试：强制修复第5题答案步骤数问题"""
        urgency = "这是最后一次机会！" if retry_num >= 3 else "请务必修复！"
        
        if wrong_steps <= 1:
            problem = f"步骤数严重不足（仅{wrong_steps}步）！这是绝对不能接受的。你必须设计一条完整的5-7步合成路线。"
            fix_guide = """=== 如何从1步扩展到5-7步 ===
你不能只写1步反应！必须设计一条多步合成路线。例如：
- 起始原料经过官能团转化（如氧化、还原、卤代、硝化、酯化、水解、酰化等）逐步构建目标分子
- 每一步只做一个转化，不要合并多步反应
- 确保有5-7个独立的→[条件]箭头
- 示例：A→[条件1]B→[条件2]C→[条件3]D→[条件4]E→[条件5]F（这就是5步）"""
        elif wrong_steps < 5:
            problem = f"步骤数太少（仅{wrong_steps}步），需要补充到5-7步。请增加中间步骤，把路线拆分成更多步反应。"
            fix_guide = """=== 如何修正 ===
把路线中的每一步都拆开，起始原料→中间体A→中间体B→...→最终产物，确保有5-7个箭头。"""
        else:
            problem = f"步骤数太多（{wrong_steps}步），需要精简到5-7步。请合并一些连续的同类反应，或去掉不必要的步骤。"
            fix_guide = """=== 如何修正 ===
合并一些连续的简单转化（如氧化后直接酯化可合并为一步），控制在5-7步。"""
        
        retry_prompt = f"""【严重错误】你生成的命题第(5)题合成路线答案步骤数不符合要求！

问题：{problem}
要求：第(5)题答案必须恰好5-7步反应，不能多也不能少。{urgency}

{fix_guide}

=== 正确答案格式（必须严格遵守！） ===
第1步：{{{{结构式:SMILES}}}}（原料名）→[条件] {{{{结构式:SMILES}}}}（产物名）
第2步：{{{{结构式:SMILES}}}}（产物名）→[条件] {{{{结构式:SMILES}}}}（产物名）
第3步：{{{{结构式:SMILES}}}}（产物名）→[条件] {{{{结构式:SMILES}}}}（产物名）
第4步：{{{{结构式:SMILES}}}}（产物名）→[条件] {{{{结构式:SMILES}}}}（产物名）
第5步：{{{{结构式:SMILES}}}}（产物名）→[条件] {{{{结构式:SMILES}}}}（产物名）
（如有第6步和第7步，继续按此格式）

注意：答案路线必须与题干路线不同！不能完全照抄题干路线。
条件中如果有(2)编号，必须同时有(1)编号，不能只有(2)没有(1)！
条件必须极简，只写试剂名+条件符号，逗号分隔，严禁"在...条件下""加热回流""催化""反应"等冗余词！

请重新生成完整的JSON命题（包含所有字段），确保第5题答案恰好5-7步。"""
        return self.llm.generate(
            system_prompt="你是一位高考化学命题专家。第5题合成路线答案必须恰好5-7步！这是硬性要求，绝对不能违反！",
            user_prompt=retry_prompt,
            temperature=0.2,
        )

    def _validate_smiles_in_answers(self, answers: list) -> list:
        """验证答案中所有SMILES的有效性，返回无效的SMILES列表"""
        import re
        from structure_renderer import renderer

        invalid = []
        for a in answers:
            content = a.get("content", "")
            number = a.get("number", "?")
            # 提取所有 {{结构式:...}} 和 {结构式:...} 占位符
            matches = re.findall(r'\{结构式:([^}]+)\}', content)
            for m in matches:
                smiles = m.strip()
                # 跳过"化合物X"格式（不是SMILES）
                if re.match(r'^化合物[A-Z]$', smiles):
                    continue
                # 验证SMILES
                if not renderer.smiles_to_mol(smiles):
                    invalid.append({
                        "number": number,
                        "smiles": smiles,
                        "context": m,
                    })
        return invalid

    def _retry_with_smiles_fix(self, context: str, previous_response: str, invalid_smiles: list) -> str:
        """重试：修复无效的SMILES"""
        invalid_list = "\n".join(
            f"  第{i['number']}题: {{{{结构式:{i['smiles']}}}}} (来自: {i['context']})"
            for i in invalid_smiles
        )
        retry_prompt = f"""你刚才生成的命题中，以下SMILES表达式无效，无法被RDKit解析：

{invalid_list}

=== SMILES书写规范（务必遵守） ===
- 苯环：c1ccccc1
- 单取代苯：取代基在1位，如甲苯 Cc1ccccc1
- 对位二取代苯：如对硝基甲苯 Cc1ccc(N(=O)=O)cc1
- 间位二取代苯：如间硝基甲苯 Cc1cccc(N(=O)=O)c1
- 邻位二取代苯：如邻硝基甲苯 Cc1ccccc1N(=O)=O
- 羧基：C(=O)O（不是COOH）
- 醛基：C=O
- 羟基：O（不是OH）
- 氨基：N（不是NH2）
- 硝基：[N+](=O)[O-] 或 N(=O)=O
- 氰基：C#N
- 酯基：C(=O)OC
- 酰胺基：C(=O)N
- 醚键：COC（两个碳之间加O）
- 双键：C=C
- 三键：C#C

请修正所有无效SMILES，重新输出完整的JSON（包含所有字段）。"""
        return self.llm.generate(
            system_prompt="你是一位高考化学命题专家，也是SMILES化学式书写专家。请修正无效的SMILES表达式。",
            user_prompt=retry_prompt,
            temperature=0.1,
        )

    def _parse_json_response(self, response: str) -> dict:
        """解析LLM返回的JSON（增强版：处理markdown代码块）"""
        cleaned = response.strip()

        # 策略1：直接解析
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        # 策略2：去除markdown代码块标记 ```json ... ``` 或 ``` ... ```
        code_block = re.search(r'```(?:json)?\s*\n?([\s\S]*?)\n?```', cleaned)
        if code_block:
            try:
                return json.loads(code_block.group(1).strip())
            except json.JSONDecodeError:
                pass

        # 策略3：栈匹配
        start = cleaned.find('{')
        if start >= 0:
            depth = 0
            for i in range(start, len(cleaned)):
                if cleaned[i] == '{':
                    depth += 1
                elif cleaned[i] == '}':
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(cleaned[start:i + 1])
                        except json.JSONDecodeError:
                            break

        # 策略4：正则回退
        json_match = re.search(r'\{[\s\S]*\}', cleaned)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        return {"raw_output": response, "parse_error": True}

    # ================================================================
    # 条件清洗：确保条件表述严格符合高考真题规范
    # ================================================================

    @staticmethod
    def _clean_condition_text(text: str) -> str:
        """
        清洗冗余条件表述，使其符合高考真题极简格式。

        真题特征：
        - 浓HNO₃, 浓H₂SO₄, △（硝化）
        - H₂, Pd-C（催化加氢）
        - NaOH, H₂O, △（水解）
        - (1) O₃ (2) Zn, H₂O（臭氧化）
        - 浓H₂SO₄, △（酯化/消去）
        - Fe, HCl（硝基还原）
        - KMnO₄, H⁺（氧化）
        - O₂, Cu, △（醇催化氧化）
        - NaOH, 醇, △（卤代烃消去）
        - Br₂, FeBr₃（苯环溴代）
        """
        if not text or not isinstance(text, str):
            return text

        cleaned = text.strip()

        # === 1. 去除冗余修饰词（按危害程度逐级清理） ===
        # 第一级：完整的冗余句式
        cleaned = re.sub(r'在\s*[^，,]*?\s*条件下', '', cleaned)
        cleaned = re.sub(r'在\s*[^，,]*?\s*下', '', cleaned)
        cleaned = re.sub(r'用\s*[^，,]*?\s*催化', '', cleaned)
        cleaned = re.sub(r'以\s*[^，,]*?\s*为催化剂', '', cleaned)

        # 第二级：单个冗余词
        redundant_words = [
            '加热回流', '回流', '搅拌', '室温',
            '过夜', '滴加', '缓慢', '反应', '催化',
            '溶液中', '作用下', '处理后', '条件下',
            '洗涤', '干燥', '过滤', '蒸馏', '萃取',
            '浓缩', '重结晶', '柱层析', '纯化',
            '通入', '加入', '依次加入', '分批加入',
            '保持', '控制', '搅拌下', '持续',
            '催化下', '保护下', '氛围', '气氛',
        ]
        for word in sorted(redundant_words, key=len, reverse=True):
            # 使用词边界匹配，避免误删化学式中的字符
            cleaned = re.sub(r'\s*' + re.escape(word) + r'\s*', ' ', cleaned)

        # === 2. 将"加热"替换为 △（如果还没被替换） ===
        # 如果清洗后仍有"加热"或"△加热"，统一为 △
        cleaned = re.sub(r'△\s*加热', '△', cleaned)
        cleaned = re.sub(r'加热\s*△', '△', cleaned)
        if '加热' in cleaned and '△' not in cleaned:
            cleaned = cleaned.replace('加热', '△')

        # === 3. 清理分隔符 ===
        # 保护(1)(2)格式：如果文本中已有(1)(2)编号，不替换分隔符
        has_numbered = bool(re.search(r'\(\d+\)', cleaned))
        if not has_numbered:
            # 旧格式 "/" → 逗号（仅在无编号时）
            cleaned = re.sub(r'\s*/\s*', ', ', cleaned)
            # 分号 → 逗号（仅在无编号时）
            cleaned = re.sub(r'\s*;\s*', ', ', cleaned)
        else:
            # 有编号时，只清理编号之间的多余空格
            cleaned = re.sub(r'\s*;\s*', '; ', cleaned)  # 保留分号但规范化空格
        # 中文逗号 → 英文逗号
        cleaned = cleaned.replace('，', ', ')
        # 顿号 → 逗号
        cleaned = cleaned.replace('、', ', ')

        # === 4. 清理多余空格和逗号 ===
        cleaned = re.sub(r'\s*,\s*', ', ', cleaned)
        cleaned = re.sub(r',\s*,', ',', cleaned)  # 连续逗号
        cleaned = re.sub(r'^\s*,\s*', '', cleaned)  # 开头逗号
        cleaned = re.sub(r'\s*,\s*$', '', cleaned)  # 结尾逗号
        cleaned = re.sub(r'\s{2,}', ' ', cleaned)  # 多个空格
        cleaned = cleaned.strip()

        # === 5. 如果完全为空，返回原文本（避免空条件） ===
        if not cleaned:
            return text.strip()

        return cleaned

    def _clean_answer_conditions(self, question_data: dict) -> dict:
        """
        清洗所有答案中的条件表述，确保符合高考真题极简格式。
        主要处理第(5)题答案中的 →[条件] 格式。
        """
        if "answers" not in question_data:
            return question_data

        for a in question_data["answers"]:
            content = a.get("content", "")
            if not isinstance(content, str):
                continue

            # 匹配 →[条件] 格式，清洗方括号内的条件文本
            def _replace_condition(match):
                bracket_content = match.group(1)
                cleaned = self._clean_condition_text(bracket_content)
                return f'→[{cleaned}]'

            # 处理 →[条件] 格式
            cleaned_content = re.sub(r'→\s*\[([^\]]*)\]', _replace_condition, content)

            # 也处理旧格式：在...条件下得 → 得
            # （这些在 _clean_condition_text 中已处理，这里做兜底）
            if cleaned_content != content:
                a["content"] = cleaned_content

        return question_data

    def validate_question(self, question_data: dict) -> dict:
        """
        验证命题质量 v4.0 - 严格验证，错误必须修复
        检查项：化学正确性、格式规范性、题型分布、难度合理性、真题风格符合度
        issues = 必须修复的严重错误（触发重试）
        warnings = 建议修复的问题（仅提示）
        """
        issues = []
        warnings = []

        # 检查必要字段
        required_fields = ["stem", "questions", "answers"]
        for field in required_fields:
            if field not in question_data:
                issues.append(f"缺少必要字段: {field}")

        if "questions" in question_data:
            n_questions = len(question_data["questions"])
            min_q, max_q = QUESTION_COUNT_RANGE
            if n_questions < min_q:
                issues.append(f"问题数量偏少({n_questions}个)，标准为{min_q}-{max_q}个")
            elif n_questions > max_q:
                issues.append(f"问题数量偏多({n_questions}个)，标准为{min_q}-{max_q}个")

            # 检查题型分布（基于81道真题数据）
            types = [q.get("type", "") for q in question_data["questions"]]

            # 第1题：必须为基础识记
            if n_questions >= 1:
                q1_type = types[0] if len(types) > 0 else ""
                basic_types = ["官能团识别", "基础识记", "反应类型判断", "手性碳", "σ键/π键计数", "官能团", "反应类型", "分子式", "命名"]
                if not any(t in q1_type for t in basic_types):
                    issues.append(f"【严重】第1题必须为基础识记题，当前为: {q1_type}")

            # 第4题：必须为同分异构体
            if n_questions >= 4:
                q4_type = types[3] if len(types) > 3 else ""
                if "同分异构" not in q4_type:
                    issues.append(f"【严重】第4题必须为同分异构体题，当前题型为: {q4_type}")

            # 第5题：必须为合成路线设计
            if n_questions >= 5:
                q5_type = types[4] if len(types) > 4 else ""
                if "合成路线" not in q5_type and "合成" not in q5_type:
                    issues.append(f"【严重】第5题必须为合成路线设计题，当前题型为: {q5_type}")

            # 检查难度递进
            difficulties = [q.get("difficulty", "") for q in question_data["questions"]]
            if len(difficulties) >= 5:
                if difficulties[0] != "easy":
                    issues.append("【严重】第(1)题应为easy难度")
                if difficulties[3] != "hard":
                    issues.append("【严重】第(4)题应为hard难度")
                if difficulties[4] != "hard":
                    issues.append("【严重】第(5)题应为hard难度")

        # === 分值校验 v4.0 - 严格分值检查 ===
        if "questions" in question_data:
            questions = question_data["questions"]
            scores = [q.get("score", 0) for q in questions]
            total = sum(scores)
            n = len(scores)

            if n >= 5:
                if scores[4] != 5:
                    issues.append(f"【严重】第5题分值必须为5分，当前为{scores[4]}分")
                if scores[3] != 3:
                    issues.append(f"【严重】第4题分值必须为3分，当前为{scores[3]}分")

            for i in range(min(3, n)):
                expected = scores[i]
                if i in [0, 1] and expected not in [2]:
                    issues.append(f"【严重】第{i+1}题分值必须为2分，当前为{expected}分")
                if i == 2 and expected not in [2, 3]:
                    issues.append(f"【严重】第3题分值必须为2或3分，当前为{expected}分")

            if total not in [14, 15]:
                issues.append(f"【严重】总分({total}分)不符合标准，江苏高考有机大题应为14或15分")
            if total == 15:
                if n >= 5 and scores[:4] != [2, 2, 3, 3]:
                    issues.append(f"【严重】15分制下前4题分值应为2+2+3+3=10分，当前为{'+'.join(str(s) for s in scores[:4])}={sum(scores[:4])}分")
            elif total == 14:
                if n >= 5 and scores[:4] != [2, 2, 2, 3]:
                    issues.append(f"【严重】14分制下前4题分值应为2+2+2+3=9分，当前为{'+'.join(str(s) for s in scores[:4])}={sum(scores[:4])}分")

        if "total_score" in question_data:
            try:
                score = float(question_data["total_score"])
                if score not in [14, 15]:
                    issues.append(f"【严重】total_score字段({score})与标准（14-15分）不符")
                if "questions" in question_data:
                    actual_total = sum(q.get("score", 0) for q in question_data["questions"])
                    if score != actual_total:
                        issues.append(f"【严重】total_score({score})与各小题分数之和({actual_total})不一致")
            except (ValueError, TypeError):
                pass

        # 检查题干是否包含用途身份
        if "stem" in question_data:
            stem = question_data["stem"]
            if not any(kw in stem for kw in ["中间体", "药物", "香料", "材料", "天然", "活性", "染料", "农药", "医药"]):
                issues.append("【严重】题干必须包含目标化合物的用途身份描述（如'化合物X是某药物的中间体'）")

        # 检查合成路线设计：需包含已知信息和目标产物
        if "questions" in question_data:
            for q in question_data["questions"]:
                if "合成" in q.get("type", ""):
                    content = q.get("content", "")
                    if "已知" not in content:
                        issues.append("【严重】第(5)题合成路线设计缺少'已知'信息，必须提供一个新反应")
                    else:
                        known_section = content.split("已知")[1] if "已知" in content else ""
                        bad_known = [
                            "格氏试剂", "Grignard", "醛酮反应", "酯化反应", "水解反应",
                            "消去反应", "加成反应", "取代反应", "氧化反应", "还原反应",
                        ]
                        has_bad_known = any(kw in known_section for kw in bad_known)
                        has_rxn_arrow = any(sym in known_section for sym in ['→', '->', '⟶'])
                        if has_bad_known and not has_rxn_arrow:
                            issues.append("【严重】第(5)题已知信息过于泛泛，必须给出具体反应方程式（含→[条件]格式）")
                        if not has_rxn_arrow and len(known_section) < 20:
                            issues.append("【严重】第(5)题已知信息过于简短，必须给出具体反应方程式")
                    if "制备" not in content and "合成" not in content:
                        issues.append("【严重】第(5)题必须明确写出'制备化合物X'（X=目标产物代号）")

        # 检查"已知"信息是否与题干路线重复
        if "new_info" in question_data and question_data["new_info"]:
            new_info = str(question_data["new_info"])
            stem = question_data.get("stem", "")
            route_conditions = set()
            for match in re.finditer(r'→\s*\[([^\]]+)\]', stem):
                for cond in match.group(1).split(','):
                    cond = cond.strip()
                    if cond:
                        route_conditions.add(cond)
            known_conditions = set()
            for match in re.finditer(r'→\s*\[([^\]]+)\]', new_info):
                for cond in match.group(1).split(','):
                    cond = cond.strip()
                    if cond:
                        known_conditions.add(cond)
            overlap = route_conditions & known_conditions
            if overlap and len(overlap) >= 2:
                issues.append(f"【严重】已知信息中的条件与题干路线重复: {overlap}，必须提供全新反应")

        # 检查 new_info 格式
        if "new_info" in question_data and question_data["new_info"]:
            new_info = str(question_data["new_info"])
            if not re.search(r'\{结构式:', new_info):
                issues.append("【严重】已知信息(new_info)必须包含{{结构式:SMILES}}占位符")
            if not re.search(r'→\s*\[', new_info):
                issues.append("【严重】已知信息(new_info)格式必须与路线图一致，使用A→[条件]B格式（条件在箭头上方）")
            if re.search(r'＋.*→', new_info):
                issues.append("【严重】已知信息(new_info)禁止使用A＋B→C格式，必须使用A→[条件]B格式")

        # 检查第2题答案是否使用路线图格式
        if "answers" in question_data:
            for a in question_data["answers"]:
                num = a.get("number", "?")
                content = a.get("content", "")
                if not isinstance(content, str) or not content:
                    continue
                
                # 检查所有含方程式的答案（第2、3、5题）
                has_equation = re.search(r'\{结构式:', content) or re.search(r'→', content)
                if has_equation:
                    # 检查是否使用了正确的路线图格式
                    if re.search(r'→', content) and not re.search(r'→\s*\[', content):
                        issues.append(f"【严重】第({num})题答案方程式格式错误，必须使用A→[条件]B格式（条件在箭头上方方括号内）")
                    if re.search(r'＋.*→', content):
                        issues.append(f"【严重】第({num})题答案禁止使用A＋B→C格式，必须使用A→[条件]B格式")
                    
                    # 检查(2)必须有(1)规则（适用于所有含方程式的答案）
                    # 提取所有→[条件]中的条件文本
                    cond_matches = re.findall(r'→\s*\[([^\]]*)\]', content)
                    for cond in cond_matches:
                        has_num2 = bool(re.search(r'\(2\)', cond))
                        has_num1 = bool(re.search(r'\(1\)', cond))
                        has_num3 = bool(re.search(r'\(3\)', cond))
                        if has_num2 and not has_num1:
                            issues.append(f"【严重】第({num})题答案条件中有(2)但没有(1)：→[{cond}]，标号不完整！")
                        if has_num3 and (not has_num1 or not has_num2):
                            issues.append(f"【严重】第({num})题答案条件中有(3)但缺少(1)或(2)：→[{cond}]，标号不完整！")
            
            # 专门检查第2题
            for a in question_data["answers"]:
                if a.get("number") == 2 or a.get("number") == "2":
                    content = a.get("content", "")
                    if content and re.search(r'\{结构式:', content):
                        if not re.search(r'→\s*\[', content) and re.search(r'→', content):
                            issues.append("【严重】第(2)题答案方程式格式错误，必须使用A→[条件]B格式（条件在箭头上方）")
                        if re.search(r'＋.*→', content):
                            issues.append("【严重】第(2)题答案禁止使用A＋B→C格式，必须使用A→[条件]B格式")

        # 检查合成路线答案：5-7步、有结构式占位符、有试剂条件
        if "answers" in question_data:
            for a in question_data["answers"]:
                # 找到第5题（合成路线设计）的答案
                if a.get("number") == 5 or a.get("number") == "5":
                    answer_content = a.get("content", "")
                    # 检查步骤数（通过"第X步"或"步骤X"计数，兜底用箭头计数）
                    step_matches = re.findall(r'第(\d+)步|步骤(\d+)', answer_content)
                    step_count = len(step_matches)
                    if step_count == 0:
                        # 兜底：统计箭头数量
                        step_count = len(re.findall(r'→\s*\[', answer_content))
                    if step_count == 1:
                        issues.append(f"【严重】合成路线答案仅1步反应！这是绝对不允许的。必须设计5-7步的完整合成路线。")
                    elif step_count < 5 and step_count > 0:
                        issues.append(f"【严重】合成路线答案步骤数({step_count}步)偏少，必须为5-7步")
                    elif step_count > 7:
                        issues.append(f"【严重】合成路线答案步骤数({step_count}步)偏多，必须为5-7步")
                    # 检查是否有结构式占位符（支持单双大括号）
                    if not re.search(r'\{结构式:', answer_content):
                        issues.append("【严重】合成路线答案必须包含结构式占位符，每步产物用{结构式:SMILES}标出")
                    # 检查每步是否包含试剂/条件信息（条件错或漏扣分）
                    if step_count > 0:
                        steps_without_condition = 0
                        steps_verbose = 0
                        steps_bad_numbered = 0
                        for i in range(1, step_count + 1):
                            pattern = re.compile(rf'第{i}步[：:]\s*(.*?)(?=第\d+步[：:]|$)', re.DOTALL)
                            step_match = pattern.search(answer_content)
                            if step_match:
                                step_text = step_match.group(1)
                                cond_match = re.search(r'→\s*\[([^\]]*)\]', step_text)
                                if cond_match:
                                    condition = cond_match.group(1).strip()
                                    if not condition or len(condition) < 2:
                                        steps_without_condition += 1
                                    has_num2 = bool(re.search(r'\(2\)', condition))
                                    has_num1 = bool(re.search(r'\(1\)', condition))
                                    if has_num2 and not has_num1:
                                        steps_bad_numbered += 1
                                    verbose_patterns = [
                                        '在.*条件下', '反应', '加热回流', '搅拌',
                                        '室温', '过夜', '滴加', '缓慢', '催化',
                                        '溶液中', '作用下', '处理后',
                                    ]
                                    if any(vp in condition for vp in verbose_patterns):
                                        steps_verbose += 1
                                    if '/' in condition and condition.count(',') == 0 and not has_num1:
                                        steps_verbose += 1
                                else:
                                    has_condition = any(kw in step_text for kw in [
                                        'KMnO₄', 'H₂SO₄', 'HNO₃', 'NaOH', 'HCl',
                                        'Pd', 'Ni', 'Fe', 'SOCl₂', 'Br₂', 'Cl₂',
                                        '浓', '稀', '△', '加热', '光照',
                                        'H⁺', 'OH⁻', 'H₂', 'O₂', 'Na₂CO₃', 'NaHCO₃',
                                    ])
                                    if not has_condition:
                                        steps_without_condition += 1
                        if steps_without_condition > 0:
                            issues.append(f"【严重】第(5)题答案有{steps_without_condition}步缺少试剂/条件信息（条件错或漏扣分）")
                        if steps_verbose > 0:
                            issues.append(f"【严重】第(5)题答案有{steps_verbose}步条件表述冗余，应采用'试剂1, 试剂2, △'的极简格式")
                        if steps_bad_numbered > 0:
                            issues.append(f"【严重】第(5)题答案有{steps_bad_numbered}步条件中有(2)但没有(1)，标号不完整")

        # 检查同分异构体是否有3个条件，且条件合理
        if "questions" in question_data:
            for q in question_data["questions"]:
                if "同分异构" in q.get("type", ""):
                    content = q.get("content", "")
                    # 检查是否包含①②③编号条件
                    cond_count = sum(1 for c in ['①', '②', '③', '条件1', '条件2', '条件3'] if c in content)
                    if cond_count < 2:
                        issues.append("【严重】同分异构体题必须包含3个限定条件（①②③编号）")
                    if cond_count == 3:
                        has_func_group = any(kw in content for kw in ['遇FeCl₃', '银镜', 'NaHCO₃', 'Na₂CO₃', 'NaOH', '溴水', '褪色', '显色', '官能团', '能发生', '能与'])
                        has_spectrum = any(kw in content for kw in ['氢谱', '核磁', '峰组', '峰面积', '吸收峰', '化学位移', '红外', '质谱'])
                        has_structure = any(kw in content for kw in ['苯环', '手性碳', '对位', '间位', '邻位', '取代基', '对称', '碳原子数'])
                        if not has_func_group:
                            issues.append("【严重】同分异构体条件①必须包含官能团特征反应限制")
                        if not has_spectrum:
                            issues.append("【严重】同分异构体条件②必须包含核磁共振氢谱等谱学限制")
                        if not has_structure:
                            issues.append("【严重】同分异构体条件③必须包含苯环取代位置或手性碳等结构限制")

        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
        }

    def refine_question(self, question_data: dict, teacher_feedback: str) -> dict:
        """
        根据教师反馈优化命题
        """
        prompt = f"""
【当前命题】
{json.dumps(question_data, ensure_ascii=False, indent=2)}

【教师修改意见】
{teacher_feedback}

请根据上述修改意见，优化命题内容。只修改教师提到的部分，保持其他内容不变。
输出完整的优化后命题（JSON格式）。"""
        try:
            response = self.llm.generate(
                system_prompt="你是一位高考化学命题专家，请根据教师反馈精确修改命题。",
                user_prompt=prompt,
                temperature=0.2,
            )
            return self._parse_json_response(response)
        except Exception as e:
            return {"error": f"优化失败: {str(e)}"}

    def extract_from_paper(self, paper_text: str) -> dict:
        """从论文文本中提取合成路线"""
        try:
            response = self.llm.extract_route_from_paper(paper_text)
            return self._parse_json_response(response)
        except Exception as e:
            return {"error": f"论文提取失败: {str(e)}"}


# 全局单例
question_generator = QuestionGenerator()