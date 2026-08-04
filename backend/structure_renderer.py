"""
化学结构式渲染服务
使用 RDKit 将 SMILES 转换为 ChemDraw 风格的 SVG/PNG 结构图
支持 PubChem API 在线查询，任意化合物名称→结构式
"""
import io
import json
import base64
import urllib.request
import urllib.parse
from typing import List, Optional, Tuple
from rdkit import Chem
from rdkit.Chem import Draw, AllChem
from rdkit.Chem.Draw import rdMolDraw2D


class StructureRenderer:
    """ChemDraw风格结构式渲染器"""

    # 查询缓存
    _cache = {}

    # ================================================================
    # 内置常见化合物映射（无需联网，覆盖高中化学全部常见化合物）
    # ================================================================
    BUILTIN_NAMES = {
        # === 基础烃类 ===
        "苯": "c1ccccc1", "甲苯": "Cc1ccccc1", "苯酚": "Oc1ccccc1",
        "苯胺": "Nc1ccccc1", "硝基苯": "O=[N+]([O-])c1ccccc1",
        "苯甲酸": "O=C(O)c1ccccc1", "苯甲醛": "O=Cc1ccccc1",
        "苯甲醇": "OCc1ccccc1", "苯乙酮": "CC(=O)c1ccccc1",
        "氯苯": "Clc1ccccc1", "溴苯": "Brc1ccccc1", "碘苯": "Ic1ccccc1",
        "苯乙烯": "C=Cc1ccccc1", "苯乙炔": "C#Cc1ccccc1",
        "苯磺酸": "O=S(=O)(O)c1ccccc1", "苯甲醚": "COc1ccccc1",
        "苯甲酰氯": "O=C(Cl)c1ccccc1", "苯乙腈": "N#CCc1ccccc1",
        "苯肼": "NNc1ccccc1", "苯甲酰胺": "NC(=O)c1ccccc1",
        "苯磺酰氯": "O=S(=O)(Cl)c1ccccc1",
        "苯乙醚": "CCOc1ccccc1", "苯乙醛": "O=CCc1ccccc1",
        "苯乙酸": "O=C(O)Cc1ccccc1",
        "氯化苄": "ClCc1ccccc1", "苄醇": "OCc1ccccc1",
        "联苯": "c1ccc(-c2ccccc2)cc1",
        "二苯甲酮": "O=C(c1ccccc1)c1ccccc1",
        "二苯甲醇": "OC(c1ccccc1)c1ccccc1",
        "三苯甲醇": "OC(c1ccccc1)(c1ccccc1)c1ccccc1",
        "偶氮苯": "N(=N/c1ccccc1)\\c1ccccc1",
        "联苯胺": "Nc1ccc(-c2ccc(N)cc2)cc1",
        "水杨酸": "O=C(O)c1ccccc1O",
        "乙酰水杨酸": "CC(=O)Oc1ccccc1C(=O)O",
        "对乙酰氨基酚": "CC(=O)Nc1ccc(O)cc1",
        "乙酰苯胺": "CC(=O)Nc1ccccc1",
        "N-苯基乙酰胺": "CC(=O)Nc1ccccc1",
        "N-苯基苯甲酰胺": "O=C(Nc1ccccc1)c1ccccc1",
        "肉桂酸": "O=C(O)/C=C/c1ccccc1",
        "肉桂醛": "O=C/C=C/c1ccccc1",
        "肉桂醇": "OC/C=C/c1ccccc1",

        # === 萘/蒽/菲 ===
        "萘": "c1ccc2ccccc2c1", "蒽": "c1ccc2cc3ccccc3cc2c1",
        "菲": "c1ccc2c(c1)ccc1ccccc12",
        "芴": "c1ccc2c(c1)Cc1ccccc12", "芘": "c1cc2ccc3cccc4ccc(c1)c2c34",

        # === 基础脂肪族 ===
        "乙酸": "CC(=O)O", "乙醇": "CCO", "乙酸乙酯": "CCOC(=O)C",
        "乙醛": "CC=O", "丙酮": "CC(=O)C", "甲醛": "C=O",
        "甲酸": "O=CO", "甲醇": "CO", "乙二醇": "OCCO",
        "甘油": "OCC(O)CO", "乙烯": "C=C", "乙炔": "C#C",
        "乙酰氯": "CC(=O)Cl", "乙酸酐": "CC(=O)OC(=O)C",
        "丙酸": "CCC(=O)O", "丁酸": "CCCC(=O)O",
        "戊酸": "CCCCC(=O)O", "己酸": "CCCCCC(=O)O",
        "草酸": "O=C(O)C(=O)O", "丙二酸": "O=C(O)CC(=O)O",
        "丁二酸": "O=C(O)CCC(=O)O", "戊二酸": "O=C(O)CCCC(=O)O",
        "己二酸": "O=C(O)CCCCC(=O)O",
        "马来酸": "O=C(O)/C=C\\C(=O)O", "富马酸": "O=C(O)/C=C/C(=O)O",
        "乳酸": "CC(O)C(=O)O", "苹果酸": "O=C(O)C(O)CC(=O)O",
        "酒石酸": "O=C(O)C(O)C(O)C(=O)O",
        "柠檬酸": "O=C(O)CC(O)(CC(=O)O)C(=O)O",
        "尿素": "NC(=O)N",

        # === 环烷烃 ===
        "环丙烷": "C1CC1", "环丁烷": "C1CCC1", "环戊烷": "C1CCCC1",
        "环己烷": "C1CCCCC1", "环己烯": "C1CCC=CC1",
        "环庚烷": "C1CCCCCC1", "环辛烷": "C1CCCCCCC1",
        "金刚烷": "C1C2CC3CC1CC(C2)C3", "立方烷": "C12C3C4C1C5C2C3C45",
        "降冰片烷": "C1CC2CCC1C2",
        "螺[2.2]戊烷": "C1CC12CC2",
        "樟脑": "CC1(C)[C@@H]2CC[C@@]1(C)C(=O)C2",
        "薄荷醇": "CC(C)[C@@H]1CC[C@@H](C)C[C@@H]1O",
        "蒎烯": "CC1=CC[C@@H]2C(C)(C)[C@H]1C2",

        # === 杂环 ===
        "吡啶": "c1ccncc1", "呋喃": "c1ccoc1",
        "噻吩": "c1ccsc1", "吡咯": "c1cc[nH]c1",
        "吲哚": "c1ccc2[nH]ccc2c1", "喹啉": "c1ccc2ncccc2c1",
        "异喹啉": "c1ccc2cnccc2c1", "嘌呤": "c1[nH]c2ncncc2n1",
        "嘧啶": "c1cncnc1", "吡嗪": "c1cnccn1", "哒嗪": "c1ccnnc1",
        "吲唑": "c1ccc2[nH]ncc2c1", "苯并咪唑": "c1ccc2[nH]cnc2c1",
        "苯并噻唑": "c1ccc2scnc2c1", "苯并噁唑": "c1ccc2ocnc2c1",
        "咔唑": "c1ccc2c(c1)[nH]c1ccccc12",
        "二苯并呋喃": "c1ccc2c(c1)oc1ccccc12",
        "二苯并噻吩": "c1ccc2c(c1)sc1ccccc12",
        "吖啶": "c1ccc2nc3ccccc3cc2c1",
        "吩噻嗪": "c1ccc2Sc3ccccc3Nc2c1",

        # === 氨基酸 ===
        "甘氨酸": "NCC(=O)O", "丙氨酸": "N[C@@H](C)C(=O)O",
        "丝氨酸": "N[C@@H](CO)C(=O)O", "半胱氨酸": "N[C@@H](CS)C(=O)O",
        "赖氨酸": "NCCCC[C@H](N)C(=O)O", "谷氨酸": "N[C@@H](CCC(=O)O)C(=O)O",
        "天冬氨酸": "N[C@@H](CC(=O)O)C(=O)O", "酪氨酸": "N[C@@H](Cc1ccc(O)cc1)C(=O)O",
        "色氨酸": "N[C@@H](Cc1c[nH]c2ccccc12)C(=O)O",
        "组氨酸": "N[C@@H](Cc1c[nH]cn1)C(=O)O",
        "脯氨酸": "O=C(O)[C@@H]1CCCN1",
        "苯丙氨酸": "N[C@@H](Cc1ccccc1)C(=O)O",
        "苯甘氨酸": "N[C@@H](C(=O)O)c1ccccc1",

        # === 葡萄糖 ===
        "葡萄糖": "OC[C@@H](O)[C@@H](O)[C@H](O)[C@@H](O)C=O",

        # === 二甲苯 ===
        "邻二甲苯": "Cc1ccccc1C", "间二甲苯": "Cc1cccc(C)c1", "对二甲苯": "Cc1ccc(C)cc1",

        # === 苯二甲酸/酐 ===
        "邻苯二甲酸": "O=C(O)c1ccccc1C(=O)O",
        "间苯二甲酸": "O=C(O)c1cccc(C(=O)O)c1",
        "对苯二甲酸": "O=C(O)c1ccc(C(=O)O)cc1",
        "均苯三甲酸": "O=C(O)c1cc(C(=O)O)cc(C(=O)O)c1",
        "邻苯二甲酸酐": "O=C1OC(=O)c2ccccc12",
        "丁二酸酐": "O=C1CCC(=O)O1", "马来酸酐": "O=C1C=CC(=O)O1",
        "苯甲酸酐": "O=C(OC(=O)c1ccccc1)c1ccccc1",

        # === 苯二酚/苯二胺 ===
        "邻苯二酚": "Oc1ccccc1O", "间苯二酚": "Oc1cccc(O)c1", "对苯二酚": "Oc1ccc(O)cc1",
        "对苯二胺": "Nc1ccc(N)cc1", "间苯二胺": "Nc1cccc(N)c1",

        # === 对苯二甲酰氯 ===
        "对苯二甲酰氯": "O=C(Cl)c1ccc(C(=O)Cl)cc1",
        "间苯二甲酰氯": "O=C(Cl)c1cccc(C(=O)Cl)c1",

        # === 茴香醚/苯乙醚 ===
        "茴香醚": "COc1ccccc1", "苯乙醚": "CCOc1ccccc1",

        # === 酯类 ===
        "苯甲酸甲酯": "COC(=O)c1ccccc1",
        "苯甲酸乙酯": "CCOC(=O)c1ccccc1",
        "苯甲酸苯酯": "O=C(Oc1ccccc1)c1ccccc1",
        "苯甲酸苄酯": "O=C(OCc1ccccc1)c1ccccc1",
        "苯乙酸乙酯": "CCOC(=O)Cc1ccccc1",
        "乙酸苯酯": "CC(=O)Oc1ccccc1",
        "乙酸苄酯": "CC(=O)OCc1ccccc1",
        "丙酸苯酯": "CCC(=O)Oc1ccccc1",
        "丁酸苯酯": "CCCC(=O)Oc1ccccc1",
        "碳酸二苯酯": "O=C(Oc1ccccc1)Oc1ccccc1",
        "水杨酸甲酯": "COC(=O)c1ccccc1O",
        "水杨酸苯酯": "O=C(Oc1ccccc1)c1ccccc1O",
        "水杨酰胺": "NC(=O)c1ccccc1O",
        "对羟基苯甲酸甲酯": "COC(=O)c1ccc(O)cc1",
        "对羟基苯甲酸乙酯": "CCOC(=O)c1ccc(O)cc1",
        "邻苯二甲酸二甲酯": "COC(=O)c1ccccc1C(=O)OC",
        "对苯二甲酸二甲酯": "COC(=O)c1ccc(C(=O)OC)cc1",

        # ================================================================
        # === 高中化学高频考点：多取代苯系物（硝基/氨基/羟基/羧基/酯基等组合） ===
        # ================================================================

        # --- 硝基甲苯系列 ---
        "邻硝基甲苯": "Cc1ccccc1[N+](=O)[O-]",
        "间硝基甲苯": "Cc1cccc([N+](=O)[O-])c1",
        "对硝基甲苯": "Cc1ccc([N+](=O)[O-])cc1",

        # --- 氨基甲苯系列 ---
        "对氨基甲苯": "Cc1ccc(N)cc1",

        # --- 卤代甲苯系列 ---
        "对氯甲苯": "Cc1ccc(Cl)cc1", "对溴甲苯": "Cc1ccc(Br)cc1",

        # --- 硝基苯酚系列 ---
        "邻硝基苯酚": "Oc1ccccc1[N+](=O)[O-]",
        "间硝基苯酚": "Oc1cccc([N+](=O)[O-])c1",
        "对硝基苯酚": "Oc1ccc([N+](=O)[O-])cc1",

        # --- 氨基苯酚系列 ---
        "邻氨基苯酚": "Nc1ccccc1O",
        "间氨基苯酚": "Nc1cccc(O)c1",
        "对氨基苯酚": "Nc1ccc(O)cc1",

        # --- 氯代苯酚系列 ---
        "邻氯苯酚": "Oc1ccccc1Cl",
        "间氯苯酚": "Oc1cccc(Cl)c1",
        "对氯苯酚": "Oc1ccc(Cl)cc1",
        "对溴苯酚": "Oc1ccc(Br)cc1",
        "对碘苯酚": "Oc1ccc(I)cc1",

        # --- 硝基苯胺系列 ---
        "邻硝基苯胺": "Nc1ccccc1[N+](=O)[O-]",
        "间硝基苯胺": "Nc1cccc([N+](=O)[O-])c1",
        "对硝基苯胺": "Nc1ccc([N+](=O)[O-])cc1",

        # --- 氯代苯胺系列 ---
        "间氯苯胺": "Nc1cccc(Cl)c1", "对氯苯胺": "Nc1ccc(Cl)cc1",

        # --- 硝基卤苯系列 ---
        "对硝基氯苯": "Clc1ccc([N+](=O)[O-])cc1",
        "对硝基溴苯": "Brc1ccc([N+](=O)[O-])cc1",
        "对硝基碘苯": "Ic1ccc([N+](=O)[O-])cc1",

        # --- 二硝基苯系列 ---
        "间二硝基苯": "O=[N+]([O-])c1cccc([N+](=O)[O-])c1",
        "对二硝基苯": "O=[N+]([O-])c1ccc([N+](=O)[O-])cc1",

        # --- 羟基苯甲酸/醛系列 ---
        "对羟基苯甲酸": "O=C(O)c1ccc(O)cc1",
        "间羟基苯甲酸": "O=C(O)c1cccc(O)c1",
        "对羟基苯甲醛": "O=Cc1ccc(O)cc1",
        "间羟基苯甲醛": "O=Cc1cccc(O)c1",

        # --- 氨基苯甲酸系列 ---
        "对氨基苯甲酸": "Nc1ccc(C(=O)O)cc1",
        "间氨基苯甲酸": "Nc1cccc(C(=O)O)c1",

        # --- 硝基苯甲酸系列（高频考点） ---
        "对硝基苯甲酸": "O=[N+]([O-])c1ccc(C(=O)O)cc1",
        "间硝基苯甲酸": "O=[N+]([O-])c1cccc(C(=O)O)c1",
        "邻硝基苯甲酸": "O=[N+]([O-])c1ccccc1C(=O)O",

        # --- 硝基苯甲醇系列（高频考点） ---
        "对硝基苯甲醇": "O=[N+]([O-])c1ccc(CO)cc1",
        "间硝基苯甲醇": "O=[N+]([O-])c1cccc(CO)c1",
        "邻硝基苯甲醇": "O=[N+]([O-])c1ccccc1CO",

        # --- 硝基苯甲醛系列 ---
        "对硝基苯甲醛": "O=[N+]([O-])c1ccc(C=O)cc1",
        "间硝基苯甲醛": "O=[N+]([O-])c1cccc(C=O)c1",

        # --- 氨基苯甲醇系列 ---
        "对氨基苯甲醇": "Nc1ccc(CO)cc1",
        "间氨基苯甲醇": "Nc1cccc(CO)c1",
        "对氨基苯甲醛": "Nc1ccc(C=O)cc1",

        # --- 硝基苯甲酸甲酯/乙酯系列（高频考点） ---
        "对硝基苯甲酸甲酯": "COC(=O)c1ccc([N+](=O)[O-])cc1",
        "对硝基苯甲酸乙酯": "CCOC(=O)c1ccc([N+](=O)[O-])cc1",
        "间硝基苯甲酸甲酯": "COC(=O)c1cccc([N+](=O)[O-])c1",
        "邻硝基苯甲酸甲酯": "COC(=O)c1ccccc1[N+](=O)[O-]",

        # --- 氨基苯甲酸甲酯/乙酯系列（高频考点） ---
        "对氨基苯甲酸甲酯": "COC(=O)c1ccc(N)cc1",
        "对氨基苯甲酸乙酯": "CCOC(=O)c1ccc(N)cc1",
        "间氨基苯甲酸甲酯": "COC(=O)c1cccc(N)c1",

        # --- 乙酰氨基苯甲酸系列（高频考点） ---
        "对乙酰氨基苯甲酸": "CC(=O)Nc1ccc(C(=O)O)cc1",
        "间乙酰氨基苯甲酸": "CC(=O)Nc1cccc(C(=O)O)c1",

        # --- 乙酰氨基苯甲酸酯系列 ---
        "对乙酰氨基苯甲酸甲酯": "COC(=O)c1ccc(NC(C)=O)cc1",
        "对乙酰氨基苯甲酸乙酯": "CCOC(=O)c1ccc(NC(C)=O)cc1",

        # --- 羟基苯甲酸酯系列 ---
        "对羟基苯甲酸甲酯": "COC(=O)c1ccc(O)cc1",
        "对羟基苯甲酸乙酯": "CCOC(=O)c1ccc(O)cc1",

        # --- 甲氧基苯系列 ---
        "对甲氧基苯甲醛": "COc1ccc(C=O)cc1",
        "对甲氧基苯甲酸": "COc1ccc(C(=O)O)cc1",
        "对甲氧基苯酚": "COc1ccc(O)cc1",
        "间甲氧基苯酚": "COc1cccc(O)c1",
        "对甲氧基苯胺": "COc1ccc(N)cc1",

        # --- 烷基苯酚系列 ---
        "对乙基苯酚": "CCc1ccc(O)cc1",
        "对异丙基苯酚": "CC(C)c1ccc(O)cc1",
        "对叔丁基苯酚": "CC(C)(C)c1ccc(O)cc1",

        # --- 多取代硝基/卤代苯酚 ---
        "2,4-二硝基苯酚": "Oc1ccc([N+](=O)[O-])cc1[N+](=O)[O-]",
        "2,4,6-三硝基苯酚": "Oc1c([N+](=O)[O-])cc([N+](=O)[O-])c([N+](=O)[O-])c1",
        "苦味酸": "O=[N+]([O-])c1c(O)c([N+](=O)[O-])cc([N+](=O)[O-])c1",
        "2,4-二硝基甲苯": "Cc1ccc([N+](=O)[O-])cc1[N+](=O)[O-]",
        "TNT": "Cc1c([N+](=O)[O-])cc([N+](=O)[O-])c([N+](=O)[O-])c1",
        "2,4-二氯苯酚": "Oc1ccc(Cl)cc1Cl",
        "2,4,6-三氯苯酚": "Oc1c(Cl)cc(Cl)c(Cl)c1",

        # --- 氰基/三氟甲基系列 ---
        "对氰基苯酚": "N#Cc1ccc(O)cc1",
        "对氰基苯甲酸": "N#Cc1ccc(C(=O)O)cc1",
        "对三氟甲基苯胺": "Nc1ccc(C(F)(F)F)cc1",
        "对三氟甲基苯酚": "Oc1ccc(C(F)(F)F)cc1",
        "对三氟甲基苯甲酸": "O=C(O)c1ccc(C(F)(F)F)cc1",

        # --- 碘代系列 ---
        "邻碘苯甲酸": "O=C(O)c1ccccc1I",
        "对碘苯甲酸": "O=C(O)c1ccc(I)cc1",

        # --- 对甲苯磺酸系列 ---
        "对甲苯磺酸": "Cc1ccc(S(=O)(=O)O)cc1",
        "对甲苯磺酰氯": "Cc1ccc(S(=O)(=O)Cl)cc1",

        # --- 偶联产物 ---
        "4-硝基联苯": "O=[N+]([O-])c1ccc(-c2ccccc2)cc1",
        "4-氨基联苯": "Nc1ccc(-c2ccccc2)cc1",
        "4-羟基联苯": "Oc1ccc(-c2ccccc2)cc1",
        "4-甲基联苯": "Cc1ccc(-c2ccccc2)cc1",
        "4-甲氧基联苯": "COc1ccc(-c2ccccc2)cc1",
        "4-氰基联苯": "N#Cc1ccc(-c2ccccc2)cc1",

        # === 含氮杂环 ===
        "2-氨基吡啶": "Nc1ccccn1", "3-氨基吡啶": "Nc1cccnc1", "4-氨基吡啶": "Nc1ccncc1",
        "2-氯吡啶": "Clc1ccccn1", "3-溴吡啶": "Brc1cccnc1",
        "2-甲基吡啶": "Cc1ccccn1", "3-甲基吡啶": "Cc1cccnc1", "4-甲基吡啶": "Cc1ccncc1",
        "2-吡啶甲酸": "O=C(O)c1ccccn1", "3-吡啶甲酸": "O=C(O)c1cccnc1", "4-吡啶甲酸": "O=C(O)c1ccncc1",
        "2-呋喃甲酸": "O=C(O)c1ccco1", "2-噻吩甲酸": "O=C(O)c1cccs1",
        "2-呋喃甲醛": "O=Cc1ccco1", "5-甲基呋喃甲醛": "Cc1ccc(C=O)o1",
        "吲哚-3-乙酸": "O=C(O)Cc1c[nH]c2ccccc12",
        "吲哚-3-甲醛": "O=Cc1c[nH]c2ccccc12",
        "5-溴吲哚": "Brc1ccc2[nH]ccc2c1", "5-硝基吲哚": "O=[N+]([O-])c1ccc2[nH]ccc2c1",
        "2-苯基吲哚": "c1ccc(-c2cc3ccccc3[nH]2)cc1",

        # === 手性化合物 ===
        "扁桃酸": "O=C(O)C(O)c1ccccc1",
        "R-扁桃酸": "O=C(O)[C@@H](O)c1ccccc1",
        "S-扁桃酸": "O=C(O)[C@H](O)c1ccccc1",
        "布洛芬": "CC(C)Cc1ccc(C(C)C(=O)O)cc1",
        "萘普生": "COc1ccc2cc(C(C)C(=O)O)ccc2c1",
        "酮洛芬": "O=C(c1ccccc1)c1ccc(C(C)C(=O)O)cc1",

        # === 保护基化合物 ===
        "Boc-苯胺": "CC(C)(C)OC(=O)Nc1ccccc1",
        "Cbz-苯胺": "O=C(OCc1ccccc1)Nc1ccccc1",
        "TBS-苯酚": "CC(C)(C)[Si](C)(C)Oc1ccccc1",

        # === 溶剂/试剂 ===
        "四氢呋喃": "C1CCOC1", "二氧六环": "C1COCCO1",
        "二甲基甲酰胺": "CN(C)C=O", "DMF": "CN(C)C=O",
        "二甲基亚砜": "CS(=O)C", "DMSO": "CS(=O)C",
        "N-甲基吡咯烷酮": "CN1CCCC1=O", "NMP": "CN1CCCC1=O",
        "六甲基磷酰三胺": "CN(C)P(=O)(N(C)C)N(C)C", "HMPA": "CN(C)P(=O)(N(C)C)N(C)C",
        "三乙胺": "CCN(CC)CC", "二氯甲烷": "ClCCl", "三氯甲烷": "ClC(Cl)Cl",
        "四氯化碳": "ClC(Cl)(Cl)Cl", "氯仿": "ClC(Cl)Cl",
        "正己烷": "CCCCCC", "石油醚": "CCCCCC",
        "乙醚": "CCOCC", "正丁醇": "CCCCO", "异丙醇": "CC(C)O", "叔丁醇": "CC(C)(C)O",
        "乙腈": "CC#N", "二甲苯": "Cc1ccc(C)cc1",
        "N,N-二甲基苯胺": "CN(C)c1ccccc1",
        "N,N-二乙基苯胺": "CCN(CC)c1ccccc1",
        "三苯基膦": "P(c1ccccc1)(c1ccccc1)c1ccccc1",
        "三苯基氧膦": "O=P(c1ccccc1)(c1ccccc1)c1ccccc1",
        "偶氮二甲酸二乙酯": "CCOC(=O)/N=N/C(=O)OCC", "DEAD": "CCOC(=O)/N=N/C(=O)OCC",
        "偶氮二甲酸二异丙酯": "CC(C)OC(=O)/N=N/C(=O)OC(C)C", "DIAD": "CC(C)OC(=O)/N=N/C(=O)OC(C)C",
        "N-溴代丁二酰亚胺": "O=C1CCC(=O)N1Br", "NBS": "O=C1CCC(=O)N1Br",
        "N-氯代丁二酰亚胺": "O=C1CCC(=O)N1Cl", "NCS": "O=C1CCC(=O)N1Cl",
        "间氯过氧苯甲酸": "O=C(OO)c1cccc(Cl)c1", "mCPBA": "O=C(OO)c1cccc(Cl)c1",
        "二异丙基氨基锂": "CC(C)N([Li])C(C)C", "LDA": "CC(C)N([Li])C(C)C",
        "二环己基碳二亚胺": "C1CCC(CC1)N=C=NC1CCCCC1", "DCC": "C1CCC(CC1)N=C=NC1CCCCC1",
        "EDC": "CCN=C=NCCCN(C)C",
        "4-二甲氨基吡啶": "CN(C)c1ccncc1", "DMAP": "CN(C)c1ccncc1",
        "1-羟基苯并三唑": "On1nnc2ccccc12", "HOBt": "On1nnc2ccccc12",
        "BOP": "F[P-](F)(F)(F)(F)F.CN(C)[P+](On1nnc2ccccc12)(N(C)C)N(C)C",
        "二碳酸二叔丁酯": "CC(C)(C)OC(=O)OC(=O)OC(C)(C)C", "Boc2O": "CC(C)(C)OC(=O)OC(=O)OC(C)(C)C",
        "氯甲酸苄酯": "O=C(Cl)OCc1ccccc1", "Cbz-Cl": "O=C(Cl)OCc1ccccc1",
        "9-芴甲氧羰基氯": "O=C(Cl)OCC1c2ccccc2-c2ccccc12", "Fmoc-Cl": "O=C(Cl)OCC1c2ccccc2-c2ccccc12",
        "叔丁基二甲基氯硅烷": "CC(C)(C)[Si](C)(C)Cl", "TBSCl": "CC(C)(C)[Si](C)(C)Cl",
        "三甲基氯硅烷": "C[Si](C)(C)Cl", "TMSCl": "C[Si](C)(C)Cl",
        "三乙基硅烷": "CC[SiH](CC)CC",
        "硼氢化钠": "[Na+].[BH4-]", "氢化铝锂": "[Li+].[AlH4-]",
        "硼烷-四氢呋喃": "B.C1CCOC1", "硼烷-二甲硫醚": "B.CSC",
        "氢化钠": "[NaH]",
        "正丁基锂": "CCCC[Li]", "叔丁基锂": "CC(C)(C)[Li]", "苯基锂": "[Li]c1ccccc1",
        "甲基溴化镁": "C[Mg]Br", "苯基溴化镁": "Br[Mg]c1ccccc1", "乙基溴化镁": "CC[Mg]Br",
        "碳酸钾": "[K+].[K+].[O-]C([O-])=O", "碳酸钠": "[Na+].[Na+].[O-]C([O-])=O",
        "碳酸氢钠": "[Na+].OC([O-])=O",
        "氢氧化钠": "[Na+].[OH-]", "氢氧化钾": "[K+].[OH-]",
        "三氟乙酸": "FC(F)(F)C(=O)O", "TFA": "FC(F)(F)C(=O)O",
        "三氟乙酸酐": "FC(F)(F)C(=O)OC(=O)C(F)(F)F", "TFAA": "FC(F)(F)C(=O)OC(=O)C(F)(F)F",
        "甲磺酰氯": "CS(=O)(=O)Cl", "MsCl": "CS(=O)(=O)Cl",
        "TsCl": "Cc1ccc(S(=O)(=O)Cl)cc1",
        "三氟甲磺酸酐": "FC(F)(F)S(=O)(=O)OS(=O)(=O)C(F)(F)F", "Tf2O": "FC(F)(F)S(=O)(=O)OS(=O)(=O)C(F)(F)F",
        "重氮甲烷": "C=[N+]=[N-]",
        "三甲基硅基重氮甲烷": "C[Si](C)(C)C=[N+]=[N-]",

        # === 常见药物 ===
        "扑热息痛": "CC(=O)Nc1ccc(O)cc1",
        "阿司匹林": "CC(=O)Oc1ccccc1C(=O)O",
        "非那西丁": "CCOc1ccc(NC(=O)C)cc1",
        "苯佐卡因": "CCOC(=O)c1ccc(N)cc1",
        "普鲁卡因": "CCN(CC)CCOC(=O)c1ccc(N)cc1",
        "利多卡因": "CCN(CC)CC(=O)Nc1c(C)cccc1C",
        "磺胺": "Nc1ccc(S(=O)(=O)N)cc1",
        "磺胺嘧啶": "Nc1ccc(S(=O)(=O)Nc2ncccn2)cc1",
        "磺胺甲噁唑": "Nc1ccc(S(=O)(=O)Nc2noc(C)c2)cc1",
        "磺胺吡啶": "Nc1ccc(S(=O)(=O)Nc2ccccn2)cc1",
        "磺胺噻唑": "Nc1ccc(S(=O)(=O)Nc2nccs2)cc1",
        "异烟肼": "NNC(=O)c1ccncc1",
        "吡嗪酰胺": "NC(=O)c1cnccn1",
        "甲硝唑": "CC1=NC=C([N+](=O)[O-])N1CCO",
        "咖啡因": "Cn1c(=O)n(C)c(=O)c2ncn(C)c12",
        "尼古丁": "c1ncccc1[C@@H]1CCCN1C",
        "吗啡": "CN1CC[C@@]23[C@@H]4Oc5c(O)ccc(C[C@@H]1[C@@H]2C=C[C@@H]4O)c35",
        "维生素C": "OC[C@@H](O)[C@H]1OC(=O)C(O)=C1O",
        "维生素B6": "CC1=NC=C(CO)C(CO)=C1O",
        "多巴胺": "NCCc1ccc(O)c(O)c1",
        "肾上腺素": "CNC[C@@H](O)c1ccc(O)c(O)c1",
        "褪黑素": "COc1ccc2[nH]cc(CCNC(=O)C)c2c1",
        "苯巴比妥": "CCC1(C(=O)NC(=O)NC1=O)c1ccccc1",
        "卡马西平": "NC(=O)N1c2ccccc2/C=C/c2ccccc12",
        "丙戊酸": "CCCC(CCC)C(=O)O",
        "双氯芬酸": "OC(=O)Cc1ccccc1Nc1c(Cl)cccc1Cl",
        "奥美拉唑": "COc1ccnc(CS(=O)c2nc3ccccc3[nH]2)c1C",
        "氯雷他定": "CCOC(=O)N1CCc2ccc(Cl)c3ccc(Cl)cc3c2C1",
        "西替利嗪": "OC(=O)CN1CCN(CCOCc2ccc(Cl)cc2)CC1",
        "塞来昔布": "Cc1nnc(S(=O)(=O)N)c1c1ccc(C(F)(F)F)cc1",
        "地西泮": "CN1C(=O)CN=C(c2ccccc2)c2cc(Cl)ccc12",
        "甲氧苄啶": "COc1c(OC)c(OC)cc(CCc2cnc(N)nc2N)c1",
        "三聚氰胺": "Nc1nc(N)nc(N)n1",
        "巴比妥酸": "O=C1CC(=O)NC(=O)N1",

        # === 农药/其他 ===
        "六六六": "ClC1C(Cl)C(Cl)C(Cl)C(Cl)C1Cl",
        "DDT": "Clc1ccc(C(c2ccc(Cl)cc2)C(Cl)(Cl)Cl)cc1",
        "六氯苯": "Clc1c(Cl)c(Cl)c(Cl)c(Cl)c1Cl",
        "三蝶烯": "c1ccc2c(c1)C1c3ccccc3C2c2ccccc12",
        "冠醚": "C1COCCOCCOCCOCCOC1", "18-冠-6": "C1COCCOCCOCCOCCOC1",
        "胆固醇": "C[C@H](CCCC(C)C)[C@H]1CC[C@@]2([H])[C@]3([H])CC=C4C[C@@H](O)CC[C@]4(C)[C@@]3([H])CC[C@]12C",
    }

    @staticmethod
    def _llm_name_to_smiles(name: str) -> Optional[str]:
        """
        LLM 智能回退：使用 DeepSeek 将化合物中文名转为 SMILES
        当内置词典和 PubChem 都查不到时调用
        """
        try:
            # 延迟导入避免循环依赖
            from llm_client import llm_client
            if not llm_client.is_available:
                return None

            prompt = f"""你是一位有机化学专家。请将以下化合物名称转换为标准的SMILES字符串。

化合物名称：{name}

规则：
1. 只返回SMILES字符串，不要任何其他文字
2. 如果是苯环衍生物，注意取代基的位置（邻/间/对位分别对应1,2-/1,3-/1,4-）
3. 硝基表示为 [N+](=O)[O-]
4. 酯基表示为 C(=O)OC 或 COC(=O)
5. 酰胺基表示为 NC(=O) 或 C(=O)N
6. 如果无法确定结构，返回 UNKNOWN

只输出SMILES字符串："""
            response = llm_client.generate(
                system_prompt="你是一个将化学名称转换为SMILES的工具。只输出SMILES字符串，不要任何解释。",
                user_prompt=prompt,
                temperature=0.0,
            )
            smiles = response.strip()
            # 验证是否为有效SMILES
            if smiles and smiles != "UNKNOWN" and len(smiles) > 1:
                mol = StructureRenderer.smiles_to_mol(smiles)
                if mol:
                    StructureRenderer._cache[name] = smiles
                    return smiles
        except Exception:
            pass
        return None

    @staticmethod
    def name_to_smiles_pubchem(name: str) -> Optional[str]:
        """
        通过 PubChem PUG REST API 查询化合物名称→SMILES
        支持中英文名称、IUPAC命名、商品名、俗名等
        回退链：内置词典 → PubChem API → LLM 智能推断
        """
        # 先检查缓存
        if name in StructureRenderer._cache:
            return StructureRenderer._cache[name]

        # 先检查内置映射
        if name in StructureRenderer.BUILTIN_NAMES:
            StructureRenderer._cache[name] = StructureRenderer.BUILTIN_NAMES[name]
            return StructureRenderer.BUILTIN_NAMES[name]

        # 尝试 PubChem API
        try:
            encoded_name = urllib.parse.quote(name)
            url = (
                f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
                f"{encoded_name}/property/CanonicalSMILES,IsomericSMILES/JSON"
            )
            req = urllib.request.Request(url, headers={"User-Agent": "ChemQuestionAgent/1.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if "PropertyTable" in data and "Properties" in data["PropertyTable"]:
                    props = data["PropertyTable"]["Properties"]
                    if props:
                        smiles = (
                            props[0].get("CanonicalSMILES") or
                            props[0].get("IsomericSMILES") or
                            props[0].get("SMILES") or
                            props[0].get("ConnectivitySMILES") or
                            ""
                        )
                        if smiles:
                            StructureRenderer._cache[name] = smiles
                            return smiles
        except urllib.error.HTTPError as e:
            if e.code == 404:
                pass
        except Exception:
            pass

        # LLM 智能回退：用 DeepSeek 推断 SMILES
        return StructureRenderer._llm_name_to_smiles(name)

    @staticmethod
    def search_compounds(keyword: str, limit: int = 10) -> List[dict]:
        """
        通过 PubChem API 搜索化合物（用于自动补全）
        """
        try:
            encoded = urllib.parse.quote(keyword)
            url = (
                f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
                f"{encoded}/cids/JSON?name_type=word"
            )
            req = urllib.request.Request(url, headers={"User-Agent": "ChemQuestionAgent/1.0"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if "IdentifierList" in data and "CID" in data["IdentifierList"]:
                    cids = data["IdentifierList"]["CID"][:limit]
                    # 获取标题
                    cid_str = ",".join(str(c) for c in cids)
                    url2 = (
                        f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/"
                        f"{cid_str}/description/JSON"
                    )
                    req2 = urllib.request.Request(url2, headers={"User-Agent": "ChemQuestionAgent/1.0"})
                    with urllib.request.urlopen(req2, timeout=5) as resp2:
                        data2 = json.loads(resp2.read().decode("utf-8"))
                        results = []
                        if "InformationList" in data2 and "Information" in data2["InformationList"]:
                            for info in data2["InformationList"]["Information"]:
                                results.append({
                                    "name": info.get("Title", ""),
                                    "cid": info.get("CID", 0),
                                })
                        return results
        except Exception:
            pass
        return []

    @staticmethod
    def name_to_smiles(name: str) -> Optional[str]:
        """化合物名称→SMILES（内置+PubChem在线查询）"""
        return StructureRenderer.name_to_smiles_pubchem(name)

    @staticmethod
    def smiles_to_mol(smiles: str) -> Optional[Chem.Mol]:
        """SMILES转分子对象"""
        try:
            mol = Chem.MolFromSmiles(smiles.strip())
            if mol is None:
                return None
            # 计算2D坐标
            AllChem.Compute2DCoords(mol)
            return mol
        except Exception:
            return None

    @staticmethod
    def render_svg(
        smiles: str,
        width: int = 400,
        height: int = 200,
        show_hydrogens: bool = False,
        label: str = "",
    ) -> str:
        """
        将SMILES渲染为SVG结构式（仿ChemDraw/高考真题风格）

        Args:
            smiles: SMILES字符串
            width: 图片宽度
            height: 图片高度
            show_hydrogens: 是否显示氢原子
            label: 化合物标签（显示在结构下方）

        Returns:
            SVG字符串
        """
        mol = StructureRenderer.smiles_to_mol(smiles)
        if mol is None:
            return f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg"><text x="10" y="20" font-size="12" fill="red">无法解析: {smiles}</text></svg>'

        drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
        # 使用系统字体目录，获得更好的字体渲染效果
        try:
            import platform
            if platform.system() == 'Windows':
                drawer.SetFontDir(r'C:\Windows\Fonts')
        except Exception:
            pass
        opts = drawer.drawOptions()
        # 仿真题ChemDraw风格参数（与路线图结构式保持一致）
        opts.bondLineWidth = 1.5          # 键线粗细（精细风格）
        opts.fixedBondLength = 30         # 固定键长
        opts.addStereoAnnotation = True
        opts.multipleBondOffset = 0.18    # 双键/三键偏移
        opts.prepareMolsBeforeDrawing = True
        opts.clearBackground = True
        opts.useBWAtomPalette()             # 黑白原子颜色（高考风格）
        opts.baseFontSize = 0.55           # 基础字号
        opts.additionalAtomLabelPadding = 0.08
        opts.minFontSize = 11
        if not show_hydrogens:
            opts.includeAtomTags = False

        if label:
            drawer.DrawMolecule(mol, legend=label)
        else:
            drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText()
        # RDKit 的 MolDraw2DSVG 输出带 svg: 命名空间前缀，在 HTML inline 中可能无法正常渲染
        # 去掉命名空间前缀，确保在浏览器中正确显示
        import re
        svg = re.sub(r'<(\/?)(svg:)(\w+)', r'<\1\3', svg)
        svg = re.sub(r'xmlns:svg=', 'xmlns=', svg)
        return svg

    @staticmethod
    def render_multiple_svg(
        compounds: List[dict],
        per_width: int = 300,
        per_height: int = 180,
    ) -> str:
        """
        渲染多个化合物并排排列（仿ChemDraw风格）

        Args:
            compounds: [{"smiles": "...", "label": "A"}, ...]
            per_width: 每个结构的宽度
            per_height: 每个结构的高度

        Returns:
            SVG字符串
        """
        mols = []
        labels = []
        for comp in compounds:
            smiles = comp.get("smiles", "")
            label = comp.get("label", "")
            mol = StructureRenderer.smiles_to_mol(smiles)
            if mol:
                mols.append(mol)
                labels.append(label)
            else:
                mols.append(None)
                labels.append(f"{label} (?)")

        if not mols:
            return ""

        n = len(mols)
        total_width = per_width * n

        drawer = rdMolDraw2D.MolDraw2DSVG(total_width, per_height, per_width, per_height)
        opts = drawer.drawOptions()
        opts.bondLineWidth = 2.0
        opts.fixedBondLength = 26
        opts.multipleBondOffset = 0.18

        valid_mols = [m for m in mols if m is not None]
        if valid_mols:
            drawer.DrawMolecules(valid_mols, legends=labels)

        drawer.FinishDrawing()
        return drawer.GetDrawingText()

    @staticmethod
    def render_reaction_svg(
        steps: List[dict],
        width: int = 800,
        height: int = 250,
    ) -> str:
        """
        渲染合成路线反应式（A → B → C → ...）（仿ChemDraw风格）

        Args:
            steps: [{"smiles": "c1ccccc1", "label": "A", "reagent": "HNO3/H2SO4"}, ...]
            width: 总宽度
            height: 高度

        Returns:
            SVG字符串
        """
        mols = []
        labels = []
        for step in steps:
            smiles = step.get("smiles", "")
            label = step.get("label", "")
            mol = StructureRenderer.smiles_to_mol(smiles)
            if mol:
                mols.append(mol)
                labels.append(label)

        if len(mols) < 2:
            return StructureRenderer.render_svg(
                steps[0].get("smiles", ""), width, height, label=steps[0].get("label", "")
            )

        n = len(mols)
        arrow_width = 60
        struct_width = (width - arrow_width * (n - 1)) // n

        drawer = rdMolDraw2D.MolDraw2DSVG(width, height, struct_width, height)
        opts = drawer.drawOptions()
        opts.bondLineWidth = 2.0
        opts.fixedBondLength = 26
        opts.multipleBondOffset = 0.18

        drawer.DrawMolecules(mols, legends=labels)
        drawer.FinishDrawing()
        return drawer.GetDrawingText()

    @staticmethod
    def _format_reagent(text: str) -> str:
        """美化试剂文本：化学式数字→Unicode下标"""
        if not text:
            return text
        sub_map = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')
        result = []
        i = 0
        while i < len(text):
            ch = text[i]
            if ch.isdigit() and i > 0:
                prev = text[i-1]
                if prev.isalpha() or prev in ')]}':
                    j = i
                    while j < len(text) and text[j].isdigit():
                        j += 1
                    result.append(text[i:j].translate(sub_map))
                    i = j
                    continue
            result.append(ch)
            i += 1
        return ''.join(result)

    @staticmethod
    def _mol_to_svg_content(mol, width: int, height: int) -> str:
        """
        将RDKit分子渲染为SVG内容片段（用于嵌入路线图）
        使用MolDraw2DSVG获得高质量矢量结构式
        """
        import re
        drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
        # 尝试使用系统字体目录，让原子标签使用更好的字体
        try:
            import platform
            if platform.system() == 'Windows':
                drawer.SetFontDir(r'C:\Windows\Fonts')
        except Exception:
            pass
        opts = drawer.drawOptions()
        # 仿真题ChemDraw风格参数
        opts.bondLineWidth = 1.5          # 键线粗细（精细风格）
        opts.fixedBondLength = 30         # 固定键长
        opts.addStereoAnnotation = True
        opts.multipleBondOffset = 0.18    # 双键/三键偏移
        opts.includeAtomTags = False
        opts.prepareMolsBeforeDrawing = True
        opts.clearBackground = True
        opts.useBWAtomPalette()             # 黑白原子颜色（高考风格）
        opts.baseFontSize = 0.55           # 基础字号
        opts.additionalAtomLabelPadding = 0.08
        opts.minFontSize = 11
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText()
        # 提取内层SVG内容（去掉外层<svg:svg>标签）
        match = re.search(r'<svg:svg[^>]*>(.*?)</svg:svg>', svg, re.DOTALL)
        if match:
            return match.group(1)
        # 回退：尝试提取普通<svg>标签内容
        inner = re.sub(r'<\?xml[^>]*\?>', '', svg)
        inner = re.sub(r'<svg[^>]*>', '', inner)
        inner = re.sub(r'</svg>', '', inner)
        return inner

    @staticmethod
    def render_route_diagram_svg(
        steps: List[dict],
        title: str = "",
    ) -> str:
        """
        渲染合成路线图 — 严格仿照江苏高考真题格式

        真题特征（经2022/2023/2024真题图片分析确认）：
        2024: 主路线图 10.93×4.82cm 单行
        2022: 主路线图 14.55×3.49cm 单行极宽
        2023: 主路线图 12.65×14.13cm 多行

        格式特征：
        - 纯白背景，无灰底面板，无边框
        - 结构式用标准键线式（ChemDraw风格），杂原子显式标注
        - 黑色细箭头(→)，箭头上方标注试剂/条件
        - 化合物编号(A/B/C...)在结构正下方，Times New Roman粗体
        - 5步以上自动换2行，行间用竖直箭头连接
        - 结构式紧凑排列，仿真题比例
        """
        n = len(steps)
        if n == 0:
            return ''

        # === 判断是否换行及分行规则 ===
        # 5步以内单行；6-10步双行U字形，按步数定制分行：
        #   6步: 3+3    7步: 4+3    8步: 5+4
        #   9步: 5+5    10步: 6+5
        if n <= 5:
            rows = [(0, n)]
        elif n == 6:
            rows = [(0, 3), (3, 6)]
        elif n == 7:
            rows = [(0, 4), (4, 7)]
        elif n == 8:
            rows = [(0, 5), (5, 8)]
        elif n == 9:
            rows = [(0, 5), (5, 9)]
        elif n == 10:
            rows = [(0, 6), (6, 10)]
        else:
            # 超过10步，前一半+1放第一行，其余放第二行
            mid = (n + 1) // 2
            rows = [(0, mid), (mid, n)]

        # === 布局参数（仿真题比例，兼顾可读性） ===
        struct_w = 160       # 结构式宽
        struct_h = 120       # 结构式高
        min_arrow_w = 90     # 最小箭头宽度
        top_margin = 56      # 顶留白（试剂标注在箭头上方）
        bottom_margin = 34   # 底留白（化合物编号）
        side_margin = 28     # 左右留白
        row_gap = 76         # 行间距

        row_total_h = struct_h + top_margin + bottom_margin

        # === 根据文字长度动态计算每个箭头的宽度 ===
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

        def _estimate_text_width(text, font_size=12):
            """估算文本渲染宽度（px），微软雅黑中文字符约1.05×字号，ASCII约0.55×字号"""
            w = 0
            for ch in text:
                if '\u4e00' <= ch <= '\u9fff' or '\u3000' <= ch <= '\u303f' or '\uff00' <= ch <= '\uffef':
                    w += font_size * 1.05
                elif ch in '₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎':
                    w += font_size * 0.5
                else:
                    w += font_size * 0.55
            return max(w, 1)

        def _calc_arrow_width(reagent_text):
            """根据试剂文字估算需要的箭头宽度"""
            if not reagent_text:
                return min_arrow_w
            reagent = StructureRenderer._format_reagent(reagent_text)
            split = _split_reagent(reagent)
            all_lines = split.get("above", []) + split.get("below", [])
            max_text_w = max(_estimate_text_width(line, 12) for line in all_lines) if all_lines else 0
            # 箭头区 = 文字宽度 + 箭头尖(18px) + 两侧留白(40px)
            return max(int(max_text_w + 58), min_arrow_w)

        # 预计算每个箭头的宽度（steps[i]的reagent是到下一个化合物的箭头）
        arrow_widths = []
        for i in range(n - 1):
            reagent = steps[i + 1].get("reagent", "")
            arrow_widths.append(_calc_arrow_width(reagent))

        # 分行并计算每行的x位置
        row_positions = []  # 每个化合物的 x 坐标

        for ri, (start, end) in enumerate(rows):
            if ri == 0:
                # 第一行：左到右，从 side_margin 开始
                positions = []
                x = side_margin
                for j in range(start, end):
                    positions.append(x)
                    x += struct_w
                    if j < end - 1:
                        x += arrow_widths[j]
            else:
                # 第二行：U字形，右到左（E在D正下方，箭头从右向左）
                positions = []
                x = prev_last_x
                for j in range(start, end):
                    positions.append(x)
                    x -= struct_w
                    if j < end - 1:
                        x -= arrow_widths[j]
            row_positions.append(positions)
            prev_last_x = positions[-1]

        # 计算画布尺寸，处理第二行可能出现的负坐标
        all_positions = [p for row_pos in row_positions for p in row_pos]
        min_x = min(all_positions) if all_positions else 0
        max_x = max(p + struct_w for p in all_positions) if all_positions else 0

        # 如果最左端超出画布左侧，整体右移
        if min_x < side_margin:
            offset = side_margin - min_x
            for ri in range(len(rows)):
                row_positions[ri] = [p + offset for p in row_positions[ri]]
            max_x += offset

        total_w = max_x + side_margin
        num_rows = len(rows)
        total_h = side_margin * 2 + row_total_h * num_rows + row_gap * (num_rows - 1)

        # === 构建 SVG ===
        svg_parts = [
            f'<svg width="{total_w}" height="{total_h}" '
            f'viewBox="0 0 {total_w} {total_h}" '
            f'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">',
        ]

        def _render_text_line(line, line_y, line_center):
            """渲染单行文本，△用大字号"""
            if '△' in line:
                parts = line.split('△')
                svg_parts.append(
                    f'<text x="{line_center}" y="{line_y}" '
                    f'text-anchor="middle" font-size="12" '
                    f'font-family="Microsoft YaHei,微软雅黑,SimHei,黑体,sans-serif" fill="#222">'
                    f'{parts[0]}<tspan font-size="24" baseline-shift="-3">△</tspan>{parts[1] if len(parts) > 1 else ""}'
                    f'</text>'
                )
            else:
                svg_parts.append(
                    f'<text x="{line_center}" y="{line_y}" '
                    f'text-anchor="middle" font-size="12" '
                    f'font-family="Microsoft YaHei,微软雅黑,SimHei,黑体,sans-serif" fill="#222">{line}</text>'
                )

        def _draw_arrow_right(x1, x2, base_y, h, reagent_text):
            """绘制右向箭头 + 试剂标注（从左到右）"""
            arrow_y = base_y + h / 2
            tx = x1 + 12
            ex = x2 - 10
            hx = ex - 10
            line_center = (tx + hx) / 2

            reagent = StructureRenderer._format_reagent(reagent_text)
            if reagent:
                split = _split_reagent(reagent)
                above_lines = split.get("above", [])
                below_lines = split.get("below", [])
                line_spacing = 16

                for li, line in enumerate(above_lines):
                    line_y = arrow_y - 5 - (len(above_lines) - 1 - li) * line_spacing
                    _render_text_line(line, line_y, line_center)
                for li, line in enumerate(below_lines):
                    line_y = arrow_y + 5 + (li + 1) * line_spacing
                    _render_text_line(line, line_y, line_center)

            svg_parts.append(
                f'<line x1="{tx}" y1="{arrow_y}" x2="{hx}" y2="{arrow_y}" '
                f'stroke="#222" stroke-width="1.5"/>'
                f'<polygon points="{hx - 6},{arrow_y - 4} {ex},{arrow_y} {hx - 6},{arrow_y + 4}" '
                f'fill="#222"/>'
            )

        def _draw_arrow_left(x1, x2, base_y, h, reagent_text):
            """绘制左向箭头 + 试剂标注（从右到左，用于U字形第二行）"""
            arrow_y = base_y + h / 2
            # x1 = 当前化合物左边缘（右端），x2 = 下一个化合物右边缘（左端）
            # 箭头从右指向左，所以 tx（箭尾）在右边，ex（箭头尖）在左边
            tx = x1 - 12  # 箭尾（右端内缩，略左于当前化合物左边缘）
            ex = x2 + 10  # 箭头尖（左端外伸，略右于下一个化合物右边缘）
            hx = ex + 10  # 箭杆起点（箭头尖右侧）
            line_center = (tx + hx) / 2

            reagent = StructureRenderer._format_reagent(reagent_text)
            if reagent:
                split = _split_reagent(reagent)
                above_lines = split.get("above", [])
                below_lines = split.get("below", [])
                line_spacing = 16

                for li, line in enumerate(above_lines):
                    line_y = arrow_y - 5 - (len(above_lines) - 1 - li) * line_spacing
                    _render_text_line(line, line_y, line_center)
                for li, line in enumerate(below_lines):
                    line_y = arrow_y + 5 + (li + 1) * line_spacing
                    _render_text_line(line, line_y, line_center)

            # 左向箭头：箭尾在右(tx)，箭头尖在左(ex)
            svg_parts.append(
                f'<line x1="{hx}" y1="{arrow_y}" x2="{tx}" y2="{arrow_y}" '
                f'stroke="#222" stroke-width="1.5"/>'
                f'<polygon points="{hx + 6},{arrow_y - 4} {ex},{arrow_y} {hx + 6},{arrow_y + 4}" '
                f'fill="#222"/>'
            )

        def render_row(start_idx, end_idx, row_idx, is_reversed=False):
            """渲染一行化合物"""
            row_n = end_idx - start_idx
            positions = row_positions[row_idx]
            struct_y = side_margin + row_idx * (row_total_h + row_gap) + top_margin

            for j in range(row_n):
                idx = start_idx + j
                step = steps[idx]
                x = positions[j]

                smiles = step.get("smiles", "")
                mol = StructureRenderer.smiles_to_mol(smiles) if smiles else None
                if mol:
                    svg_content = StructureRenderer._mol_to_svg_content(mol, struct_w, struct_h)
                    svg_parts.append(
                        f'<g transform="translate({x}, {struct_y})">'
                        f'{svg_content}'
                        f'</g>'
                    )
                else:
                    name = step.get("name", "?")
                    svg_parts.append(
                        f'<text x="{x + struct_w / 2}" y="{struct_y + struct_h / 2}" '
                        f'text-anchor="middle" font-size="13" fill="#999" '
                        f'font-family="Microsoft YaHei,微软雅黑,sans-serif">{name}</text>'
                    )

                label = step.get("label", chr(65 + idx))
                label_y = struct_y + struct_h + 20
                svg_parts.append(
                    f'<text x="{x + struct_w / 2}" y="{label_y}" '
                    f'text-anchor="middle" font-size="11" font-weight="bold" '
                    f'font-family="Times New Roman,Times,serif" fill="#111">{label}</text>'
                )

                if j < row_n - 1:
                    arrow_w = arrow_widths[idx]
                    if is_reversed:
                        # 第二行：箭头从右向左（化合物j左边缘 → 化合物j+1右边缘）
                        _draw_arrow_left(x, x - arrow_w, struct_y, struct_h,
                                    steps[idx + 1].get("reagent", ""))
                    else:
                        _draw_arrow_right(x + struct_w, x + struct_w + arrow_w, struct_y, struct_h,
                                    steps[idx + 1].get("reagent", ""))

            return struct_y, positions[0]

        # === 渲染各行 ===
        prev_end_y = 0
        prev_end_x = 0
        for ri, (start, end) in enumerate(rows):
            is_reversed = (ri > 0)  # 第二行是U字形，箭头从右向左

            # 行间竖直箭头 — 在第二行结构式之前绘制，避免箭头压在结构上
            if ri > 0:
                struct_y = side_margin + ri * (row_total_h + row_gap) + top_margin
                row_start = row_positions[ri][0]
                top_x = prev_end_x + struct_w / 2
                top_y = prev_end_y + struct_h
                bot_x = row_start + struct_w / 2
                bot_y = struct_y

                mid_y = (top_y + bot_y) / 2
                reagent = steps[start].get("reagent", "")
                reagent = StructureRenderer._format_reagent(reagent)
                if reagent:
                    svg_parts.append(
                        f'<text x="{top_x + 18}" y="{mid_y - 8}" '
                        f'text-anchor="start" font-size="12" '
                        f'font-family="Microsoft YaHei,微软雅黑,SimHei,sans-serif" fill="#222">{reagent}</text>'
                    )

                if abs(top_x - bot_x) < 5:
                    svg_parts.append(
                        f'<line x1="{top_x}" y1="{top_y + 24}" x2="{bot_x}" y2="{bot_y - 24}" '
                        f'stroke="#222" stroke-width="1.5"/>'
                        f'<polygon points="{bot_x - 6},{bot_y - 24} {bot_x},{bot_y - 14} {bot_x + 6},{bot_y - 24}" '
                        f'fill="#222"/>'
                    )
                else:
                    svg_parts.append(
                        f'<line x1="{top_x}" y1="{top_y + 24}" x2="{top_x}" y2="{mid_y}" '
                        f'stroke="#222" stroke-width="1.5"/>'
                        f'<line x1="{top_x}" y1="{mid_y}" x2="{bot_x}" y2="{mid_y}" '
                        f'stroke="#222" stroke-width="1.5"/>'
                        f'<line x1="{bot_x}" y1="{mid_y}" x2="{bot_x}" y2="{bot_y - 24}" '
                        f'stroke="#222" stroke-width="1.5"/>'
                        f'<polygon points="{bot_x - 6},{bot_y - 24} {bot_x},{bot_y - 14} {bot_x + 6},{bot_y - 24}" '
                        f'fill="#222"/>'
                    )

            struct_y, row_start = render_row(start, end, ri, is_reversed)
            prev_end_y = struct_y
            prev_end_x = row_positions[ri][-1]

        svg_parts.append('</svg>')
        return '\n'.join(svg_parts)

    @staticmethod
    def _mol_to_png_b64(mol, width: int, height: int, scale: int = 2) -> str:
        """
        将RDKit分子渲染为PNG base64 data URI
        使用2x分辨率渲染再缩放，保证清晰度
        跨平台一致，不依赖系统字体
        """
        dw = width * scale
        dh = height * scale
        img = Draw.MolToImage(
            mol, size=(dw, dh),
            kekulize=True,
            wedgeBonds=True,
        )
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{b64}"

    @staticmethod
    def _mol_to_svg_str(mol, width: int, height: int) -> str:
        """将RDKit分子渲染为SVG片段（回退方案）"""
        drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
        opts = drawer.drawOptions()
        opts.bondLineWidth = 1.8
        opts.fixedBondLength = 28
        opts.addStereoAnnotation = True
        opts.multipleBondOffset = 0.15
        opts.includeAtomTags = False
        opts.prepareMolsBeforeDrawing = True
        opts.clearBackground = True
        opts.atomLabelFontSize = 16
        opts.additionalAtomLabelPadding = 0.12
        drawer.DrawMolecule(mol)
        drawer.FinishDrawing()
        svg = drawer.GetDrawingText()
        gt_pos = svg.find('>')
        svg_end = svg.rfind('</svg>')
        if gt_pos >= 0 and svg_end >= 0:
            return svg[gt_pos + 1:svg_end]
        return svg

    @staticmethod
    def render_route_diagram_png(
        steps: List[dict],
        title: str = "",
        scale: float = 2.0,
    ) -> bytes:
        """
        渲染合成路线图为PNG（用于Word嵌入）

        Returns:
            PNG字节数据
        """
        svg = StructureRenderer.render_route_diagram_svg(steps, title)
        # 使用cairosvg将SVG转PNG
        try:
            import cairosvg
            return cairosvg.svg2png(bytestring=svg.encode('utf-8'), scale=scale)
        except ImportError:
            # 回退：使用RDKit直接渲染（简单并排）
            mols = []
            legends = []
            for step in steps:
                smiles = step.get("smiles", "")
                mol = StructureRenderer.smiles_to_mol(smiles)
                if mol:
                    mols.append(mol)
                    legends.append(step.get("label", ""))
            if not mols:
                return b''
            img = Draw.MolsToGridImage(
                mols, molsPerRow=len(mols),
                subImgSize=(300, 200),
                legends=legends
            )
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            buffer.seek(0)
            return buffer.getvalue()

    @staticmethod
    def render_png_base64(
        smiles: str,
        width: int = 400,
        height: int = 200,
        label: str = "",
    ) -> str:
        """
        将SMILES渲染为PNG base64

        Returns:
            data:image/png;base64,... 格式字符串
        """
        mol = StructureRenderer.smiles_to_mol(smiles)
        if mol is None:
            return ""

        img = Draw.MolToImage(mol, size=(width, height), legend=label if label else None)
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        b64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return f"data:image/png;base64,{b64}"


# 全局单例
renderer = StructureRenderer()