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
    MIN_REACTION_STEPS, DEFAULT_DIFFICULTY,
    TOTAL_SCORE, QUESTION_COUNT_RANGE,
)


# 已知信息反应类型池（第5题已知信息从以下随机选择，避免 LLM 反复选 Perkin）
KNOWN_INFO_REACTION_POOL = [
    "Wittig反应（醛酮→烯烃）：R-CHO→[Ph₃P=CHR', THF] R-CH=CH-R'",
    "Knoevenagel缩合（醛+活泼亚甲基→α,β-不饱和化合物）：R-CHO→[CH₂(COOEt)₂, 哌啶, △] R-CH=C(COOEt)₂",
    "羟醛缩合（Aldol）：R-CHO→[NaOH, H₂O, △] R-CH=CH-CHO",
    "Perkin反应（芳醛+酸酐→肉桂酸类）：Ar-CHO→[(CH₃CO)₂O, CH₃COONa, △] Ar-CH=CH-COOH",
    "Claisen酯缩合（酯→β-酮酯）：R-COOEt→[NaOEt, EtOH] R-CO-CH₂-COOEt",
    "Gabriel胺合成（邻苯二甲酰亚胺→伯胺）：R-Br→[邻苯二甲酰亚胺钾, N₂H₄] R-NH₂",
    "Clemmensen还原（羰基→亚甲基）：R-CO-R'→[Zn(Hg), HCl] R-CH₂-R'",
    "Wolff-Kishner还原（羰基→亚甲基，碱性）：R-CO-R'→[N₂H₄, KOH, 二甘醇, △] R-CH₂-R'",
    "Hell-Volhard-Zelinsky反应（羧酸α-卤代）：R-CH₂-COOH→[Br₂, P(红)] R-CHBr-COOH",
    "Hofmann重排（酰胺→少一个碳的胺）：R-CONH₂→[Br₂, NaOH] R-NH₂",
    "黄鸣龙改进（羰基→亚甲基）：R-CO-R'→[N₂H₄·H₂O, NaOH, 二甘醇, △] R-CH₂-R'",
    "格氏试剂与CO₂（制备羧酸）：R-MgBr→[CO₂, H₃O⁺] R-COOH",
    "格氏试剂与醛酮（制备醇）：R-MgBr→[R'-CHO, H₃O⁺] R-CH(OH)-R'",
    "苯炔中间体（消除加成）：Ar-X→[NaNH₂, NH₃(l)] Ar-NH₂",
    "Diels-Alder反应（环加成）：双烯→[亲双烯体, △] 环己烯衍生物",
]


class QuestionGenerator:
    """命题生成引擎 v4.0"""

    def __init__(self):
        self.llm = llm_client

    def build_context_prompt(self, route_data: dict) -> str:
        """
        构建命题上下文 v6.0 — 丰富路线信息，引导LLM深度理解路线
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

        # 随机指定已知信息反应类型（避免 LLM 反复选 Perkin）
        forced_reaction = random.choice(KNOWN_INFO_REACTION_POOL)

        # 🔴 提取路线关键信息，帮助LLM精准设问
        steps = route_data.get("steps", [])
        route_summary = []
        for i, step in enumerate(steps):
            reactant = step.get("reactant", "?")
            product = step.get("product", "?")
            conditions = step.get("conditions", "?")
            rxn_type = step.get("reaction_type", "?")
            route_summary.append(
                f"  第{i+1}步：{reactant} →[{conditions}] {product}（{rxn_type}）"
            )
        
        # 提取关键中间体（路线中间位置的化合物，适用于第4题同分异构体）
        mid_compounds = []
        for i, step in enumerate(steps):
            if i == 0:
                mid_compounds.append(f"起始原料：{step.get('reactant', '?')}")
            prod = step.get("product", "?")
            if i < len(steps) - 1:
                mid_compounds.append(f"中间体{chr(65+i+1)}：{prod}")
            else:
                mid_compounds.append(f"最终产物：{prod}")

        context = f"""【用户输入的合成路线】
{json.dumps(route_data, ensure_ascii=False, indent=2)}

【路线步骤概览】
{chr(10).join(route_summary)}

【路线中的化合物】
{chr(10).join(mid_compounds)}

【建议的目标化合物用途身份】
{identity}

【路线中涉及的反应类型】
{', '.join(reaction_types_in_route) if reaction_types_in_route else '未指定'}

【相关高中反应参考】
{chr(10).join(relevant_reactions[:8])}

【🔴 强制规定 — 本次已知信息反应类型（必须严格遵守，不得改用其他反应）】
第(5)题已知信息(new_info)必须使用以下反应类型，不得使用 Perkin 或其他类型替代：
{forced_reaction}

【命题提示 — 请严格遵循以下指引】
1. 第(1)题：从上述中间体C/D/E中选择一个，问其官能团名称、分子式、手性碳个数或某步反应类型
   关键：必须指定具体化合物代号，不能泛泛而问
2. 第(2)题：选择路线中某一步转化，让学生书写反应方程式或推断产物结构简式
   关键：方程式必须用→[条件]格式，条件在箭头上方
3. 第(3)题：选择需要特定试剂的步骤，问反应条件或试剂选择
   关键：必须具体到某步（如"B→C所需的试剂和条件为____"）
4. 第(4)题：从路线中间体中选择一个，设计3个递进条件（①官能团特征反应②核磁氢谱③结构限制）
   关键：条件必须具体且有区分度，能唯一确定结构
5. 第(5)题：已知信息必须使用上面【强制规定】指定的反应类型，设计不同于题干路线的合成路线
   关键：目标产物是路线中某化合物的"类似物"（结构相近但不同），答案路线必须与题干路线不同
6. 第(5)题合成路线答案必须恰好5-7步，不能少于5步，也不能多于7步。这是硬性要求！
🔴 单步路线（仅1步反应）绝对禁止！必须设计5-7步的完整合成路线。
7. 🔴 所有方程式必须使用→[条件]格式（条件在箭头上方方括号内），绝对禁止A+B→C格式
8. 🔴 题干只写一句话描述实际用途，不写"合成路线如下"，不描述路线步骤
请基于以上合成路线，创作一道高质量的原创有机化学大题。命题要求已在系统提示中详细说明，请严格遵守。"""
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
        # 题目路线不限步数上限，仅答案限制5-7步

        # 构建上下文
        context = self.build_context_prompt(route_data)

        # 调用DeepSeek生成命题
        try:
            raw_response = self.llm.generate_question(context, difficulty)
            self._last_raw = raw_response
            question_data = self._parse_json_response(raw_response)
            question_data["raw_route"] = route_data
            question_data["generated_by"] = "DeepSeek-Chemistry-Agent-v3.0"
            
            # 🔴 提取hidden_structure（结构推断题专用）
            hidden_structure = question_data.get("hidden_structure")
            if hidden_structure and hidden_structure != "null" and hidden_structure != "None":
                question_data["raw_route"]["hidden_structure"] = hidden_structure
                print(f"  🔍 结构推断题：隐藏化合物 {hidden_structure} 的结构式")

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

            # === 🔴 终审格式审计：确认答案格式符合高考要求 ===
            format_audit = self._final_format_audit(question_data)
            question_data["_format_audit"] = format_audit

            return question_data
        except Exception as e:
            import traceback
            tb = traceback.format_exc()
            print("=== generate_from_route EXCEPTION TRACEBACK ===\n" + tb, flush=True)
            return {"error": f"命题生成失败: {str(e)}", "raw_response": getattr(self, '_last_raw', ''), "_traceback": tb}

    @staticmethod
    def _coerce_dict_list(value):
        """将 answers/questions 规范化为 list[dict]。

        LLM 在重试时偶发把 answers 返回成 list[str]（如 ["答案1","答案2"]），
        导致下游 a.get("content") / q.get("type") 抛 'str' object has no attribute 'get'。
        这里把字符串元素包装为 {"content": str}，其余非 dict 元素丢弃，保证不再崩溃。
        """
        if not isinstance(value, list):
            return []
        result = []
        for item in value:
            if isinstance(item, dict):
                result.append(item)
            elif isinstance(item, str):
                result.append({"content": item})
        return result

    @classmethod
    def _normalize_question_data(cls, question_data):
        """把 question_data 中 answers/questions 规范化，兜住 LLM 偶发的各种异常形态。

        LLM 在重试时可能把 answers/questions 返回成：
        - list[str]（如 ["答案1","答案2"]）
        - str（纯文本描述）
        - dict（单个对象而非列表）
        这些都会导致下游 a.get("content") / q.get("type") 抛 'str' object has no attribute 'get'。
        这里统一归约为 list[dict]，无法解析的形态置空以触发验证重试，而非直接崩溃。
        """
        if not isinstance(question_data, dict):
            return question_data
        for key in ("answers", "questions"):
            val = question_data.get(key)
            if isinstance(val, list):
                question_data[key] = cls._coerce_dict_list(val)
            elif isinstance(val, str):
                # 纯字符串无法可靠拆分为结构化条目，置空交给验证重试兜底
                question_data[key] = []
            elif isinstance(val, dict):
                question_data[key] = [val]
            elif val is None:
                question_data[key] = []

        # 兜底：answers 元素即便丢失 number（LLM 返回 list[str] 时），也按位置补全，
        # 否则前端无法识别第5题路线答案，导致答案不显示。
        answers = question_data.get("answers")
        if isinstance(answers, list):
            for idx, a in enumerate(answers):
                if isinstance(a, dict) and a.get("number") is None:
                    a["number"] = idx + 1
        return question_data

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
- 第(1)题必须是基础识记题（官能团名称/反应类型/分子式），难度easy，必须指定具体化合物代号
- 第(2)题必须具体到某步转化（如"写出B→C反应的化学方程式"），若含方程式必须用路线图格式
- 🔴 结构推断题：若第(2)题为结构推断，必须设置hidden_structure字段为被隐藏的化合物代号（如"D"），且不能隐藏起始原料A
- 第(3)题必须具体到某步（如"B→C所需的试剂和条件为____"），若含方程式也必须用路线图格式
- 第(4)题必须是同分异构体题，含3个递进条件（①②③），难度hard
  - ①必须写具体官能团特征反应（如"遇FeCl₃溶液显紫色"），不能泛泛说"含有酚羟基"
  - ②必须给出具体谱学数据（如"核磁共振氢谱显示有4组峰，峰面积比为1:2:2:3"）
  - ③必须给出具体结构限制（如"苯环上的一氯代物只有2种"）
- 第(5)题必须是合成路线设计题，含"已知"信息，明确写"制备化合物X"，难度hard
- 分值严格按14分(2+2+2+3+5)或15分(2+2+3+3+5)分配

🔴🔴 化学方程式格式（最高优先级！违反此条全部重做）🔴🔴
- 唯一正确格式：{{{{结构式:SMILES}}}}→[条件] {{{{结构式:SMILES}}}}
- →[条件]是一个整体！箭头后紧跟方括号，条件写在方括号内，渲染时条件显示在箭头上方
- 绝对禁止：A＋B→C 或 A+B→C（双反应物反应，第二个反应物写入条件方括号内）
- 绝对禁止：文字描述反应（如"在NaOH条件下反应得B""与乙酸酐反应生成C"）
- 绝对禁止：→后没有方括号（如→NaOH B 或 →B）
- 绝对禁止：→[]空条件方括号
✅ Perkin正确：{{{{结构式:O=Cc1ccccc1}}}}→[(CH₃CO)₂O, CH₃COONa, △] {{{{结构式:O=C(O)/C=C/c1ccccc1}}}}
❌ Perkin错误：苯甲醛＋乙酸酐→[CH₃COONa, △]肉桂酸
❌ Perkin错误：苯甲醛与乙酸酐在碱催化下反应生成肉桂酸
❌ Perkin错误：苯甲醛→乙酸酐肉桂酸（无条件方括号）

- 条件中有(2)编号必须同时有(1)编号，不能只有(2)没有(1)
- 条件必须极简！只写试剂名+条件符号，逗号分隔，严禁冗余词
🔴🔴 题干格式（最高优先级！违反此条全部重做）🔴🔴
- 题干就一句话，只说这个化合物的实际用途/意义，不超过50字
- 不需要写"合成路线如下"或"可通过以下路线合成"，路线图自动展示
- 题干绝对不能描述任何合成路线步骤！禁止出现以下任何内容：
  ❌ 禁止：化合物A经硝化得B，B经还原得C...
  ❌ 禁止：A→[条件]B→[条件]C...
  ❌ 禁止：化合物A与乙酸酐反应生成B...
  ❌ 禁止：在Fe/HCl条件下还原得C...
  ❌ 禁止：合成路线如下、可通过以下路线合成
  ✅ 正确：化合物G是某抗炎药物的关键中间体。
  ✅ 正确：化合物H是一种新型香料的主要成分。
- 题干绝对不能与已知信息重复任何内容！
- 已知信息只能出现在第(5)题设问中，答案中不要重复"已知："，解析中不要复述
- 已知信息的反应不能与题干路线重复
- 已知信息中的双反应物反应也必须用A→[条件]B格式
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
所有方程式必须用→[条件]格式！禁止A+B→C、文字描述反应、→后无方括号！

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
        """解析LLM返回的JSON（增强版：处理markdown代码块 + 数据规范化）"""
        cleaned = response.strip()
        result = None

        # 策略1：直接解析
        try:
            result = json.loads(cleaned)
        except json.JSONDecodeError:
            pass

        # 策略2：去除markdown代码块标记 ```json ... ``` 或 ``` ... ```
        if result is None:
            code_block = re.search(r'```(?:json)?\s*\n?([\s\S]*?)\n?```', cleaned)
            if code_block:
                try:
                    result = json.loads(code_block.group(1).strip())
                except json.JSONDecodeError:
                    pass

        # 策略3：栈匹配
        if result is None:
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
                                result = json.loads(cleaned[start:i + 1])
                                break
                            except json.JSONDecodeError:
                                break

        # 策略4：正则回退
        if result is None:
            json_match = re.search(r'\{[\s\S]*\}', cleaned)
            if json_match:
                try:
                    result = json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass

        # 🔴 数据规范化：确保answers/questions总是list[dict]，防止LLM返回list[str]导致下游a.get()崩溃
        if isinstance(result, dict):
            result = QuestionGenerator._normalize_question_data(result)
            return result

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

        # 防御性：确保answers是 list[dict]
        question_data = QuestionGenerator._normalize_question_data(question_data)

        for a in question_data["answers"]:
            if not isinstance(a, dict):
                continue
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
            if not any(kw in stem for kw in ["中间体", "药物", "香料", "材料", "天然", "活性", "染料", "农药", "医药", "合成", "制备", "用于", "成分"]):
                issues.append("【严重】题干必须包含目标化合物的实际用途描述（如'化合物G是某药物的中间体'）")
            
            # 🔴 检查题干是否描述了合成路线（绝对不能！）
            # 扩展检测模式：覆盖所有可能的路线描述形式
            route_patterns_in_stem = [
                (r'→', '箭头符号'),
                (r'经.*得', '经...得格式'),
                (r'\[.*?\]', '方括号条件'),
                (r'硝化.*得', '硝化反应描述'),
                (r'还原.*得', '还原反应描述'),
                (r'氧化.*得', '氧化反应描述'),
                (r'酯化.*得', '酯化反应描述'),
                (r'水解.*得', '水解反应描述'),
                (r'酰化.*得', '酰化反应描述'),
                (r'取代.*得', '取代反应描述'),
                (r'加成.*得', '加成反应描述'),
                (r'消去.*得', '消去反应描述'),
                (r'卤代.*得', '卤代反应描述'),
                (r'溴代.*得', '溴代反应描述'),
                (r'氯化.*得', '氯化反应描述'),
                (r'缩合.*得', '缩合反应描述'),
                (r'重氮化.*得', '重氮化反应描述'),
                (r'偶联.*得', '偶联反应描述'),
                (r'第\d+步', '步骤编号'),
                (r'第一步', '步骤描述'),
                (r'第二步', '步骤描述'),
                (r'第三步', '步骤描述'),
                (r'化合物[A-Z]经', '化合物经...格式'),
                (r'生成化合物', '生成化合物描述'),
                (r'与.*反应', '反应描述'),
                (r'与.*缩合', '缩合反应描述'),
                (r'在.*条件下', '条件描述'),
                (r'经.*反应生成', '经...反应生成格式'),
                (r'经.*反应得', '经...反应得格式'),
                (r'在.*催化下', '催化条件描述'),
                (r'以.*为原料.*经', '以...为原料经...格式'),
                (r'通入.*得', '通入...得格式'),
                (r'用.*处理.*得', '用...处理得格式'),
                (r'通过.*反应', '通过...反应格式'),
                (r'依次经', '依次经...格式'),
                (r'再经', '再经...格式'),
                (r'然后.*得', '然后...得格式'),
                (r'接着.*得', '接着...得格式'),
                (r'最后.*得', '最后...得格式'),
                (r'进一步.*得', '进一步...得格式'),
                (r'分别.*得', '分别...得格式'),
            ]
            found_patterns = []
            for pattern, desc in route_patterns_in_stem:
                if re.search(pattern, stem):
                    found_patterns.append(desc)
            if found_patterns:
                issues.append(f"【严重】题干中出现了路线描述（{', '.join(found_patterns[:5])}等{len(found_patterns)}处）：题干只需一句话描述实际用途，禁止任何路线步骤描述")
            
            # 题干过长也说明在描述路线
            if len(stem) > 50:
                issues.append(f"【严重】题干过长（{len(stem)}字），应仅1句话描述实际应用意义，不超过50字")
            
            # 🔴 题干不能包含"合成路线如下"等冗余表述
            if re.search(r'合成路线如下|可通过以下路线合成|路线如下|合成路线', stem):
                issues.append("【严重】题干不需要写'合成路线如下'，只写一句话描述实际意义即可，路线图自动展示在下方")

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
            # 🔴 双反应物格式检查：Perkin/Knoevenagel/羟醛缩合等禁止A＋B→C格式
            if re.search(r'＋.*→', new_info):
                issues.append("【严重】已知信息(new_info)禁止使用A＋B→C格式，必须使用A→[条件]B格式（第二个反应物写入条件方括号内）")
            # 🔴 检查双反应物反应是否用了错误格式
            double_reactant_patterns = [
                (r'苯甲醛.*乙酸酐|乙酸酐.*苯甲醛', 'Perkin反应：苯甲醛→[(CH₃CO)₂O, CH₃COONa, △]产物'),
                (r'苯甲醛.*丙二酸|丙二酸.*苯甲醛', 'Knoevenagel反应：苯甲醛→[CH₂(COOH)₂, 哌啶, △]产物'),
                (r'苯甲醛.*乙醛|乙醛.*苯甲醛', '羟醛缩合：苯甲醛→[CH₃CHO, NaOH, H₂O]产物'),
                (r'醛.*酮.*缩合|酮.*醛.*缩合', 'Aldol缩合，第二个反应物写入条件'),
            ]
            for pattern, fix_hint in double_reactant_patterns:
                if re.search(pattern, new_info, re.IGNORECASE):
                    if re.search(r'＋', new_info) or not re.search(r'→\s*\[', new_info):
                        issues.append(f"【严重】已知信息({fix_hint})——双反应物反应禁止A＋B→C格式，第二个反应物必须写入条件方括号内！")
                        break

        # 🔴 已知信息重复检测：已知信息只能在第(5)题设问中出现一次
        if "new_info" in question_data and question_data["new_info"]:
            new_info = str(question_data["new_info"])
            # 检查答案中是否重复了已知信息
            if "answers" in question_data:
                for a in question_data["answers"]:
                    num = a.get("number", "?")
                    content = str(a.get("content", ""))
                    if num == 5 and "已知" in content:
                        issues.append("【严重】第(5)题答案中重复了'已知'信息。已知信息只能出现在第(5)题设问中，答案直接写合成路线即可，不要重复'已知：...'")
            # 检查解析中是否重复了已知信息
            analysis = str(question_data.get("analysis", ""))
            if "已知" in analysis and "→" in analysis:
                # 检查是否在复述已知信息反应式
                if re.search(r'已知.*→.*\[', analysis):
                    issues.append("【严重】解析中重复了已知信息。已知信息只能出现在第(5)题设问中，解析中不要复述")

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
                        # 区分是花括号还是完全没有方括号
                        if re.search(r'→\s*\{', content):
                            issues.append(f"【严重】第({num})题答案使用花括号→{{条件}}，必须改为方括号→[条件]！条件写在箭头上方必须用[]")
                        else:
                            issues.append(f"【严重】第({num})题答案方程式格式错误，必须使用A→[条件]B格式（条件在箭头上方方括号内）")
                    # 🔴 双反应物格式检查：禁止A＋B→C格式
                    if re.search(r'＋.*→', content):
                        issues.append(f"【严重】第({num})题答案禁止使用A＋B→C格式，第二个反应物必须写入条件方括号内！→[试剂, 条件]B")
                    # 🔴 检查答案中是否包含双反应物反应类型的错误格式
                    if re.search(r'Perkin|Knoevenagel|羟醛缩合|Aldol|缩合', content, re.IGNORECASE):
                        if re.search(r'＋', content):
                            issues.append(f"【严重】第({num})题答案涉及双反应物反应（Perkin/Knoevenagel/羟醛缩合），禁止A＋B→C格式！第二个反应物必须写入条件方括号内")
                    
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

        # === 🔴 内容质量检查：设问必须具体，与路线紧密结合 ===
        if "questions" in question_data:
            for q in question_data["questions"]:
                num = q.get("number", "?")
                content = q.get("content", "")
                
                if num in [1, "1"]:
                    # 第1题必须提到具体化合物或反应步骤
                    has_compound = bool(re.search(r'化合物\s*[A-Z]', content))
                    has_step = bool(re.search(r'[A-Z]\s*→\s*[A-Z]', content))
                    has_type = bool(re.search(r'反应类型|官能团|分子式|命名', content))
                    if not has_compound and not has_step:
                        issues.append(f"【质量】第(1)题设问不够具体，应指定化合物代号（如'化合物C中含有的官能团'）")
                    if not has_type:
                        issues.append(f"【质量】第(1)题应考查官能团名称、反应类型或分子式")
                
                elif num in [2, "2"]:
                    # 第2题必须提到具体反应步骤
                    has_step = bool(re.search(r'[A-Z]\s*→\s*[A-Z]|制备|反应|方程式', content))
                    if not has_step:
                        issues.append(f"【质量】第(2)题应具体到某步转化（如'写出B→C反应的化学方程式'）")
                
                elif num in [3, "3"]:
                    # 第3题必须问到试剂或条件
                    has_reagent = bool(re.search(r'试剂|条件|选用|所需', content))
                    if not has_reagent:
                        issues.append(f"【质量】第(3)题应询问试剂或反应条件（如'C→D所需的试剂和条件为____'）")
                
                elif num in [4, "4"]:
                    # 第4题同分异构体质量检查
                    if "同分异构" in content:
                        # 检查是否指定了具体化合物
                        has_compound = bool(re.search(r'化合物\s*[A-Z]', content))
                        if not has_compound:
                            issues.append(f"【质量】第(4)题应指定具体化合物（如'化合物D的同分异构体中'）")
                        
                        # 检查条件①是否有具体官能团特征反应
                        has_specific_func = bool(re.search(
                            r'FeCl₃|银镜|NaHCO₃|Na₂CO₃|NaOH|溴水|褪色|显色|能与.*反应|发生.*反应',
                            content
                        ))
                        if not has_specific_func:
                            issues.append(f"【质量】第(4)题条件①过于泛泛，应写具体特征反应（如'遇FeCl₃显紫色'）")
                        
                        # 检查条件②是否有具体谱学数据
                        has_specific_spectrum = bool(re.search(
                            r'峰面积比|组峰.*面积|化学位移|吸收峰.*cm|质谱.*m/z',
                            content
                        ))
                        if not has_specific_spectrum:
                            issues.append(f"【质量】第(4)题条件②过于泛泛，应给出具体谱学数据（如'峰面积比为1:2:2:3'）")
                        
                        # 检查条件③是否有具体结构限制
                        has_specific_structure = bool(re.search(
                            r'一氯代物.*[1-9]种|手性碳.*[1-9]个|对位|间位|邻位|取代基.*[1-9]个|对称',
                            content
                        ))
                        if not has_specific_structure:
                            issues.append(f"【质量】第(4)题条件③过于泛泛，应给出具体结构限制（如'苯环上一氯代物只有2种'）")
                
                elif num in [5, "5"]:
                    # 第5题质量检查
                    if "合成" in content or "制备" in content:
                        # 必须明确写"制备化合物X"
                        has_prepare = bool(re.search(r'制备化合物\s*[A-Z]', content))
                        if not has_prepare:
                            issues.append(f"【质量】第(5)题应明确写'制备化合物X'（X为具体化合物代号）")
                        
                        # 已知信息不能太泛泛
                        if "已知" in content:
                            known_part = content.split("已知")[1] if "已知" in content else ""
                            if len(known_part) < 15:
                                issues.append(f"【质量】第(5)题已知信息过于简短，应给出具体反应方程式")
                            if not re.search(r'\{结构式:', known_part):
                                issues.append(f"【质量】第(5)题已知信息应包含结构式占位符")
                            # 已知信息必须有→[条件]格式
                            if not re.search(r'→\s*\[', known_part):
                                issues.append(f"【质量】第(5)题已知信息必须使用→[条件]格式（条件在箭头上方方括号内）")
        
        # === 🔴 化学准确性验证（新增） ===
        chem_issues = self._check_chemical_accuracy(question_data)
        issues.extend(chem_issues)
        
        # === 🔴 题目多样性检查（新增） ===
        diversity_issues = self._check_question_diversity(question_data)
        issues.extend(diversity_issues)

        # === 🔴 内容重复检测（新增） ===
        duplication_issues = self._check_content_duplication(question_data)
        issues.extend(duplication_issues)

        # 🔴 全局格式扫描：检查所有字段中的A＋B→C格式
        global_issues = self._global_format_check(question_data)
        issues.extend(global_issues)

        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
        }

    def _check_chemical_accuracy(self, question_data: dict) -> list:
        """
        🔴 化学准确性验证：检查反应条件与反应类型是否匹配、试剂选择性是否正确等。
        """
        import re
        issues = []
        
        answers = question_data.get("answers", [])
        new_info = str(question_data.get("new_info", ""))
        
        all_texts = []
        if new_info and new_info != "None":
            all_texts.append(("已知信息", new_info))
        for a in answers:
            content = str(a.get("content", ""))
            if content:
                all_texts.append((f"第{a.get('number', '?')}题答案", content))
        
        for field_name, text in all_texts:
            # 提取所有→[条件]
            conds = re.findall(r'→\s*\[([^\]]*)\]', text)
            for cond in conds:
                cond_lower = cond.lower()
                
                # 1. 硝化反应检查
                if re.search(r'硝化|nitr', cond_lower):
                    if 'hno₃' not in cond_lower and 'hno3' not in cond_lower:
                        issues.append(f"【化学】{field_name}：硝化反应条件中缺少HNO₃ →[{cond}]")
                    if 'h₂so₄' not in cond_lower and 'h2so4' not in cond_lower and '浓硫酸' not in cond:
                        issues.append(f"【化学】{field_name}：硝化反应条件中缺少浓H₂SO₄ →[{cond}]")
                
                # 2. 硝基还原检查
                if re.search(r'还原.*硝基|硝基.*还原|fe.*hcl|sn.*hcl', cond_lower):
                    if 'fe' not in cond_lower and 'sn' not in cond_lower and 'h₂' not in cond_lower and 'h2' not in cond_lower:
                        issues.append(f"【化学】{field_name}：硝基还原需要Fe/HCl、Sn/HCl或H₂/Pd-C →[{cond}]")
                
                # 3. LiAlH₄ 使用检查
                if 'lialh₄' in cond_lower or 'lialh4' in cond_lower:
                    # LiAlH₄后通常需要水处理
                    if 'h₂o' not in cond_lower and 'h2o' not in cond_lower and '(2)' not in cond:
                        issues.append(f"【化学】{field_name}：LiAlH₄还原后需要水处理 →[{cond}]")
                
                # 4. NaBH₄ 使用检查
                if 'nabh₄' in cond_lower or 'nabh4' in cond_lower:
                    # NaBH₄只能还原醛酮，不能还原酯/羧酸/酰胺
                    if re.search(r'酯|羧酸|酰胺|ester|carboxyl|amide', text):
                        issues.append(f"【化学】{field_name}：NaBH₄不能还原酯基/羧基/酰胺基，只能还原醛酮羰基 →[{cond}]")
                
                # 5. 氧化反应检查
                if re.search(r'kmno₄|kmno4|酸性高锰酸钾', cond_lower):
                    # 酸性KMnO₄会氧化苯环侧链为羧基
                    pass  # 这是正确的用法，无需警告
                
                # 6. 苯环卤代检查
                if re.search(r'br₂|br2|cl₂|cl2', cond_lower):
                    if re.search(r'苯环|aromatic|phenyl', cond_lower) or re.search(r'c1ccccc1', text):
                        if 'febr₃' not in cond_lower and 'febr3' not in cond_lower and 'fecl₃' not in cond_lower and 'fecl3' not in cond_lower and 'alcl₃' not in cond_lower and 'alcl3' not in cond_lower and 'fe' not in cond_lower:
                            issues.append(f"【化学】{field_name}：苯环卤代需要Lewis酸催化剂（FeBr₃/FeCl₃/AlCl₃/Fe） →[{cond}]")
                
                # 7. 酯化反应检查
                if re.search(r'酯化|esterif', cond_lower):
                    if 'h₂so₄' not in cond_lower and 'h2so4' not in cond_lower and '浓硫酸' not in cond:
                        issues.append(f"【化学】{field_name}：酯化反应通常需要浓H₂SO₄催化 →[{cond}]")
                
                # 8. 消去反应检查
                if re.search(r'消去|elimin', cond_lower):
                    if 'naoh' in cond_lower and '醇' not in cond and 'alcohol' not in cond_lower and 'etoh' not in cond_lower:
                        issues.append(f"【化学】{field_name}：卤代烃消去需要NaOH/醇溶液 →[{cond}]")
        
        return issues
    
    def _check_question_diversity(self, question_data: dict) -> list:
        """
        🔴 题目多样性检查（基于81道真题分析）：确保题目不模板化，各题有区分度。
        """
        import re
        issues = []
        warnings = []
        
        questions = question_data.get("questions", [])
        if len(questions) < 5:
            return issues
        
        q_types = [q.get("type", "") for q in questions]
        
        # === 第1题检查：从7种高频设问中随机选择 ===
        q1_type = q_types[0]
        q1_content = questions[0].get("content", "")
        valid_q1_types = ["官能团识别", "碳原子杂化", "σπ键计数", "手性碳", "酸碱性比较", "反应类型", "反应目的"]
        if q1_type not in valid_q1_types and "官能团" in q1_type:
            pass  # 近似匹配
        elif q1_type not in valid_q1_types:
            warnings.append(f"【多样性】第(1)题类型'{q1_type}'不在真题高频设问中，建议从{valid_q1_types}中选择")
        
        # 第1题不能总是官能团识别
        if "官能团名称" in q1_content and "分子式" not in q1_content and "杂化" not in q1_content and "σ键" not in q1_content and "手性碳" not in q1_content and "反应类型" not in q1_content and "酸性" not in q1_content and "碱性" not in q1_content:
            warnings.append("【多样性】第(1)题建议变换问法，避免总是问官能团名称（真题中还有杂化、σ/π键、手性碳、酸碱性比较等）")
        
        # === 第2题检查：从5种高频设问中随机选择 ===
        q2_type = q_types[1]
        q2_content = questions[1].get("content", "")
        valid_q2_types = ["结构推断", "反应类型", "副产物推断", "反应机理", "化学方程式"]
        if q2_type not in valid_q2_types:
            warnings.append(f"【多样性】第(2)题类型'{q2_type}'不在真题高频设问中，建议从{valid_q2_types}中选择")
        
        # 第2题必须有具体转化
        if not re.search(r'[A-G]→[A-G]|[A-G]转化为[A-G]|由[A-G]制备[A-G]|结构简式|反应类型|副产物|经历.*过程', q2_content):
            warnings.append("【多样性】第(2)题建议指定具体转化步骤（如'D的结构简式为____'、'C→D的反应类型为____'）")
        
        # 🔴 结构推断题：检查hidden_structure是否设置
        if "结构推断" in q2_type or "结构简式" in q2_content:
            hidden = question_data.get("hidden_structure")
            if not hidden or hidden == "null" or hidden == "None":
                issues.append("【严重】第(2)题为结构推断题，但hidden_structure字段未设置。必须设置hidden_structure为被隐藏结构的化合物代号（如'D'）")
            else:
                # 检查hidden_structure是否为有效的化合物代号
                if not re.match(r'^[A-Z]$', hidden):
                    issues.append(f"【严重】hidden_structure字段值'{hidden}'不是有效的化合物代号（应为单个大写字母如'A''B''C'等）")
                # 检查隐藏的不能是起始原料A
                if hidden == "A":
                    issues.append("【严重】不能隐藏起始原料A的结构，请选择中间产物（如B、C、D等）")
                # 检查设问中是否包含了hidden_structure对应的化合物
                if hidden not in q2_content:
                    warnings.append(f"【多样性】第(2)题设问中未出现被隐藏的化合物{hidden}，建议在设问中明确写出'化合物{hidden}的结构简式为____'")
        
        # === 第3题检查：从5种高频设问中随机选择，与第2题不重复 ===
        q3_type = q_types[2]
        q3_content = questions[2].get("content", "")
        valid_q3_types = ["试剂条件", "反应类型+副产物", "中间体结构", "保护基目的", "试剂选择理由"]
        if q3_type not in valid_q3_types:
            warnings.append(f"【多样性】第(3)题类型'{q3_type}'不在真题高频设问中，建议从{valid_q3_types}中选择")
        
        # 第3题与第2题不能重复类型
        if q2_type == q3_type:
            issues.append(f"【严重】第(2)题和第(3)题类型相同（都是'{q2_type}'），真题中两题不会重复考查同一类型，必须更换其中一题")
        
        # 第3题必须有具体转化
        if not re.search(r'[A-G]→[A-G]|[A-G]转化为[A-G]|由[A-G]制备[A-G]|试剂|条件|中间体|目的|加入.*是为了', q3_content):
            warnings.append("【多样性】第(3)题建议指定具体转化步骤（如'C→D所需的试剂和条件为____'）")
        
        # === 第4题同分异构体条件多样性检查 ===
        q4_content = questions[3].get("content", "")
        # 确保条件①不是总是FeCl₃
        feature_conditions = ["FeCl₃", "银镜", "NaHCO₃", "溴水", "溴的四氯化碳", "水解", "显色", "NaOH"]
        found_conditions = [c for c in feature_conditions if c in q4_content]
        if len(found_conditions) < 2:
            warnings.append("【多样性】第(4)题同分异构条件建议多样化，真题中常见组合：水解+银镜+氢谱、FeCl₃显色+水解+氢谱、NaHCO₃反应+氢谱+手性碳")
        
        # 确保条件②有具体谱学数据
        if "核磁" not in q4_content and "氢谱" not in q4_content and "红外" not in q4_content and "NMR" not in q4_content and "化学环境" not in q4_content:
            issues.append("【严重】第(4)题同分异构条件缺少谱学数据（核磁共振氢谱/红外光谱），真题中条件②必须有谱学特征")
        
        # 确保条件③有具体结构限制
        if "氯代物" not in q4_content and "手性碳" not in q4_content and "不含甲基" not in q4_content and "种官能团" not in q4_content and "取代基" not in q4_content:
            warnings.append("【多样性】第(4)题条件③建议包含具体结构限制（如苯环上一氯代物X种、含N个手性碳、不含甲基等）")
        
        # === 第5题检查 ===
        q5_content = questions[4].get("content", "")
        if "制备" not in q5_content and "合成" not in q5_content:
            issues.append("【严重】第(5)题必须包含'制备'或'合成'关键词")
        
        if "已知" not in q5_content:
            issues.append("【严重】第(5)题必须包含'已知'信息（具体反应方程式），真题中第5题100%有已知信息")
        
        # 已知信息必须包含具体反应式
        if "已知" in q5_content and "→" not in q5_content:
            issues.append("【严重】第(5)题已知信息必须包含具体反应方程式（→[条件]格式），不能是泛泛描述")
        
        return issues

    def _check_content_duplication(self, question_data: dict) -> list:
        """
        🔴 内容重复检测：确保题干、已知信息、题目、答案之间不重复。
        检测项：
        1. 题干 vs 已知信息：是否有相同或高度相似的内容
        2. 题目 vs 答案：答案中是否直接复述了题目内容
        3. 题干 vs 路线描述：题干是否包含了路线步骤
        4. 各小题之间：是否有重复的设问
        """
        import re
        issues = []
        
        stem = str(question_data.get("stem", ""))
        new_info = str(question_data.get("new_info", ""))
        questions = question_data.get("questions", [])
        answers = question_data.get("answers", [])
        
        # === 1. 题干 vs 已知信息重复检测 ===
        if stem and new_info and new_info != "None":
            # 提取关键化合物名称和结构式
            stem_compounds = set(re.findall(r'化合物\s*[A-Z]', stem))
            new_info_compounds = set(re.findall(r'化合物\s*[A-Z]', new_info))
            overlap_compounds = stem_compounds & new_info_compounds
            if overlap_compounds:
                # 如果题干和已知信息提到了相同的化合物，检查是否重复描述了反应
                stem_sentences = [s.strip() for s in re.split(r'[。，；]', stem) if len(s.strip()) > 10]
                for sent in stem_sentences:
                    # 检查题干句子是否描述了反应（含"得""生成""反应"等词）
                    if re.search(r'得|生成|反应|转化|制备', sent):
                        # 检查已知信息中是否有相似内容
                        words_in_sent = set(re.findall(r'[\u4e00-\u9fff]{2,}', sent))
                        words_in_new = set(re.findall(r'[\u4e00-\u9fff]{2,}', new_info))
                        common_words = words_in_sent & words_in_new
                        if len(common_words) >= 3:
                            issues.append(f"【重复】题干与已知信息内容重复：题干句子'{sent[:50]}...'与已知信息高度相似。题干不能描述反应步骤，已知信息不能重复题干内容")
                            break
                
                # 检查结构式是否重复
                stem_smiles = set(re.findall(r'\{结构式:([^}]+)\}', stem))
                new_info_smiles = set(re.findall(r'\{结构式:([^}]+)\}', new_info))
                overlap_smiles = stem_smiles & new_info_smiles
                if overlap_smiles:
                    issues.append(f"【重复】题干与已知信息使用了相同的结构式（共{len(overlap_smiles)}个），已知信息必须提供全新反应")
        
        # === 2. 题目 vs 答案重复检测 ===
        for q in questions:
            q_num = q.get("number", "?")
            q_content = str(q.get("content", ""))
            for a in answers:
                a_num = a.get("number", "?")
                a_content = str(a.get("content", ""))
                if q_num == a_num:
                    # 同题号的题目和答案对比
                    # 提取题目中的关键短语
                    q_keywords = re.findall(r'[\u4e00-\u9fff]{5,}', q_content)
                    a_keywords = re.findall(r'[\u4e00-\u9fff]{5,}', a_content)
                    # 如果答案中出现了题目的完整句子（超过10个字相同），说明重复
                    for qk in q_keywords:
                        if len(qk) >= 10 and qk in a_content:
                            issues.append(f"【重复】第{q_num}题答案中直接复述了题目内容'{qk[:30]}...'，答案不应重复题目设问")
                            break
        
        # === 3. 各小题之间的重复检测 ===
        for i in range(len(questions)):
            for j in range(i+1, len(questions)):
                qi = questions[i]
                qj = questions[j]
                ci = str(qi.get("content", ""))
                cj = str(qj.get("content", ""))
                # 提取关键短语
                ki = re.findall(r'[\u4e00-\u9fff]{5,}', ci)
                kj = re.findall(r'[\u4e00-\u9fff]{5,}', cj)
                common = len(set(ki) & set(kj))
                if common >= 3:
                    issues.append(f"【重复】第{qi.get('number')}题与第{qj.get('number')}题设问高度相似（{common}处相同），两题应该有区分度")
        
        # === 4. 题干 vs 答案重复检测 ===
        if stem:
            for a in answers:
                a_content = str(a.get("content", ""))
                a_num = a.get("number", "?")
                # 题干中不应出现 →[条件] 格式，但如果在答案中发现的格式也出现在题干中，说明重复
                stem_arrows = re.findall(r'→\s*\[([^\]]*)\]', stem)
                answer_arrows = re.findall(r'→\s*\[([^\]]*)\]', a_content)
                if stem_arrows and answer_arrows:
                    common_arrows = set(stem_arrows) & set(answer_arrows)
                    if common_arrows:
                        issues.append(f"【重复】题干与第{a_num}题答案中出现了相同的反应条件→{[list(common_arrows)[0][:30]]}...，题干不能包含路线步骤")
        
        return issues

    def _global_format_check(self, question_data: dict) -> list:
        """
        🔴 全局格式扫描：检查所有字段中的格式错误。
        覆盖 stem、questions、answers、new_info、analysis 等所有文本字段。
        检查项：
        1. A＋B→C / A+B→C 格式（全角/半角加号）
        2. 文字描述反应（"在...条件下反应得""与...反应生成"等）
        3. 箭头后无条件方括号（→ 后不是 [条件]）
        4. 条件方括号内为空
        """
        import re
        issues = []
        
        # 收集所有需要检查的文本
        texts_to_check = []
        
        if "stem" in question_data:
            texts_to_check.append(("题干", str(question_data["stem"])))
        if "new_info" in question_data and question_data["new_info"]:
            texts_to_check.append(("已知信息", str(question_data["new_info"])))
        if "analysis" in question_data and question_data["analysis"]:
            texts_to_check.append(("解析", str(question_data["analysis"])))
        
        if "questions" in question_data:
            for q in question_data["questions"]:
                texts_to_check.append((f"第{q.get('number', '?')}题", str(q.get("content", ""))))
        
        if "answers" in question_data:
            for a in question_data["answers"]:
                texts_to_check.append((f"第{a.get('number', '?')}题答案", str(a.get("content", ""))))
        
        for field_name, text in texts_to_check:
            if not text or len(text) < 3:
                continue
            
            # === 1. 检查 A＋B→C 或 A+B→C 格式（全角和半角加号） ===
            if re.search(r'[＋+]', text):
                # 找到具体位置
                matches = re.findall(r'[^{{]*?[＋+][^}]*?→', text)
                for m in matches:
                    m_clean = m.strip()[:80]
                    issues.append(f"【严重】{field_name}中发现A+B→C格式：'{m_clean}...' —— 禁止使用＋/+号，第二个反应物必须写入条件方括号内！")
                    break  # 每个字段只报告一次
            
            # === 2. 检查文字描述反应（应使用→[条件]格式） ===
            # 检测"在...条件下反应/得/生成"、"与...反应生成"、"经...得"等文字描述
            text_desc_patterns = [
                (r'在.{0,10}条件下.{0,5}(?:反应|得|生成)', '在...条件下反应得'),
                (r'与.{0,10}反应.{0,5}(?:生成|得|制)', '与...反应生成'),
                (r'经.{0,10}(?:得|生成|制得)', '经...得'),
                (r'通过.{0,10}反应.{0,5}(?:生成|得)', '通过...反应生成'),
                (r'发生.{0,10}反应.{0,5}(?:生成|得)', '发生...反应生成'),
                (r'用.{0,10}(?:处理|氧化|还原|硝化|酯化|水解|酰化).{0,5}(?:得|生成)', '用...处理得'),
            ]
            for pattern, desc in text_desc_patterns:
                if re.search(pattern, text):
                    # 确认不是题目设问中的条件描述（如"在下列条件下能发生反应的是"）
                    if not re.search(r'[能可][否以]|下列|选择|判断|满足|符合', text[max(0, text.find(re.search(pattern, text).group())-20):]):
                        issues.append(f"【严重】{field_name}中使用文字描述反应（{desc}），必须改为→[条件]格式！条件写在箭头上方方括号内")
                        break
            
            # === 3. 检查箭头后无条件方括号（仅当内容含结构式占位符或箭头时） ===
            has_structure = re.search(r'\{结构式:', text)
            has_arrow = re.search(r'→', text)
            if has_structure or has_arrow:
                # 情况A：有→但没有→[条件]格式
                if has_arrow and not re.search(r'→\s*\[', text):
                    # 排除题目设问中的箭头（如"→[条件]"本身是格式说明）
                    if not re.search(r'→\s*\[条件\]', text):
                        issues.append(f"【严重】{field_name}中有箭头→但没有→[条件]方括号格式，条件必须写在箭头上方方括号内！")
                
                # 情况B：有结构式占位符但没有箭头（可能是纯文字描述）
                if has_structure and not has_arrow:
                    # 检查是否包含反应描述关键词
                    reaction_keywords = ['反应', '硝化', '还原', '氧化', '酯化', '水解', '酰化', '取代', '加成', '消去', '缩合', '溴代', '氯化']
                    if any(kw in text for kw in reaction_keywords):
                        issues.append(f"【严重】{field_name}中有结构式但用文字描述反应，必须使用→[条件]格式！")
            
            # === 4. 检查条件方括号内是否为空 ===
            empty_conds = re.findall(r'→\s*\[\s*\]', text)
            if empty_conds:
                issues.append(f"【严重】{field_name}中有空条件方括号→[]，必须填写具体反应条件！")
            
            # === 5. 🔴 检查花括号代替方括号（→{条件}错误格式） ===
            curly_conds = re.findall(r'→\s*\{([^}]*)\}', text)
            if curly_conds:
                issues.append(f"【严重】{field_name}中使用了花括号→{{条件}}，必须改为方括号→[条件]！条件写在箭头上方必须用方括号[]")
        
        return issues

    def _final_format_audit(self, question_data: dict) -> dict:
        """
        🔴 终审格式审计：生成完成后对答案格式做最终确认。
        逐项检查每个答案和已知信息，返回明确的通过/不通过报告。
        这是格式合规的最后一道关卡，确保符合高考要求。
        """
        import re
        items = []  # 每项检查结果
        all_pass = True
        
        answers = question_data.get("answers", [])
        new_info = str(question_data.get("new_info", ""))
        
        # === 1. 已知信息格式检查 ===
        if new_info and new_info != "None" and len(new_info) > 5:
            item = {"field": "已知信息(new_info)", "checks": []}
            # 1a. 结构式占位符
            has_placeholder = bool(re.search(r'\{结构式:', new_info))
            item["checks"].append({
                "check": "包含结构式占位符",
                "pass": has_placeholder,
                "detail": "✓" if has_placeholder else "缺少 {{结构式:SMILES}}"
            })
            if not has_placeholder:
                all_pass = False
            
            # 1b. →[条件]格式
            has_arrow_bracket = bool(re.search(r'→\s*\[', new_info))
            item["checks"].append({
                "check": "使用→[条件]格式",
                "pass": has_arrow_bracket,
                "detail": "✓" if has_arrow_bracket else "未使用→[条件]格式"
            })
            if not has_arrow_bracket:
                all_pass = False
            
            # 1c. 无A+B→C格式
            has_plus = bool(re.search(r'[＋+]', new_info))
            item["checks"].append({
                "check": "无A+B→C格式",
                "pass": not has_plus,
                "detail": "✓" if not has_plus else "存在A+B→C格式，第二个反应物应写入条件"
            })
            if has_plus:
                all_pass = False
            
            # 1d. 无文字描述
            has_text_desc = bool(re.search(r'在.{0,10}条件下.{0,5}(?:反应|得|生成)|与.{0,10}反应.{0,5}(?:生成|得)', new_info))
            item["checks"].append({
                "check": "无文字描述反应",
                "pass": not has_text_desc,
                "detail": "✓" if not has_text_desc else "使用了文字描述反应，应改为→[条件]格式"
            })
            if has_text_desc:
                all_pass = False
            
            # 1e. 条件编号
            conds = re.findall(r'→\s*\[([^\]]*)\]', new_info)
            for cond in conds:
                has2 = bool(re.search(r'\(2\)', cond))
                has1 = bool(re.search(r'\(1\)', cond))
                if has2 and not has1:
                    item["checks"].append({
                        "check": "条件编号完整",
                        "pass": False,
                        "detail": f"有(2)无(1)：→[{cond}]"
                    })
                    all_pass = False
            
            # 1f. 🔴 花括号检查
            has_curly = bool(re.search(r'→\s*\{', new_info))
            item["checks"].append({
                "check": "使用方括号[]而非花括号{}",
                "pass": not has_curly,
                "detail": "✓" if not has_curly else "使用了花括号→{条件}，必须改为方括号→[条件]"
            })
            if has_curly:
                all_pass = False
            
            items.append(item)
        
        # === 2. 逐题答案格式检查 ===
        for a in answers:
            num = a.get("number", "?")
            content = str(a.get("content", ""))
            item = {"field": f"第{num}题答案", "checks": []}
            
            # 第1题和第4题通常不涉及方程式，跳过严格格式检查
            if num in [1, "1", 4, "4"]:
                # 但仍检查是否有格式问题
                if re.search(r'[＋+]', content):
                    item["checks"].append({
                        "check": "无A+B→C格式",
                        "pass": False,
                        "detail": "存在A+B→C格式"
                    })
                    all_pass = False
                items.append(item)
                continue
            
            # 第2、3、5题：必须检查方程式格式
            has_structure = bool(re.search(r'\{结构式:', content))
            has_arrow = bool(re.search(r'→', content))
            
            if has_structure or has_arrow:
                # 2a. →[条件]格式
                has_arrow_bracket = bool(re.search(r'→\s*\[', content))
                if has_arrow:
                    item["checks"].append({
                        "check": "使用→[条件]格式（条件在箭头上方）",
                        "pass": has_arrow_bracket,
                        "detail": "✓" if has_arrow_bracket else "箭头后缺少[条件]方括号"
                    })
                    if not has_arrow_bracket:
                        all_pass = False
                
                # 2b. 无A+B→C格式
                has_plus = bool(re.search(r'[＋+]', content))
                item["checks"].append({
                    "check": "无A+B→C格式",
                    "pass": not has_plus,
                    "detail": "✓" if not has_plus else "存在A+B→C格式，第二个反应物应写入条件"
                })
                if has_plus:
                    all_pass = False
                
                # 2c. 无文字描述
                has_text_desc = bool(re.search(r'在.{0,10}条件下.{0,5}(?:反应|得|生成)|与.{0,10}反应.{0,5}(?:生成|得)', content))
                item["checks"].append({
                    "check": "无文字描述反应",
                    "pass": not has_text_desc,
                    "detail": "✓" if not has_text_desc else "使用了文字描述反应"
                })
                if has_text_desc:
                    all_pass = False
                
                # 2d. 条件编号规则
                conds = re.findall(r'→\s*\[([^\]]*)\]', content)
                for cond in conds:
                    has2 = bool(re.search(r'\(2\)', cond))
                    has1 = bool(re.search(r'\(1\)', cond))
                    has3 = bool(re.search(r'\(3\)', cond))
                    if has2 and not has1:
                        item["checks"].append({
                            "check": "条件编号完整",
                            "pass": False,
                            "detail": f"有(2)无(1)：→[{cond}]"
                        })
                        all_pass = False
                    if has3 and (not has1 or not has2):
                        item["checks"].append({
                            "check": "条件编号完整",
                            "pass": False,
                            "detail": f"有(3)但缺(1)或(2)：→[{cond}]"
                        })
                        all_pass = False
                
                # 2e. 条件冗余词检查
                verbose_patterns = ['加热回流', '搅拌', '室温', '过夜', '滴加', '催化', '溶液中', '作用下', '条件下']
                for cond in conds:
                    found_verbose = [v for v in verbose_patterns if v in cond]
                    if found_verbose:
                        item["checks"].append({
                            "check": "条件极简（无冗余词）",
                            "pass": False,
                            "detail": f"→[{cond}] 含冗余词：{', '.join(found_verbose)}"
                        })
                        all_pass = False
                        break
                
                # 2f. 🔴 花括号检查
                has_curly = bool(re.search(r'→\s*\{', content))
                item["checks"].append({
                    "check": "使用方括号[]而非花括号{}",
                    "pass": not has_curly,
                    "detail": "✓" if not has_curly else "→{条件}必须改为→[条件]（方括号！）"
                })
                if has_curly:
                    all_pass = False
            
            # 第5题额外检查
            if num in [5, "5"]:
                # 步骤数
                step_matches = re.findall(r'第(\d+)步|步骤(\d+)', content)
                step_count = len(step_matches)
                if step_count == 0:
                    step_count = len(re.findall(r'→\s*\[', content))
                in_range = 5 <= step_count <= 7
                item["checks"].append({
                    "check": f"步骤数5-7步（当前{step_count}步）",
                    "pass": in_range,
                    "detail": "✓" if in_range else f"步骤数{step_count}步不符合5-7步要求"
                })
                if not in_range:
                    all_pass = False
                
                # 每步条件检查
                steps_no_cond = 0
                for i in range(1, step_count + 1):
                    pattern = re.compile(rf'第{i}步[：:]\s*(.*?)(?=第\d+步[：:]|$)', re.DOTALL)
                    sm = pattern.search(content)
                    if sm:
                        step_text = sm.group(1)
                        if not re.search(r'→\s*\[([^\]]+)\]', step_text):
                            steps_no_cond += 1
                if steps_no_cond > 0:
                    item["checks"].append({
                        "check": "每步都有反应条件",
                        "pass": False,
                        "detail": f"有{steps_no_cond}步缺少条件"
                    })
                    all_pass = False
            
            items.append(item)
        
        return {
            "all_pass": all_pass,
            "status": "✅ 全部格式检查通过，符合高考要求" if all_pass else "❌ 存在格式问题，请查看详情",
            "items": items,
            "total_checks": sum(len(item["checks"]) for item in items),
            "failed_checks": sum(
                sum(1 for c in item["checks"] if not c["pass"])
                for item in items
            ),
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