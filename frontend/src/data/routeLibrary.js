const ROUTE_LIBRARY = [
  {
    id: 1,
    title: "苯巴比妥合成路线",
    desc: "苯 → 苯巴比妥（7步），傅克烷基化→自由基卤代→腈化→酯化→Claisen缩合→烷基化→巴比妥酸环化，经典镇静催眠药物全合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "CH₃Cl, AlCl₃, △", product: "甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "甲苯", reagent: "Cl₂, 光照", product: "苄基氯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "苄基氯", reagent: "KCN, C₂H₅OH", product: "苯乙腈", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯乙腈", reagent: "C₂H₅OH, 浓H₂SO₄, △", product: "苯乙酸乙酯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "苯乙酸乙酯", reagent: "(COOC₂H₅)₂, NaOEt", product: "苯基丙二酸二乙酯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "苯基丙二酸二乙酯", reagent: "C₂H₅Br, NaOEt", product: "苯基乙基丙二酸二乙酯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "苯基乙基丙二酸二乙酯", reagent: "尿素, NaOEt, △", product: "苯巴比妥", reaction_type: "取代反应" }
    ]
  },
  {
    id: 2,
    title: "水杨酸丙酯合成路线",
    desc: "苯酚 → 水杨酸丙酯（7步），Kolbe-Schmitt羧化→酸化→酰化保护→酰氯化→酯化→脱保护，经典酚酸酯合成",
    steps: [
      { step_number: 1, reactant: "苯酚", reagent: "NaOH, H₂O", product: "苯酚钠", reaction_type: "酸碱反应" },
      { step_number: 2, reactant: "苯酚钠", reagent: "CO₂, 加压, 120°C", product: "水杨酸钠", reaction_type: "取代反应" },
      { step_number: 3, reactant: "水杨酸钠", reagent: "HCl, H₂O", product: "水杨酸", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "水杨酸", reagent: "(CH₃CO)₂O, H₂SO₄, △", product: "乙酰水杨酸", reaction_type: "取代反应" },
      { step_number: 5, reactant: "乙酰水杨酸", reagent: "SOCl₂, △", product: "乙酰水杨酰氯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "乙酰水杨酰氯", reagent: "CH₃CH₂CH₂OH, 吡啶", product: "乙酰水杨酸丙酯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "乙酰水杨酸丙酯", reagent: "NH₃, CH₃OH, 0°C", product: "水杨酸丙酯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 3,
    title: "己二酸合成路线",
    desc: "环己酮 → 己二酸（7步），肟化→Beckmann重排→水解→重氮化→酯化→氧化→水解，经典尼龙-66前体合成",
    steps: [
      { step_number: 1, reactant: "环己酮", reagent: "NH₂OH·HCl, NaOAc", product: "环己酮肟", reaction_type: "加成反应" },
      { step_number: 2, reactant: "环己酮肟", reagent: "浓H₂SO₄, 100°C", product: "己内酰胺", reaction_type: "重排反应" },
      { step_number: 3, reactant: "己内酰胺", reagent: "HCl, H₂O, △", product: "6-氨基己酸", reaction_type: "水解反应" },
      { step_number: 4, reactant: "6-氨基己酸", reagent: "NaNO₂, HCl, 0-5°C", product: "6-羟基己酸", reaction_type: "取代反应" },
      { step_number: 5, reactant: "6-羟基己酸", reagent: "CH₃OH, 浓H₂SO₄, △", product: "6-羟基己酸甲酯", reaction_type: "酯化反应" },
      { step_number: 6, reactant: "6-羟基己酸甲酯", reagent: "KMnO₄, H⁺, 0°C", product: "己二酸单甲酯", reaction_type: "氧化反应" },
      { step_number: 7, reactant: "己二酸单甲酯", reagent: "NaOH, H₂O, △; (2) HCl", product: "己二酸", reaction_type: "水解反应" }
    ]
  },
  {
    id: 4,
    title: "苯丁腈合成路线",
    desc: "苯甲醛 → 苯丁腈（7步），Perkin缩合→酰氯化→酯化→催化氢化→LiAlH₄还原→卤代→腈化，经典同系化延伸策略",
    steps: [
      { step_number: 1, reactant: "苯甲醛", reagent: "(CH₃CO)₂O, CH₃COONa, △", product: "肉桂酸", reaction_type: "取代反应" },
      { step_number: 2, reactant: "肉桂酸", reagent: "SOCl₂, △", product: "肉桂酰氯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "肉桂酰氯", reagent: "C₂H₅OH, 吡啶", product: "肉桂酸乙酯", reaction_type: "取代反应" },
      { step_number: 4, reactant: "肉桂酸乙酯", reagent: "H₂, Pd/C, CH₃OH", product: "苯丙酸乙酯", reaction_type: "加成反应" },
      { step_number: 5, reactant: "苯丙酸乙酯", reagent: "LiAlH₄, 无水乙醚", product: "苯丙醇", reaction_type: "还原反应" },
      { step_number: 6, reactant: "苯丙醇", reagent: "PBr₃, 0°C", product: "苯丙基溴", reaction_type: "取代反应" },
      { step_number: 7, reactant: "苯丙基溴", reagent: "KCN, C₂H₅OH, △", product: "苯丁腈", reaction_type: "取代反应" }
    ]
  },
  {
    id: 5,
    title: "对氨基苯甲酸合成路线",
    desc: "甲苯 → 对氨基苯甲酸（7步），硝化→氧化→酰氯化→酰胺化→还原→水解，经典PABA合成，磺胺类药物关键中间体",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "KMnO₄, OH⁻, △", product: "对硝基苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 3, reactant: "对硝基苯甲酸钾", reagent: "HCl, H₂O", product: "对硝基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "对硝基苯甲酸", reagent: "SOCl₂, △", product: "对硝基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对硝基苯甲酰氯", reagent: "NH₃, 0°C", product: "对硝基苯甲酰胺", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对硝基苯甲酰胺", reagent: "Fe, HCl", product: "对氨基苯甲酰胺", reaction_type: "还原反应" },
      { step_number: 7, reactant: "对氨基苯甲酰胺", reagent: "NaOH, H₂O, △; (2) HCl", product: "对氨基苯甲酸", reaction_type: "水解反应" }
    ]
  },
  {
    id: 6,
    title: "二苯甲酮合成路线",
    desc: "苯 → 二苯甲酮（7步），溴代→Grignard试剂→Friedel-Crafts酰化→卤仿反应→酰氯化→Friedel-Crafts，经典光引发剂合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "Br₂, FeBr₃", product: "溴苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "溴苯", reagent: "Mg, 无水乙醚", product: "苯基溴化镁", reaction_type: "加成反应" },
      { step_number: 3, reactant: "苯", reagent: "CH₃COCl, AlCl₃", product: "苯乙酮", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯乙酮", reagent: "Br₂, NaOH, △", product: "苯甲酸钠", reaction_type: "取代反应" },
      { step_number: 5, reactant: "苯甲酸钠", reagent: "HCl, H₂O", product: "苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 6, reactant: "苯甲酸", reagent: "SOCl₂, △", product: "苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "苯甲酰氯", reagent: "苯基溴化镁, 无水乙醚, −78°C; (2) H₂O", product: "二苯甲酮", reaction_type: "加成反应" }
    ]
  },
  {
    id: 7,
    title: "己二酸二甲酯合成路线",
    desc: "环己醇 → 己二酸二甲酯（7步），消去→环氧化→水解→氧化断裂→酸化→酰氯化→酯化，经典尼龙单体合成变体",
    steps: [
      { step_number: 1, reactant: "环己醇", reagent: "浓H₂SO₄, 170°C", product: "环己烯", reaction_type: "消去反应" },
      { step_number: 2, reactant: "环己烯", reagent: "H₂O₂, HCOOH", product: "环氧环己烷", reaction_type: "氧化反应" },
      { step_number: 3, reactant: "环氧环己烷", reagent: "H₂O, H⁺, △", product: "反-1,2-环己二醇", reaction_type: "加成反应" },
      { step_number: 4, reactant: "反-1,2-环己二醇", reagent: "NaIO₄, H₂O", product: "己二醛", reaction_type: "氧化反应" },
      { step_number: 5, reactant: "己二醛", reagent: "Ag₂O, NH₃, H₂O", product: "己二酸铵", reaction_type: "氧化反应" },
      { step_number: 6, reactant: "己二酸铵", reagent: "HCl, H₂O", product: "己二酸", reaction_type: "酸碱反应" },
      { step_number: 7, reactant: "己二酸", reagent: "CH₃OH, 浓H₂SO₄, △", product: "己二酸二甲酯", reaction_type: "酯化反应" }
    ]
  },
  {
    id: 8,
    title: "对硝基苯乙醚合成路线",
    desc: "苯 → 对硝基苯乙醚（7步），硝化→还原→乙酰化保护→硝化→脱保护→重氮化水解→Williamson醚化，经典对位硝基芳醚合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, △", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对硝基乙酰苯胺", reagent: "NaOH, H₂O, △", product: "对硝基苯胺", reaction_type: "水解反应" },
      { step_number: 6, reactant: "对硝基苯胺", reagent: "NaNO₂, HCl, 0-5°C; (2) H₂O, △", product: "对硝基苯酚", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对硝基苯酚", reagent: "C₂H₅Br, K₂CO₃, DMF", product: "对硝基苯乙醚", reaction_type: "取代反应" }
    ]
  },
  {
    id: 9,
    title: "对硝基苯甲腈合成路线",
    desc: "苯 → 对硝基苯胺（7步），硝化→还原→乙酰化保护→硝化→水解→重氮化→Sandmeyer氰化，经典硝基芳胺合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, △", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对硝基乙酰苯胺", reagent: "NaOH, H₂O, △", product: "对硝基苯胺", reaction_type: "水解反应" },
      { step_number: 6, reactant: "对硝基苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "对硝基重氮盐", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对硝基重氮盐", reagent: "CuCN, △", product: "对硝基苯甲腈", reaction_type: "取代反应" }
    ]
  },
  {
    id: 10,
    title: "6-羧基香豆素甲酯合成路线",
    desc: "苯酚 → 6-羧基香豆素甲酯（8步），Reimer-Tiemann甲酰化→Perkin缩合→内酯化→硝化→还原→重氮化/Sandmeyer氰化→水解→酯化，经典香豆素衍生物全合成",
    steps: [
      { step_number: 1, reactant: "苯酚", reagent: "CHCl₃, NaOH, △", product: "水杨醛", reaction_type: "取代反应" },
      { step_number: 2, reactant: "水杨醛", reagent: "(CH₃CO)₂O, CH₃COONa, △", product: "邻乙酰氧基肉桂酸", reaction_type: "取代反应" },
      { step_number: 3, reactant: "邻乙酰氧基肉桂酸", reagent: "△, 减压", product: "香豆素", reaction_type: "消去反应" },
      { step_number: 4, reactant: "香豆素", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "6-硝基香豆素", reaction_type: "取代反应" },
      { step_number: 5, reactant: "6-硝基香豆素", reagent: "Fe, HCl, △", product: "6-氨基香豆素", reaction_type: "还原反应" },
      { step_number: 6, reactant: "6-氨基香豆素", reagent: "NaNO₂, HCl, 0-5°C; (2) CuCN, △", product: "6-氰基香豆素", reaction_type: "取代反应" },
      { step_number: 7, reactant: "6-氰基香豆素", reagent: "NaOH, H₂O, △; (2) HCl", product: "6-羧基香豆素", reaction_type: "水解反应" },
      { step_number: 8, reactant: "6-羧基香豆素", reagent: "CH₃OH, 浓H₂SO₄, △", product: "6-羧基香豆素甲酯", reaction_type: "酯化反应" }
    ]
  },
  {
    id: 11,
    title: "对甲氧基苯甲酸甲酯合成路线",
    desc: "甲苯 → 对甲氧基苯甲酸甲酯（7步），磺化→碱熔→甲基化保护→氧化→酸化→酯化，经典茴香酸酯合成",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓H₂SO₄, △", product: "对甲苯磺酸", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对甲苯磺酸", reagent: "NaOH, 熔融, 300°C", product: "对甲苯酚钠", reaction_type: "取代反应" },
      { step_number: 3, reactant: "对甲苯酚钠", reagent: "HCl, H₂O", product: "对甲苯酚", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "对甲苯酚", reagent: "CH₃I, K₂CO₃, DMF", product: "对甲基苯甲醚", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对甲基苯甲醚", reagent: "KMnO₄, OH⁻, △", product: "对甲氧基苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 6, reactant: "对甲氧基苯甲酸钾", reagent: "HCl, H₂O", product: "对甲氧基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 7, reactant: "对甲氧基苯甲酸", reagent: "CH₃OH, 浓H₂SO₄, △", product: "对甲氧基苯甲酸甲酯", reaction_type: "酯化反应" }
    ]
  },
  {
    id: 12,
    title: "肉桂醛合成路线",
    desc: "苯甲醛 → 肉桂醛（7步），Knoevenagel缩合→酰氯化→酯化→溴代→消除→Na/NH₃还原→DIBAL-H选择性还原，经典α,β-不饱和醛合成",
    steps: [
      { step_number: 1, reactant: "苯甲醛", reagent: "CH₂(COOH)₂, 吡啶, △", product: "肉桂酸", reaction_type: "消去反应" },
      { step_number: 2, reactant: "肉桂酸", reagent: "SOCl₂, △", product: "肉桂酰氯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "肉桂酰氯", reagent: "C₂H₅OH, 吡啶", product: "肉桂酸乙酯", reaction_type: "取代反应" },
      { step_number: 4, reactant: "肉桂酸乙酯", reagent: "Br₂, CCl₄", product: "2,3-二溴苯丙酸乙酯", reaction_type: "加成反应" },
      { step_number: 5, reactant: "2,3-二溴苯丙酸乙酯", reagent: "KOH, C₂H₅OH, △", product: "苯丙炔酸乙酯", reaction_type: "消去反应" },
      { step_number: 6, reactant: "苯丙炔酸乙酯", reagent: "Na, NH₃(l)", product: "肉桂酸乙酯", reaction_type: "还原反应" },
      { step_number: 7, reactant: "肉桂酸乙酯", reagent: "DIBAL-H, 甲苯, −78°C", product: "肉桂醛", reaction_type: "还原反应" }
    ]
  },
  {
    id: 13,
    title: "戊二酸合成路线",
    desc: "环戊酮 → 戊二酸（7步），Baeyer-Villiger氧化→水解→酯化→还原→卤代→腈化→水解，经典二羧酸合成策略",
    steps: [
      { step_number: 1, reactant: "环戊酮", reagent: "H₂O₂, CH₃COOH, 0°C", product: "δ-戊内酯", reaction_type: "氧化反应" },
      { step_number: 2, reactant: "δ-戊内酯", reagent: "NaOH, H₂O, △", product: "5-羟基戊酸钠", reaction_type: "水解反应" },
      { step_number: 3, reactant: "5-羟基戊酸钠", reagent: "HCl, H₂O", product: "5-羟基戊酸", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "5-羟基戊酸", reagent: "CH₃OH, 浓H₂SO₄, △", product: "5-羟基戊酸甲酯", reaction_type: "酯化反应" },
      { step_number: 5, reactant: "5-羟基戊酸甲酯", reagent: "PBr₃, 0°C", product: "5-溴戊酸甲酯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "5-溴戊酸甲酯", reagent: "KCN, DMSO, △", product: "5-氰基戊酸甲酯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "5-氰基戊酸甲酯", reagent: "NaOH, H₂O, △; (2) HCl", product: "戊二酸", reaction_type: "水解反应" }
    ]
  },
  {
    id: 14,
    title: "3-苯基丁酸合成路线",
    desc: "苯 → 3-苯基丁酸（8步），Friedel-Crafts酰化→还原→卤代→Grignard→甲醛加成→卤代→腈化→水解，经典苯基取代丁酸合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "CH₃COCl, AlCl₃", product: "苯乙酮", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯乙酮", reagent: "NaBH₄, CH₃OH", product: "1-苯乙醇", reaction_type: "还原反应" },
      { step_number: 3, reactant: "1-苯乙醇", reagent: "PBr₃, 0°C", product: "1-苯基溴乙烷", reaction_type: "取代反应" },
      { step_number: 4, reactant: "1-苯基溴乙烷", reagent: "Mg, 无水乙醚", product: "1-苯乙基溴化镁", reaction_type: "加成反应" },
      { step_number: 5, reactant: "1-苯乙基溴化镁", reagent: "HCHO, 无水乙醚; (2) H₂O", product: "2-苯基丙醇", reaction_type: "加成反应" },
      { step_number: 6, reactant: "2-苯基丙醇", reagent: "PBr₃, 0°C", product: "2-苯基丙基溴", reaction_type: "取代反应" },
      { step_number: 7, reactant: "2-苯基丙基溴", reagent: "KCN, C₂H₅OH, △", product: "3-苯基丁腈", reaction_type: "取代反应" },
      { step_number: 8, reactant: "3-苯基丁腈", reagent: "NaOH, H₂O, △; (2) HCl", product: "3-苯基丁酸", reaction_type: "水解反应" }
    ]
  },
  {
    id: 15,
    title: "对羧基苯甲酸合成路线",
    desc: "甲苯 → 对羧基苯甲酸（7步），硝化→氧化→酯化→还原→重氮化/Sandmeyer氰化→水解→酸化，经典对苯二甲酸单酯前体合成",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "KMnO₄, OH⁻, △", product: "对硝基苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 3, reactant: "对硝基苯甲酸钾", reagent: "HCl, H₂O", product: "对硝基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "对硝基苯甲酸", reagent: "C₂H₅OH, 浓H₂SO₄, △", product: "对硝基苯甲酸乙酯", reaction_type: "酯化反应" },
      { step_number: 5, reactant: "对硝基苯甲酸乙酯", reagent: "Fe, HCl", product: "对氨基苯甲酸乙酯", reaction_type: "还原反应" },
      { step_number: 6, reactant: "对氨基苯甲酸乙酯", reagent: "NaNO₂, HCl, 0-5°C; (2) CuCN, △", product: "对氰基苯甲酸乙酯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对氰基苯甲酸乙酯", reagent: "NaOH, H₂O, △; (2) HCl", product: "对羧基苯甲酸", reaction_type: "水解反应" }
    ]
  },
  {
    id: 16,
    title: "对溴苯甲酸甲酯合成路线",
    desc: "甲苯 → 对溴苯甲酸甲酯（7步），硝化→氧化→酸化→还原→重氮化/Sandmeyer溴代→酰氯化→酯化，经典对溴苯甲酸酯合成",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "KMnO₄, OH⁻, △", product: "对硝基苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 3, reactant: "对硝基苯甲酸钾", reagent: "HCl, H₂O", product: "对硝基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "对硝基苯甲酸", reagent: "Fe, HCl", product: "对氨基苯甲酸", reaction_type: "还原反应" },
      { step_number: 5, reactant: "对氨基苯甲酸", reagent: "NaNO₂, HCl, 0-5°C; (2) CuBr, △", product: "对溴苯甲酸", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对溴苯甲酸", reagent: "SOCl₂, △", product: "对溴苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对溴苯甲酰氯", reagent: "CH₃OH, 吡啶", product: "对溴苯甲酸甲酯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 17,
    title: "苯甲酰苯胺合成路线",
    desc: "苯 → 苯甲酰苯胺（7步），Friedel-Crafts酰化→卤仿→酸化→酰氯化→酰胺化→Hofmann重排→Schotten-Baumann，经典芳酰胺合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "CH₃COCl, AlCl₃", product: "苯乙酮", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯乙酮", reagent: "Br₂, NaOH, △", product: "苯甲酸钠", reaction_type: "取代反应" },
      { step_number: 3, reactant: "苯甲酸钠", reagent: "HCl, H₂O", product: "苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "苯甲酸", reagent: "SOCl₂, △", product: "苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "苯甲酰氯", reagent: "NH₃, 0°C", product: "苯甲酰胺", reaction_type: "取代反应" },
      { step_number: 6, reactant: "苯甲酰胺", reagent: "Br₂, NaOH, △", product: "苯胺", reaction_type: "取代反应" },
      { step_number: 7, reactant: "苯胺", reagent: "苯甲酰氯, NaOH, H₂O", product: "苯甲酰苯胺", reaction_type: "取代反应" }
    ]
  },
  {
    id: 18,
    title: "对羟基苯甲醛合成路线",
    desc: "苯酚 → 对羟基苯甲醛（7步），甲基化保护→Friedel-Crafts酰化→卤仿反应→酰氯化→选择性还原→脱甲基，经典对位羟基芳醛合成",
    steps: [
      { step_number: 1, reactant: "苯酚", reagent: "CH₃I, K₂CO₃, DMF", product: "苯甲醚", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯甲醚", reagent: "CH₃COCl, AlCl₃", product: "对甲氧基苯乙酮", reaction_type: "取代反应" },
      { step_number: 3, reactant: "对甲氧基苯乙酮", reagent: "Br₂, NaOH, △", product: "对甲氧基苯甲酸钠", reaction_type: "取代反应" },
      { step_number: 4, reactant: "对甲氧基苯甲酸钠", reagent: "HCl, H₂O", product: "对甲氧基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 5, reactant: "对甲氧基苯甲酸", reagent: "SOCl₂, △", product: "对甲氧基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对甲氧基苯甲酰氯", reagent: "LiAlH(OtBu)₃, 无水乙醚, −78°C", product: "对甲氧基苯甲醛", reaction_type: "还原反应" },
      { step_number: 7, reactant: "对甲氧基苯甲醛", reagent: "HBr, △", product: "对羟基苯甲醛", reaction_type: "取代反应" }
    ]
  },
  {
    id: 19,
    title: "苯丙酸合成路线",
    desc: "甲苯 → 苯丙酸（7步），自由基卤代→腈化→水解→酯化→还原→卤代→Grignard羧化，经典芳基链酸合成",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "Cl₂, 光照", product: "苄基氯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苄基氯", reagent: "KCN, C₂H₅OH, △", product: "苯乙腈", reaction_type: "取代反应" },
      { step_number: 3, reactant: "苯乙腈", reagent: "NaOH, H₂O, △; (2) HCl", product: "苯乙酸", reaction_type: "水解反应" },
      { step_number: 4, reactant: "苯乙酸", reagent: "C₂H₅OH, 浓H₂SO₄, △", product: "苯乙酸乙酯", reaction_type: "酯化反应" },
      { step_number: 5, reactant: "苯乙酸乙酯", reagent: "LiAlH₄, 无水乙醚", product: "苯乙醇", reaction_type: "还原反应" },
      { step_number: 6, reactant: "苯乙醇", reagent: "PBr₃, 0°C", product: "苯乙基溴", reaction_type: "取代反应" },
      { step_number: 7, reactant: "苯乙基溴", reagent: "Mg, 无水乙醚; (2) CO₂; (3) H₂O", product: "苯丙酸", reaction_type: "加成反应" }
    ]
  },
  {
    id: 20,
    title: "对氯苯磺酸合成路线",
    desc: "苯 → 对氯苯磺酸（8步），磺化→酰氯化→酰胺化→硝化→还原→重氮化/Sandmeyer氯代→水解→酸化，经典对氯苯磺酸合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓H₂SO₄, △", product: "苯磺酸", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯磺酸", reagent: "PCl₅, △", product: "苯磺酰氯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "苯磺酰氯", reagent: "NH₃, 0°C", product: "苯磺酰胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯磺酰胺", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基苯磺酰胺", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对硝基苯磺酰胺", reagent: "Fe, HCl", product: "对氨基苯磺酰胺", reaction_type: "还原反应" },
      { step_number: 6, reactant: "对氨基苯磺酰胺", reagent: "NaNO₂, HCl, 0-5°C; (2) CuCl, △", product: "对氯苯磺酰胺", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对氯苯磺酰胺", reagent: "NaOH, H₂O, △", product: "对氯苯磺酸钠", reaction_type: "水解反应" },
      { step_number: 8, reactant: "对氯苯磺酸钠", reagent: "HCl, H₂O", product: "对氯苯磺酸", reaction_type: "酸碱反应" }
    ]
  },
  {
    id: 21,
    title: "二苯乙酸合成路线",
    desc: "甲苯/苯 → 二苯乙酸（8步），自由基卤代→水解→氧化→溴代→Grignard→加成→卤代→腈化水解，经典二苯乙酸合成",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "Cl₂, 光照", product: "苄基氯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苄基氯", reagent: "NaOH, H₂O, △", product: "苯甲醇", reaction_type: "取代反应" },
      { step_number: 3, reactant: "苯甲醇", reagent: "PCC, CH₂Cl₂", product: "苯甲醛", reaction_type: "氧化反应" },
      { step_number: 4, reactant: "苯", reagent: "Br₂, FeBr₃", product: "溴苯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "溴苯", reagent: "Mg, 无水乙醚", product: "苯基溴化镁", reaction_type: "加成反应" },
      { step_number: 6, reactant: "苯基溴化镁", reagent: "苯甲醛, 无水乙醚; (2) H₂O", product: "二苯甲醇", reaction_type: "加成反应" },
      { step_number: 7, reactant: "二苯甲醇", reagent: "PBr₃, 0°C", product: "二苯溴甲烷", reaction_type: "取代反应" },
      { step_number: 8, reactant: "二苯溴甲烷", reagent: "(1) KCN, C₂H₅OH, △; (2) NaOH, H₂O, △; (3) HCl", product: "二苯乙酸", reaction_type: "取代反应" }
    ]
  },
  {
    id: 22,
    title: "3-氨基吲哚合成路线",
    desc: "苯胺 → 吲哚（8步），重氮化→还原→Fischer吲哚合成，经典含氮杂环合成",
    steps: [
      { step_number: 1, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "重氮盐", reaction_type: "取代反应" },
      { step_number: 2, reactant: "重氮盐", reagent: "SnCl₂, HCl", product: "苯肼", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯肼", reagent: "CH₃CHO, H⁺", product: "乙醛苯腙", reaction_type: "加成反应" },
      { step_number: 4, reactant: "乙醛苯腙", reagent: "ZnCl₂, △", product: "吲哚", reaction_type: "重排反应" },
      { step_number: 5, reactant: "吲哚", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "3-硝基吲哚", reaction_type: "取代反应" },
      { step_number: 6, reactant: "3-硝基吲哚", reagent: "Fe, HCl", product: "3-氨基吲哚", reaction_type: "还原反应" },
      { step_number: 7, reactant: "3-氨基吲哚", reagent: "CH₃COCl, 吡啶", product: "3-乙酰氨基吲哚", reaction_type: "取代反应" },
      { step_number: 8, reactant: "3-乙酰氨基吲哚", reagent: "NaOH, H₂O, △; (2) HCl", product: "3-氨基吲哚", reaction_type: "水解反应" }
    ]
  },
  {
    id: 23,
    title: "苯并呋喃-2-甲酸甲酯合成路线",
    desc: "苯酚 → 苯并呋喃（8步），O-烷基化→Claisen重排→臭氧化→环化脱水，经典苯并杂环合成",
    steps: [
      { step_number: 1, reactant: "苯酚", reagent: "CH₂=CHCH₂Br, K₂CO₃, DMF", product: "苯基烯丙基醚", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯基烯丙基醚", reagent: "△, 200°C", product: "邻烯丙基苯酚", reaction_type: "重排反应" },
      { step_number: 3, reactant: "邻烯丙基苯酚", reagent: "O₃, CH₂Cl₂; (2) Zn, H₂O", product: "邻羟基苯乙醛", reaction_type: "氧化反应" },
      { step_number: 4, reactant: "邻羟基苯乙醛", reagent: "H⁺, △", product: "苯并呋喃", reaction_type: "消去反应" },
      { step_number: 5, reactant: "苯并呋喃", reagent: "Br₂, CCl₄", product: "2,3-二溴苯并呋喃", reaction_type: "加成反应" },
      { step_number: 6, reactant: "2,3-二溴苯并呋喃", reagent: "KOH, C₂H₅OH, △", product: "2-溴苯并呋喃", reaction_type: "消去反应" },
      { step_number: 7, reactant: "2-溴苯并呋喃", reagent: "Mg, 无水乙醚; (2) CO₂; (3) H₂O", product: "苯并呋喃-2-甲酸", reaction_type: "加成反应" },
      { step_number: 8, reactant: "苯并呋喃-2-甲酸", reagent: "CH₃OH, 浓H₂SO₄, △", product: "苯并呋喃-2-甲酸甲酯", reaction_type: "酯化反应" }
    ]
  },
  {
    id: 24,
    title: "对羟基苯甲酸合成路线",
    desc: "苯 → 对羟基苯甲酸（8步），硝化→还原→乙酰化保护→Friedel-Crafts酰化→脱保护→重氮化水解→Williamson醚化→卤仿/酸化，经典对羟基苯甲酸合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, △", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "CH₃COCl, AlCl₃", product: "对乙酰氨基苯乙酮", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对乙酰氨基苯乙酮", reagent: "NaOH, H₂O, △", product: "对氨基苯乙酮", reaction_type: "水解反应" },
      { step_number: 6, reactant: "对氨基苯乙酮", reagent: "NaNO₂, HCl, 0-5°C; (2) H₂O, △", product: "对羟基苯乙酮", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对羟基苯乙酮", reagent: "CH₃I, K₂CO₃, DMF", product: "对甲氧基苯乙酮", reaction_type: "取代反应" },
      { step_number: 8, reactant: "对甲氧基苯乙酮", reagent: "(1) Br₂, NaOH, △; (2) HCl; (3) HBr, △", product: "对羟基苯甲酸", reaction_type: "取代反应" }
    ]
  },
  {
    id: 25,
    title: "对溴苯甲酸甲酯合成路线",
    desc: "甲苯 → 对溴苯甲酸甲酯（7步），硝化→还原→重氮化→Sandmeyer溴代→氧化→酰氯化→酯化，经典对溴苯甲酸酯合成",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "Fe, HCl", product: "对氨基甲苯", reaction_type: "还原反应" },
      { step_number: 3, reactant: "对氨基甲苯", reagent: "NaNO₂, HCl, 0-5°C", product: "对甲苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "对甲苯重氮盐", reagent: "CuBr, △", product: "对溴甲苯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对溴甲苯", reagent: "KMnO₄, OH⁻, △", product: "对溴苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 6, reactant: "对溴苯甲酸钾", reagent: "HCl, H₂O", product: "对溴苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 7, reactant: "对溴苯甲酸", reagent: "(1) SOCl₂, △; (2) CH₃OH, 吡啶", product: "对溴苯甲酸甲酯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 26,
    title: "N-乙酰扁桃酰胺合成路线",
    desc: "苯甲醛 → N-乙酰扁桃酰胺（7步），氰醇化→水解→酯化→酰胺化→脱水→还原→乙酰化，经典α-羟基酰胺衍生物合成",
    steps: [
      { step_number: 1, reactant: "苯甲醛", reagent: "NaCN, HCl, 0°C", product: "扁桃腈", reaction_type: "加成反应" },
      { step_number: 2, reactant: "扁桃腈", reagent: "HCl, H₂O, △", product: "扁桃酸", reaction_type: "水解反应" },
      { step_number: 3, reactant: "扁桃酸", reagent: "CH₃OH, 浓H₂SO₄, △", product: "扁桃酸甲酯", reaction_type: "酯化反应" },
      { step_number: 4, reactant: "扁桃酸甲酯", reagent: "NH₃, CH₃OH, △", product: "扁桃酰胺", reaction_type: "取代反应" },
      { step_number: 5, reactant: "扁桃酰胺", reagent: "P₂O₅, △", product: "扁桃腈", reaction_type: "消去反应" },
      { step_number: 6, reactant: "扁桃腈", reagent: "H₂, Raney Ni, NH₃, C₂H₅OH", product: "α-羟基苯乙胺", reaction_type: "加成反应" },
      { step_number: 7, reactant: "α-羟基苯乙胺", reagent: "(CH₃CO)₂O, 吡啶", product: "N-乙酰扁桃酰胺", reaction_type: "取代反应" }
    ]
  },
  {
    id: 27,
    title: "对氯苯甲酸合成路线",
    desc: "苯→对氯苯甲酸(7步)，FC烷基化→硝化→还原→重氮化→Sandmeyer氯代→KMnO₄氧化→酸化，经典对位取代苯甲酸合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "CH₃Cl, AlCl₃, △", product: "甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "对硝基甲苯", reagent: "Fe, HCl, △", product: "对氨基甲苯", reaction_type: "还原反应" },
      { step_number: 4, reactant: "对氨基甲苯", reagent: "NaNO₂, HCl, 0-5°C", product: "对甲基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对甲基苯重氮盐", reagent: "CuCl, HCl, △", product: "对氯甲苯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对氯甲苯", reagent: "KMnO₄, OH⁻, △", product: "对氯苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 7, reactant: "对氯苯甲酸钾", reagent: "HCl, H₂O", product: "对氯苯甲酸", reaction_type: "酸碱反应" }
    ]
  },
  {
    id: 28,
    title: "苯甲酸乙酯合成路线",
    desc: "苯→苯甲酸乙酯(7步)，FC烷基化→自由基卤代→水解→氧化→酸化→酰氯化→酯化，经典芳香酯合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "CH₃Cl, AlCl₃, △", product: "甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "甲苯", reagent: "Cl₂, 光照", product: "苄基氯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "苄基氯", reagent: "NaOH, H₂O, △", product: "苯甲醇", reaction_type: "水解反应" },
      { step_number: 4, reactant: "苯甲醇", reagent: "KMnO₄, OH⁻, △", product: "苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 5, reactant: "苯甲酸钾", reagent: "HCl, H₂O", product: "苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 6, reactant: "苯甲酸", reagent: "SOCl₂, △", product: "苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "苯甲酰氯", reagent: "C₂H₅OH", product: "苯甲酸乙酯", reaction_type: "酯化反应" }
    ]
  },
  {
    id: 29,
    title: "对羟基苯甲酸合成路线",
    desc: "苯酚→对羟基苯甲酸(7步)，Williamson醚化→FC烷基化→自由基卤代→水解→KMnO₄氧化→酸化→HI醚键断裂，经典酚酸合成",
    steps: [
      { step_number: 1, reactant: "苯酚", reagent: "CH₃I, K₂CO₃, DMF", product: "苯甲醚", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯甲醚", reagent: "CH₃Cl, AlCl₃, △", product: "对甲基苯甲醚", reaction_type: "取代反应" },
      { step_number: 3, reactant: "对甲基苯甲醚", reagent: "Cl₂, 光照", product: "对氯甲基苯甲醚", reaction_type: "取代反应" },
      { step_number: 4, reactant: "对氯甲基苯甲醚", reagent: "NaOH, H₂O, △", product: "对甲氧基苯甲醇", reaction_type: "水解反应" },
      { step_number: 5, reactant: "对甲氧基苯甲醇", reagent: "KMnO₄, OH⁻, △", product: "对甲氧基苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 6, reactant: "对甲氧基苯甲酸钾", reagent: "HCl, H₂O", product: "对甲氧基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 7, reactant: "对甲氧基苯甲酸", reagent: "HI, △", product: "对羟基苯甲酸", reaction_type: "取代反应" }
    ]
  },
  {
    id: 30,
    title: "苯甲酰氯合成路线",
    desc: "苯→苯甲酰氯(7步)，FC烷基化→自由基卤代→水解→PCC氧化→KMnO₄氧化→酸化→SOCl₂酰氯化，经典酰氯合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "CH₃Cl, AlCl₃, △", product: "甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "甲苯", reagent: "Cl₂, 光照", product: "苄基氯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "苄基氯", reagent: "NaOH, H₂O, △", product: "苯甲醇", reaction_type: "水解反应" },
      { step_number: 4, reactant: "苯甲醇", reagent: "PCC, CH₂Cl₂", product: "苯甲醛", reaction_type: "氧化反应" },
      { step_number: 5, reactant: "苯甲醛", reagent: "KMnO₄, OH⁻, △", product: "苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 6, reactant: "苯甲酸钾", reagent: "HCl, H₂O", product: "苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 7, reactant: "苯甲酸", reagent: "SOCl₂, △", product: "苯甲酰氯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 31,
    title: "苯甲酸丙酯合成路线",
    desc: "苯→苯甲酸丙酯(7步)，FC烷基化→自由基卤代→水解→氧化→酸化→酰氯化→丙醇酯化，经典芳香酯合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "CH₃Cl, AlCl₃, △", product: "甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "甲苯", reagent: "Cl₂, 光照", product: "苄基氯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "苄基氯", reagent: "NaOH, H₂O, △", product: "苯甲醇", reaction_type: "水解反应" },
      { step_number: 4, reactant: "苯甲醇", reagent: "KMnO₄, OH⁻, △", product: "苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 5, reactant: "苯甲酸钾", reagent: "HCl, H₂O", product: "苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 6, reactant: "苯甲酸", reagent: "SOCl₂, △", product: "苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "苯甲酰氯", reagent: "CH₃CH₂CH₂OH", product: "苯甲酸丙酯", reaction_type: "酯化反应" }
    ]
  },
  {
    id: 32,
    title: "对硝基苯甲酸甲酯合成路线",
    desc: "甲苯→对硝基苯甲酸甲酯(7步)，硝化→自由基卤代→水解→KMnO₄氧化→酸化→酯化，经典硝基芳香酯合成",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "Cl₂, 光照", product: "对硝基苄基氯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "对硝基苄基氯", reagent: "NaOH, H₂O, △", product: "对硝基苯甲醇", reaction_type: "水解反应" },
      { step_number: 4, reactant: "对硝基苯甲醇", reagent: "KMnO₄, OH⁻, △", product: "对硝基苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 5, reactant: "对硝基苯甲酸钾", reagent: "HCl, H₂O", product: "对硝基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 6, reactant: "对硝基苯甲酸", reagent: "SOCl₂, △", product: "对硝基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对硝基苯甲酰氯", reagent: "CH₃OH", product: "对硝基苯甲酸甲酯", reaction_type: "酯化反应" }
    ]
  },
  {
    id: 33,
    title: "对苯二甲酸单甲酯合成路线",
    desc: "对二甲苯→对苯二甲酸单甲酯(8步)，自由基卤代→水解→PCC氧化→银镜反应→酸化→酯化→KMnO₄氧化→酸化，经典对苯二甲酸单酯合成",
    steps: [
      { step_number: 1, reactant: "对二甲苯", reagent: "Cl₂, 光照", product: "对甲基苄基氯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对甲基苄基氯", reagent: "NaOH, H₂O, △", product: "对甲基苯甲醇", reaction_type: "水解反应" },
      { step_number: 3, reactant: "对甲基苯甲醇", reagent: "PCC, CH₂Cl₂", product: "对甲基苯甲醛", reaction_type: "氧化反应" },
      { step_number: 4, reactant: "对甲基苯甲醛", reagent: "Ag(NH₃)₂OH, △", product: "对甲基苯甲酸铵", reaction_type: "氧化反应" },
      { step_number: 5, reactant: "对甲基苯甲酸铵", reagent: "HCl, H₂O", product: "对甲基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 6, reactant: "对甲基苯甲酸", reagent: "CH₃OH, 浓H₂SO₄, △", product: "对甲基苯甲酸甲酯", reaction_type: "酯化反应" },
      { step_number: 7, reactant: "对甲基苯甲酸甲酯", reagent: "KMnO₄, OH⁻, △", product: "对甲氧羰基苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 8, reactant: "对甲氧羰基苯甲酸钾", reagent: "HCl, H₂O", product: "对苯二甲酸单甲酯", reaction_type: "酸碱反应" }
    ]
  },
  {
    id: 34,
    title: "对甲氧基苯甲酰氯合成路线",
    desc: "苯酚→对甲氧基苯甲酰氯(8步)，Williamson醚化→FC烷基化→自由基卤代→水解→PCC氧化→银镜反应→酸化→SOCl₂酰氯化，经典对位取代芳香酰氯合成",
    steps: [
      { step_number: 1, reactant: "苯酚", reagent: "CH₃I, K₂CO₃, DMF", product: "苯甲醚", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯甲醚", reagent: "CH₃Cl, AlCl₃, △", product: "对甲基苯甲醚", reaction_type: "取代反应" },
      { step_number: 3, reactant: "对甲基苯甲醚", reagent: "Cl₂, 光照", product: "对氯甲基苯甲醚", reaction_type: "取代反应" },
      { step_number: 4, reactant: "对氯甲基苯甲醚", reagent: "NaOH, H₂O, △", product: "对甲氧基苯甲醇", reaction_type: "水解反应" },
      { step_number: 5, reactant: "对甲氧基苯甲醇", reagent: "PCC, CH₂Cl₂", product: "对甲氧基苯甲醛", reaction_type: "氧化反应" },
      { step_number: 6, reactant: "对甲氧基苯甲醛", reagent: "Ag(NH₃)₂OH, △", product: "对甲氧基苯甲酸铵", reaction_type: "氧化反应" },
      { step_number: 7, reactant: "对甲氧基苯甲酸铵", reagent: "HCl, H₂O", product: "对甲氧基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 8, reactant: "对甲氧基苯甲酸", reagent: "SOCl₂, △", product: "对甲氧基苯甲酰氯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 35,
    title: "苯乙酸乙酯合成路线",
    desc: "苯→苯乙酸乙酯(7步)，FC烷基化→自由基卤代→氰基取代→水解→酰氯化→酯化→氨解，经典苯乙酸酯合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "CH₃Cl, AlCl₃, △", product: "甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "甲苯", reagent: "Cl₂, 光照", product: "苄基氯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "苄基氯", reagent: "NaCN, C₂H₅OH", product: "苯乙腈", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯乙腈", reagent: "(1) NaOH, H₂O, △; (2) HCl", product: "苯乙酸", reaction_type: "水解反应" },
      { step_number: 5, reactant: "苯乙酸", reagent: "SOCl₂, △", product: "苯乙酰氯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "苯乙酰氯", reagent: "C₂H₅OH", product: "苯乙酸乙酯", reaction_type: "酯化反应" },
      { step_number: 7, reactant: "苯乙酸乙酯", reagent: "NH₃, CH₃OH, △", product: "苯乙酰胺", reaction_type: "取代反应" }
    ]
  },
  {
    id: 36,
    title: "间溴苯甲酸合成路线",
    desc: "苯→间溴苯甲酸(8步)，FC烷基化→自由基卤代→水解→氧化→酸化→硝化→还原→重氮化+Sandmeyer溴代，经典间位取代苯甲酸合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "CH₃Cl, AlCl₃, △", product: "甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "甲苯", reagent: "Cl₂, 光照", product: "苄基氯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "苄基氯", reagent: "NaOH, H₂O, △", product: "苯甲醇", reaction_type: "水解反应" },
      { step_number: 4, reactant: "苯甲醇", reagent: "KMnO₄, OH⁻, △", product: "苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 5, reactant: "苯甲酸钾", reagent: "HCl, H₂O", product: "苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 6, reactant: "苯甲酸", reagent: "浓HNO₃, 浓H₂SO₄", product: "间硝基苯甲酸", reaction_type: "取代反应" },
      { step_number: 7, reactant: "间硝基苯甲酸", reagent: "Fe, HCl, △", product: "间氨基苯甲酸", reaction_type: "还原反应" },
      { step_number: 8, reactant: "间氨基苯甲酸", reagent: "(1) NaNO₂, HCl, 0-5°C; (2) CuBr, △", product: "间溴苯甲酸", reaction_type: "取代反应" }
    ]
  },
  {
    id: 37,
    title: "对氨基苯甲酸甲酯合成路线",
    desc: "甲苯→对氨基苯甲酸甲酯(8步)，硝化→自由基卤代→水解→KMnO₄氧化→酸化→酰氯化→酯化→Fe/HCl还原，经典PABA甲酯合成",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "Cl₂, 光照", product: "对硝基苄基氯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "对硝基苄基氯", reagent: "NaOH, H₂O, △", product: "对硝基苯甲醇", reaction_type: "水解反应" },
      { step_number: 4, reactant: "对硝基苯甲醇", reagent: "KMnO₄, OH⁻, △", product: "对硝基苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 5, reactant: "对硝基苯甲酸钾", reagent: "HCl, H₂O", product: "对硝基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 6, reactant: "对硝基苯甲酸", reagent: "SOCl₂, △", product: "对硝基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对硝基苯甲酰氯", reagent: "CH₃OH", product: "对硝基苯甲酸甲酯", reaction_type: "酯化反应" },
      { step_number: 8, reactant: "对硝基苯甲酸甲酯", reagent: "Fe, HCl, △", product: "对氨基苯甲酸甲酯", reaction_type: "还原反应" }
    ]
  },
  {
    id: 38,
    title: "邻氯苯甲酸甲酯合成路线",
    desc: "苯胺→邻氯苯甲酸甲酯(7步)，乙酰化保护→邻位氯代→水解→重氮化→Sandmeyer氰化→水解→酯化，经典邻位取代苯甲酸酯合成",
    steps: [
      { step_number: 1, reactant: "苯胺", reagent: "(CH₃CO)₂O, △", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 2, reactant: "乙酰苯胺", reagent: "Cl₂, FeCl₃", product: "邻氯乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 3, reactant: "邻氯乙酰苯胺", reagent: "H₂O, H⁺, △", product: "邻氯苯胺", reaction_type: "水解反应" },
      { step_number: 4, reactant: "邻氯苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "邻氯苯重氮盐", reaction_type: "取代反应" },
      { step_number: 5, reactant: "邻氯苯重氮盐", reagent: "CuCN, △", product: "邻氯苯甲腈", reaction_type: "取代反应" },
      { step_number: 6, reactant: "邻氯苯甲腈", reagent: "(1) NaOH, H₂O, △; (2) HCl", product: "邻氯苯甲酸", reaction_type: "水解反应" },
      { step_number: 7, reactant: "邻氯苯甲酸", reagent: "(1) SOCl₂, △; (2) CH₃OH, 吡啶", product: "邻氯苯甲酸甲酯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 39,
    title: "对甲基苯甲酸乙酯合成路线",
    desc: "对二甲苯→对甲基苯甲酸乙酯(8步)，自由基卤代→水解→PCC氧化→银镜反应→酸化→酰氯化→甲醇酯化→酯交换，经典对位甲基芳香酯合成",
    steps: [
      { step_number: 1, reactant: "对二甲苯", reagent: "Cl₂, 光照", product: "对甲基苄基氯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对甲基苄基氯", reagent: "NaOH, H₂O, △", product: "对甲基苯甲醇", reaction_type: "水解反应" },
      { step_number: 3, reactant: "对甲基苯甲醇", reagent: "PCC, CH₂Cl₂", product: "对甲基苯甲醛", reaction_type: "氧化反应" },
      { step_number: 4, reactant: "对甲基苯甲醛", reagent: "Ag(NH₃)₂OH, △", product: "对甲基苯甲酸铵", reaction_type: "氧化反应" },
      { step_number: 5, reactant: "对甲基苯甲酸铵", reagent: "HCl, H₂O", product: "对甲基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 6, reactant: "对甲基苯甲酸", reagent: "SOCl₂, △", product: "对甲基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对甲基苯甲酰氯", reagent: "CH₃OH", product: "对甲基苯甲酸甲酯", reaction_type: "酯化反应" },
      { step_number: 8, reactant: "对甲基苯甲酸甲酯", reagent: "C₂H₅OH, H⁺, △", product: "对甲基苯甲酸乙酯", reaction_type: "酯化反应" }
    ]
  },
  {
    id: 40,
    title: "间苯二甲酸合成路线",
    desc: "间二甲苯→间苯二甲酸(8步)，自由基卤代→水解→PCC氧化→银镜反应→酸化→酯化保护→KMnO₄氧化→水解酸化，经典苯二甲酸合成",
    steps: [
      { step_number: 1, reactant: "间二甲苯", reagent: "Cl₂, 光照", product: "间甲基苄基氯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "间甲基苄基氯", reagent: "NaOH, H₂O, △", product: "间甲基苯甲醇", reaction_type: "水解反应" },
      { step_number: 3, reactant: "间甲基苯甲醇", reagent: "PCC, CH₂Cl₂", product: "间甲基苯甲醛", reaction_type: "氧化反应" },
      { step_number: 4, reactant: "间甲基苯甲醛", reagent: "Ag(NH₃)₂OH, △", product: "间甲基苯甲酸铵", reaction_type: "氧化反应" },
      { step_number: 5, reactant: "间甲基苯甲酸铵", reagent: "HCl, H₂O", product: "间甲基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 6, reactant: "间甲基苯甲酸", reagent: "CH₃OH, 浓H₂SO₄, △", product: "间甲基苯甲酸甲酯", reaction_type: "酯化反应" },
      { step_number: 7, reactant: "间甲基苯甲酸甲酯", reagent: "KMnO₄, OH⁻, △", product: "间苯二甲酸单甲酯钾", reaction_type: "氧化反应" },
      { step_number: 8, reactant: "间苯二甲酸单甲酯钾", reagent: "(1) HCl; (2) H₂O, H⁺, △", product: "间苯二甲酸", reaction_type: "水解反应" }
    ]
  },
  {
    id: 41,
    title: "肉桂酸乙酯合成路线",
    desc: "苯→肉桂酸乙酯(8步)，FC烷基化→自由基卤代→水解→PCC氧化→羟醛缩合→银镜反应→酸化→酯化，经典α,β-不饱和芳香酯合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "CH₃Cl, AlCl₃, △", product: "甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "甲苯", reagent: "Cl₂, 光照", product: "苄基氯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "苄基氯", reagent: "NaOH, H₂O, △", product: "苯甲醇", reaction_type: "水解反应" },
      { step_number: 4, reactant: "苯甲醇", reagent: "PCC, CH₂Cl₂", product: "苯甲醛", reaction_type: "氧化反应" },
      { step_number: 5, reactant: "苯甲醛", reagent: "CH₃CHO, NaOH, △", product: "肉桂醛", reaction_type: "加成反应" },
      { step_number: 6, reactant: "肉桂醛", reagent: "Ag(NH₃)₂OH, △", product: "肉桂酸铵", reaction_type: "氧化反应" },
      { step_number: 7, reactant: "肉桂酸铵", reagent: "HCl, H₂O", product: "肉桂酸", reaction_type: "酸碱反应" },
      { step_number: 8, reactant: "肉桂酸", reagent: "(1) SOCl₂, △; (2) C₂H₅OH, 吡啶", product: "肉桂酸乙酯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 42,
    title: "对乙酰氨基苯甲酸合成路线",
    desc: "甲苯→对乙酰氨基苯甲酸(8步)，硝化→自由基卤代→水解→Fe/HCl还原→乙酰化保护→PCC氧化→银镜反应→酸化，经典对乙酰氨基苯甲酸合成",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "Cl₂, 光照", product: "对硝基苄基氯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "对硝基苄基氯", reagent: "NaOH, H₂O, △", product: "对硝基苯甲醇", reaction_type: "水解反应" },
      { step_number: 4, reactant: "对硝基苯甲醇", reagent: "Fe, HCl, △", product: "对氨基苯甲醇", reaction_type: "还原反应" },
      { step_number: 5, reactant: "对氨基苯甲醇", reagent: "(CH₃CO)₂O, △", product: "对乙酰氨基苯甲醇", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对乙酰氨基苯甲醇", reagent: "PCC, CH₂Cl₂", product: "对乙酰氨基苯甲醛", reaction_type: "氧化反应" },
      { step_number: 7, reactant: "对乙酰氨基苯甲醛", reagent: "Ag(NH₃)₂OH, △", product: "对乙酰氨基苯甲酸铵", reaction_type: "氧化反应" },
      { step_number: 8, reactant: "对乙酰氨基苯甲酸铵", reagent: "HCl, H₂O", product: "对乙酰氨基苯甲酸", reaction_type: "酸碱反应" }
    ]
  },
  {
    id: 43,
    title: "对乙酰基苯甲腈合成路线",
    desc: "苯→对乙酰基苯甲腈(7步)，硝化→还原→乙酰化保护→FC酰基化→水解→重氮化→Sandmeyer氰化，经典对位氰基芳酮合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "CH₃COCl, AlCl₃, △", product: "对乙酰氨基苯乙酮", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对乙酰氨基苯乙酮", reagent: "HCl, H₂O, △", product: "对氨基苯乙酮", reaction_type: "水解反应" },
      { step_number: 6, reactant: "对氨基苯乙酮", reagent: "NaNO₂, HCl, 0-5°C", product: "对乙酰基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对乙酰基苯重氮盐", reagent: "CuCN, △", product: "对乙酰基苯甲腈", reaction_type: "取代反应" }
    ]
  },
  {
    id: 44,
    title: "对甲苯胺合成路线",
    desc: "甲苯→对甲苯胺(7步)，硝化→还原→乙酰化→氧化→酸化→还原→脱保护，经典甲基苯胺合成",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "Fe, HCl, △", product: "对甲苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "对甲苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "对甲基乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "对甲基乙酰苯胺", reagent: "KMnO₄, OH⁻, △", product: "对乙酰氨基苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 5, reactant: "对乙酰氨基苯甲酸钾", reagent: "HCl, H₂O", product: "对乙酰氨基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 6, reactant: "对乙酰氨基苯甲酸", reagent: "Fe, HCl, △", product: "对氨基苯甲酸", reaction_type: "还原反应" },
      { step_number: 7, reactant: "对氨基苯甲酸", reagent: "NaOH, H₂O, △; (2) HCl", product: "对甲苯胺", reaction_type: "脱羧反应" }
    ]
  },
  {
    id: 45,
    title: "间溴硝基苯合成路线",
    desc: "苯→间溴硝基苯(7步)，硝化→还原→乙酰化→硝化→水解脱保护→重氮化→Sandmeyer溴代，利用乙酰氨基的间位定位效应",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "间硝基乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 5, reactant: "间硝基乙酰苯胺", reagent: "HCl, H₂O, △", product: "间硝基苯胺", reaction_type: "水解反应" },
      { step_number: 6, reactant: "间硝基苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "间硝基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 7, reactant: "间硝基苯重氮盐", reagent: "CuBr, △", product: "间溴硝基苯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 46,
    title: "N-甲基对溴苯胺合成路线",
    desc: "苯→N-甲基对溴苯胺(7步)，硝化→还原→乙酰化→N-甲基化→水解→重氮化→Sandmeyer溴代，经典对溴-N-甲基苯胺合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "CH₃I, K₂CO₃, DMF", product: "N-甲基乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 5, reactant: "N-甲基乙酰苯胺", reagent: "HCl, H₂O, △", product: "N-甲基苯胺", reaction_type: "水解反应" },
      { step_number: 6, reactant: "N-甲基苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "N-甲基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 7, reactant: "N-甲基苯重氮盐", reagent: "CuBr, △", product: "N-甲基对溴苯胺", reaction_type: "取代反应" }
    ]
  },
  {
    id: 47,
    title: "邻氯溴苯合成路线",
    desc: "苯→邻氯溴苯(7步)，硝化→还原→乙酰化→邻位氯化→水解→重氮化→Sandmeyer溴代，利用乙酰氨基的邻对位定位效应",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "Cl₂, FeCl₃, 低温", product: "邻氯乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 5, reactant: "邻氯乙酰苯胺", reagent: "HCl, H₂O, △", product: "邻氯苯胺", reaction_type: "水解反应" },
      { step_number: 6, reactant: "邻氯苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "邻氯苯重氮盐", reaction_type: "取代反应" },
      { step_number: 7, reactant: "邻氯苯重氮盐", reagent: "CuBr, △", product: "邻氯溴苯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 48,
    title: "对羟基苯甲酸合成路线",
    desc: "苯→对羟基苯甲酸(7步)，硝化→还原→重氮化→水解→亚硝化→还原→重氮化/Sandmeyer氰化→水解，经苯酚中间体的对位亚硝化策略",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯重氮盐", reagent: "H₂O, △", product: "苯酚", reaction_type: "取代反应" },
      { step_number: 5, reactant: "苯酚", reagent: "NaNO₂, HCl, 0-5°C", product: "对亚硝基苯酚", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对亚硝基苯酚", reagent: "Na₂S₂O₄, NaOH, H₂O", product: "对氨基苯酚", reaction_type: "还原反应" },
      { step_number: 7, reactant: "对氨基苯酚", reagent: "NaNO₂, HCl, 0-5°C; (2) CuCN, △; (3) NaOH, H₂O, △; (4) HCl", product: "对羟基苯甲酸", reaction_type: "取代反应" }
    ]
  },
  {
    id: 49,
    title: "对溴碘苯合成路线",
    desc: "苯→对溴碘苯(7步)，硝化→还原→乙酰化→溴化→水解→重氮化→Sandmeyer碘代，乙酰氨基定位的对位溴代策略",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "Br₂, FeBr₃, 低温", product: "对溴乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对溴乙酰苯胺", reagent: "HCl, H₂O, △", product: "对溴苯胺", reaction_type: "水解反应" },
      { step_number: 6, reactant: "对溴苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "对溴苯重氮盐", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对溴苯重氮盐", reagent: "KI, △", product: "对溴碘苯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 50,
    title: "对硝基溴苯合成路线",
    desc: "苯→对硝基溴苯(7步)，硝化→还原→乙酰化→硝化→水解→重氮化→Sandmeyer溴代，利用乙酰氨基定位的二次硝化",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "对硝基乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对硝基乙酰苯胺", reagent: "HCl, H₂O, △", product: "对硝基苯胺", reaction_type: "水解反应" },
      { step_number: 6, reactant: "对硝基苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "对硝基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对硝基苯重氮盐", reagent: "CuBr, △", product: "对硝基溴苯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 51,
    title: "对氯苯磺酸合成路线",
    desc: "苯→对氯苯磺酸(7步)，硝化→还原→乙酰化→氯磺化→水解→重氮化→Sandmeyer氯代，经乙酰苯胺氯磺化策略",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "ClSO₃H, △", product: "对乙酰氨基苯磺酰氯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对乙酰氨基苯磺酰氯", reagent: "H₂O, △", product: "对乙酰氨基苯磺酸", reaction_type: "水解反应" },
      { step_number: 6, reactant: "对乙酰氨基苯磺酸", reagent: "HCl, H₂O, △", product: "对氨基苯磺酸", reaction_type: "水解反应" },
      { step_number: 7, reactant: "对氨基苯磺酸", reagent: "NaNO₂, HCl, 0-5°C; (2) CuCl, △", product: "对氯苯磺酸", reaction_type: "取代反应" }
    ]
  },
  {
    id: 52,
    title: "苯肼合成路线",
    desc: "苯→苯肼(7步)，硝化→还原→重氮化→还原→乙酰化→硝化→还原，经典重氮盐还原法",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯重氮盐", reagent: "SnCl₂, HCl, 0°C", product: "苯肼", reaction_type: "还原反应" },
      { step_number: 5, reactant: "苯肼", reagent: "(CH₃CO)₂O, 吡啶", product: "N-乙酰苯肼", reaction_type: "取代反应" },
      { step_number: 6, reactant: "N-乙酰苯肼", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "对硝基-N-乙酰苯肼", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对硝基-N-乙酰苯肼", reagent: "(1) HCl, H₂O, △; (2) Fe, HCl, △", product: "对氨基苯肼", reaction_type: "还原反应" }
    ]
  },
  {
    id: 53,
    title: "对二溴苯合成路线",
    desc: "苯→对二溴苯(7步)，硝化→还原→乙酰化→硝化→水解→还原→重氮化/Sandmeyer溴代，经典对二卤代苯合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "对硝基乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对硝基乙酰苯胺", reagent: "HCl, H₂O, △", product: "对硝基苯胺", reaction_type: "水解反应" },
      { step_number: 6, reactant: "对硝基苯胺", reagent: "Fe, HCl, △", product: "对苯二胺", reaction_type: "还原反应" },
      { step_number: 7, reactant: "对苯二胺", reagent: "(1) NaNO₂, HCl, 0-5°C; (2) CuBr, △", product: "对二溴苯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 54,
    title: "对氰基苯甲酰胺合成路线",
    desc: "甲苯→对氰基苯甲酰胺(7步)，硝化→氧化→酸化→酰氯化→酰胺化→还原→重氮化/Sandmeyer氰化，PABA衍生物合成",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "KMnO₄, OH⁻, △", product: "对硝基苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 3, reactant: "对硝基苯甲酸钾", reagent: "HCl, H₂O", product: "对硝基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "对硝基苯甲酸", reagent: "SOCl₂, △", product: "对硝基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对硝基苯甲酰氯", reagent: "NH₃, 0°C", product: "对硝基苯甲酰胺", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对硝基苯甲酰胺", reagent: "Fe, HCl, △", product: "对氨基苯甲酰胺", reaction_type: "还原反应" },
      { step_number: 7, reactant: "对氨基苯甲酰胺", reagent: "NaNO₂, HCl, 0-5°C; (2) CuCN, △", product: "对氰基苯甲酰胺", reaction_type: "取代反应" }
    ]
  },
  {
    id: 55,
    title: "2,4-二甲基苯胺合成路线",
    desc: "间二甲苯→2,4-二甲基苯胺(8步)，硝化→还原→重氮化→Sandmeyer氰化→水解→酰氯化→酰胺化→Hofmann重排，巧妙利用Hofmann重排循环",
    steps: [
      { step_number: 1, reactant: "间二甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "2,4-二甲基硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "2,4-二甲基硝基苯", reagent: "Fe, HCl, △", product: "2,4-二甲基苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "2,4-二甲基苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "2,4-二甲基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "2,4-二甲基苯重氮盐", reagent: "CuCN, NaCN, △", product: "2,4-二甲基苯甲腈", reaction_type: "取代反应" },
      { step_number: 5, reactant: "2,4-二甲基苯甲腈", reagent: "HCl, H₂O, △", product: "2,4-二甲基苯甲酸", reaction_type: "水解反应" },
      { step_number: 6, reactant: "2,4-二甲基苯甲酸", reagent: "SOCl₂, △", product: "2,4-二甲基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "2,4-二甲基苯甲酰氯", reagent: "NH₃, 0°C", product: "2,4-二甲基苯甲酰胺", reaction_type: "取代反应" },
      { step_number: 8, reactant: "2,4-二甲基苯甲酰胺", reagent: "Br₂, NaOH, △", product: "2,4-二甲基苯胺", reaction_type: "重排反应" }
    ]
  },
  {
    id: 56,
    title: "N-乙酰基对溴苯胺合成路线",
    desc: "甲苯→N-乙酰基对溴苯胺(7步)，硝化→还原→重氮化→水解→Bucherer胺化→乙酰化→重氮化/Sandmeyer溴代，经酚中间体Bucherer胺化策略",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "Fe, HCl, △", product: "对甲苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "对甲苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "对甲基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "对甲基苯重氮盐", reagent: "H₂O, △", product: "对甲苯酚", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对甲苯酚", reagent: "(1) NaHSO₃, NH₃, △; (2) NaOH", product: "对甲苯胺", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对甲苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "N-乙酰基对甲苯胺", reaction_type: "取代反应" },
      { step_number: 7, reactant: "N-乙酰基对甲苯胺", reagent: "NaNO₂, HCl, 0-5°C; (2) CuBr, △", product: "N-乙酰基对溴苯胺", reaction_type: "取代反应" }
    ]
  },
  {
    id: 57,
    title: "邻溴苯甲酸合成路线",
    desc: "甲苯→邻溴苯甲酸(7步)，硝化→还原→乙酰化→KMnO₄氧化→酸化→水解脱保护→重氮化/Sandmeyer溴代，利用乙酰基保护氨基的氧化策略",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "邻硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "邻硝基甲苯", reagent: "Fe, HCl, △", product: "邻甲苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "邻甲苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "邻甲基乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "邻甲基乙酰苯胺", reagent: "KMnO₄, OH⁻, △", product: "邻乙酰氨基苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 5, reactant: "邻乙酰氨基苯甲酸钾", reagent: "HCl, H₂O", product: "邻乙酰氨基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 6, reactant: "邻乙酰氨基苯甲酸", reagent: "HCl, H₂O, △", product: "邻氨基苯甲酸", reaction_type: "水解反应" },
      { step_number: 7, reactant: "邻氨基苯甲酸", reagent: "NaNO₂, HCl, 0-5°C; (2) CuBr, △", product: "邻溴苯甲酸", reaction_type: "取代反应" }
    ]
  },
  {
    id: 58,
    title: "对氨基苯甲腈合成路线",
    desc: "甲苯→对氨基苯甲腈(7步)，硝化→氧化→酸化→酰氯化→酰胺化→脱水→还原，经酰胺脱水的腈基引入策略",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "KMnO₄, OH⁻, △", product: "对硝基苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 3, reactant: "对硝基苯甲酸钾", reagent: "HCl, H₂O", product: "对硝基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "对硝基苯甲酸", reagent: "SOCl₂, △", product: "对硝基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对硝基苯甲酰氯", reagent: "NH₃, 0°C", product: "对硝基苯甲酰胺", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对硝基苯甲酰胺", reagent: "P₂O₅, △", product: "对硝基苯甲腈", reaction_type: "消去反应" },
      { step_number: 7, reactant: "对硝基苯甲腈", reagent: "Fe, HCl, △", product: "对氨基苯甲腈", reaction_type: "还原反应" }
    ]
  },
  {
    id: 59,
    title: "对溴-4′-硝基偶氮苯合成路线",
    desc: "苯→对溴-4′-硝基偶氮苯(7步)，硝化→还原→重氮化→偶合→重氮化→Sandmeyer溴代→硝化，重氮偶合与Sandmeyer策略",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯重氮盐", reagent: "苯胺, NaOAc, H₂O, 0°C", product: "对氨基偶氮苯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对氨基偶氮苯", reagent: "NaNO₂, HCl, 0-5°C", product: "偶氮苯重氮盐", reaction_type: "取代反应" },
      { step_number: 6, reactant: "偶氮苯重氮盐", reagent: "CuBr, △", product: "对溴偶氮苯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对溴偶氮苯", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "对溴-4′-硝基偶氮苯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 60,
    title: "对溴苯乙酸合成路线",
    desc: "甲苯→对溴苯乙酸(7步)，硝化→自由基卤代→腈化→水解→还原→重氮化→Sandmeyer溴代，硝基保护下的侧链延伸策略",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "Cl₂, 光照", product: "对硝基苄基氯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "对硝基苄基氯", reagent: "KCN, C₂H₅OH, △", product: "对硝基苯乙腈", reaction_type: "取代反应" },
      { step_number: 4, reactant: "对硝基苯乙腈", reagent: "HCl, H₂O, △", product: "对硝基苯乙酸", reaction_type: "水解反应" },
      { step_number: 5, reactant: "对硝基苯乙酸", reagent: "Fe, HCl, △", product: "对氨基苯乙酸", reaction_type: "还原反应" },
      { step_number: 6, reactant: "对氨基苯乙酸", reagent: "NaNO₂, HCl, 0-5°C", product: "对羧甲基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对羧甲基苯重氮盐", reagent: "CuBr, △", product: "对溴苯乙酸", reaction_type: "取代反应" }
    ]
  },
  {
    id: 61,
    title: "间氨基苯酚合成路线",
    desc: "苯→间氨基苯酚(8步)，硝化→还原→重氮化→水解→磺化→硝化→碱熔→还原，经磺化碱熔的间位定位策略",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯重氮盐", reagent: "H₂O, △", product: "苯酚", reaction_type: "取代反应" },
      { step_number: 5, reactant: "苯酚", reagent: "浓H₂SO₄, △", product: "间羟基苯磺酸", reaction_type: "取代反应" },
      { step_number: 6, reactant: "间羟基苯磺酸", reagent: "浓HNO₃, 浓H₂SO₄", product: "间硝基间羟基苯磺酸", reaction_type: "取代反应" },
      { step_number: 7, reactant: "间硝基间羟基苯磺酸", reagent: "NaOH, 熔融, △", product: "间硝基苯酚钠", reaction_type: "取代反应" },
      { step_number: 8, reactant: "间硝基苯酚钠", reagent: "(1) HCl, H₂O; (2) Fe, HCl, △", product: "间氨基苯酚", reaction_type: "还原反应" }
    ]
  },
  {
    id: 62,
    title: "对氨基-N,N-二甲基苯胺合成路线",
    desc: "苯→对氨基-N,N-二甲基苯胺(8步)，硝化→还原→重氮化→Sandmeyer氯代→硝化→还原→N,N-二甲基化→氨解，经对氯硝基苯策略",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯重氮盐", reagent: "CuCl, HCl, △", product: "氯苯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "氯苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基氯苯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对硝基氯苯", reagent: "Fe, HCl, △", product: "对氯苯胺", reaction_type: "还原反应" },
      { step_number: 7, reactant: "对氯苯胺", reagent: "2CH₃I, K₂CO₃, DMF", product: "对氯-N,N-二甲基苯胺", reaction_type: "取代反应" },
      { step_number: 8, reactant: "对氯-N,N-二甲基苯胺", reagent: "NaNH₂, NH₃(液), -33°C", product: "对氨基-N,N-二甲基苯胺", reaction_type: "取代反应" }
    ]
  },
  {
    id: 63,
    title: "对氯苯磺酰苯胺合成路线",
    desc: "苯→对氯苯磺酰苯胺(7步)，硝化→还原→乙酰化→氯磺化→Schotten-Baumann酰胺化→水解→重氮化/Sandmeyer氯代，磺胺类衍生物合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "ClSO₃H, △", product: "对乙酰氨基苯磺酰氯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对乙酰氨基苯磺酰氯", reagent: "苯胺, NaOH, 0°C", product: "对乙酰氨基苯磺酰苯胺", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对乙酰氨基苯磺酰苯胺", reagent: "HCl, H₂O, △", product: "对氨基苯磺酰苯胺", reaction_type: "水解反应" },
      { step_number: 7, reactant: "对氨基苯磺酰苯胺", reagent: "NaNO₂, HCl, 0-5°C; (2) CuCl, △", product: "对氯苯磺酰苯胺", reaction_type: "取代反应" }
    ]
  },
  {
    id: 64,
    title: "对溴偶氮苯合成路线",
    desc: "苯→对溴偶氮苯(8步)，硝化→还原→重氮化→偶合→重氮化→Sandmeyer溴代→纯化→纯化，经典偶氮染料中间体合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯重氮盐", reagent: "苯胺, NaOAc, H₂O, 0°C", product: "对氨基偶氮苯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对氨基偶氮苯", reagent: "NaNO₂, HCl, 0-5°C", product: "偶氮苯重氮盐", reaction_type: "取代反应" },
      { step_number: 6, reactant: "偶氮苯重氮盐", reagent: "CuBr, △", product: "对溴偶氮苯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对溴偶氮苯", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "对溴-4′-硝基偶氮苯", reaction_type: "取代反应" },
      { step_number: 8, reactant: "对溴-4′-硝基偶氮苯", reagent: "Fe, HCl, △", product: "对溴-4′-氨基偶氮苯", reaction_type: "还原反应" }
    ]
  },
  {
    id: 65,
    title: "邻氨基苯甲酰胺合成路线",
    desc: "甲苯→邻氨基苯甲酰胺(8步)，硝化→还原→乙酰化→KMnO₄氧化→酸化→水解脱保护→酰氯化→酰胺化，经典邻位取代苯甲酰胺合成",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "邻硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "邻硝基甲苯", reagent: "Fe, HCl, △", product: "邻甲苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "邻甲苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "邻甲基乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "邻甲基乙酰苯胺", reagent: "KMnO₄, OH⁻, △", product: "邻乙酰氨基苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 5, reactant: "邻乙酰氨基苯甲酸钾", reagent: "HCl, H₂O", product: "邻乙酰氨基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 6, reactant: "邻乙酰氨基苯甲酸", reagent: "HCl, H₂O, △", product: "邻氨基苯甲酸", reaction_type: "水解反应" },
      { step_number: 7, reactant: "邻氨基苯甲酸", reagent: "SOCl₂, △", product: "邻氨基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 8, reactant: "邻氨基苯甲酰氯", reagent: "NH₃, 0°C", product: "邻氨基苯甲酰胺", reaction_type: "取代反应" }
    ]
  },
  {
    id: 66,
    title: "对氰基苯甲醛合成路线",
    desc: "甲苯→对氰基苯甲醛(8步)，硝化→氧化→酸化→酰氯化→LiAlH₄还原→PCC氧化→还原→重氮化/Sandmeyer氰化，经对硝基苯甲酰氯部分还原策略",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "KMnO₄, OH⁻, △", product: "对硝基苯甲酸钾", reaction_type: "氧化反应" },
      { step_number: 3, reactant: "对硝基苯甲酸钾", reagent: "HCl, H₂O", product: "对硝基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "对硝基苯甲酸", reagent: "SOCl₂, △", product: "对硝基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对硝基苯甲酰氯", reagent: "LiAlH(OtBu)₃, 无水乙醚, −78°C", product: "对硝基苯甲醇", reaction_type: "还原反应" },
      { step_number: 6, reactant: "对硝基苯甲醇", reagent: "PCC, CH₂Cl₂", product: "对硝基苯甲醛", reaction_type: "氧化反应" },
      { step_number: 7, reactant: "对硝基苯甲醛", reagent: "Fe, HCl, △", product: "对氨基苯甲醛", reaction_type: "还原反应" },
      { step_number: 8, reactant: "对氨基苯甲醛", reagent: "NaNO₂, HCl, 0-5°C; (2) CuCN, △", product: "对氰基苯甲醛", reaction_type: "取代反应" }
    ]
  },
  {
    id: 67,
    title: "苯磺酰胺合成路线",
    desc: "苯→苯磺酰胺(8步)，硝化→还原→乙酰化→氯磺化→酰胺化→水解脱保护→重氮化→脱氨基，经对氨基苯磺酰胺脱氨基的经典策略",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "ClSO₃H, △", product: "对乙酰氨基苯磺酰氯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对乙酰氨基苯磺酰氯", reagent: "NH₃, 0°C", product: "对乙酰氨基苯磺酰胺", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对乙酰氨基苯磺酰胺", reagent: "HCl, H₂O, △", product: "对氨基苯磺酰胺", reaction_type: "水解反应" },
      { step_number: 7, reactant: "对氨基苯磺酰胺", reagent: "NaNO₂, HCl, 0-5°C", product: "对磺酰胺基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 8, reactant: "对磺酰胺基苯重氮盐", reagent: "H₃PO₂, H₂O, 0°C", product: "苯磺酰胺", reaction_type: "还原反应" }
    ]
  },
  {
    id: 68,
    title: "对溴苯乙酸乙酯合成路线",
    desc: "甲苯→对溴苯乙酸乙酯(8步)，硝化→自由基卤代→腈化→水解→酯化→还原→重氮化→Sandmeyer溴代，侧链延伸与氨基保护策略",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "Cl₂, 光照", product: "对硝基苄基氯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "对硝基苄基氯", reagent: "KCN, C₂H₅OH, △", product: "对硝基苯乙腈", reaction_type: "取代反应" },
      { step_number: 4, reactant: "对硝基苯乙腈", reagent: "HCl, H₂O, △", product: "对硝基苯乙酸", reaction_type: "水解反应" },
      { step_number: 5, reactant: "对硝基苯乙酸", reagent: "C₂H₅OH, 浓H₂SO₄, △", product: "对硝基苯乙酸乙酯", reaction_type: "酯化反应" },
      { step_number: 6, reactant: "对硝基苯乙酸乙酯", reagent: "Fe, HCl, △", product: "对氨基苯乙酸乙酯", reaction_type: "还原反应" },
      { step_number: 7, reactant: "对氨基苯乙酸乙酯", reagent: "NaNO₂, HCl, 0-5°C", product: "对乙氧羰基甲基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 8, reactant: "对乙氧羰基甲基苯重氮盐", reagent: "CuBr, △", product: "对溴苯乙酸乙酯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 69,
    title: "水杨醛合成路线",
    desc: "苯→水杨醛(7步)，硝化→还原→重氮化→水解→Reimer-Tiemann→加成→酸化，经典邻羟基芳醛合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯重氮盐", reagent: "H₂O, △", product: "苯酚", reaction_type: "取代反应" },
      { step_number: 5, reactant: "苯酚", reagent: "CHCl₃, NaOH, △", product: "水杨醛", reaction_type: "取代反应" },
      { step_number: 6, reactant: "水杨醛", reagent: "NaHSO₃, H₂O", product: "水杨醛亚硫酸氢钠", reaction_type: "加成反应" },
      { step_number: 7, reactant: "水杨醛亚硫酸氢钠", reagent: "HCl, H₂O", product: "水杨醛", reaction_type: "酸碱反应" }
    ]
  },
  {
    id: 70,
    title: "4,4′-二甲基二苯甲酮肟合成路线",
    desc: "甲苯→4,4′-二甲基二苯甲酮肟(8步)，硝化→还原→重氮化→Sandmeyer氰化→水解→酰氯化→FC酰基化→肟化，经典甲基二苯甲酮肟合成",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "Fe, HCl, △", product: "对甲苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "对甲苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "对甲基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "对甲基苯重氮盐", reagent: "CuCN, △", product: "对甲基苯甲腈", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对甲基苯甲腈", reagent: "HCl, H₂O, △", product: "对甲基苯甲酸", reaction_type: "水解反应" },
      { step_number: 6, reactant: "对甲基苯甲酸", reagent: "SOCl₂, △", product: "对甲基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对甲基苯甲酰氯", reagent: "甲苯, AlCl₃", product: "4,4′-二甲基二苯甲酮", reaction_type: "取代反应" },
      { step_number: 8, reactant: "4,4′-二甲基二苯甲酮", reagent: "NH₂OH·HCl, NaOAc, △", product: "4,4′-二甲基二苯甲酮肟", reaction_type: "加成反应" }
    ]
  },
  {
    id: 71,
    title: "邻氯苯甲酸合成路线",
    desc: "甲苯→邻氯苯甲酸(8步)，自由基卤代→水解→PCC氧化→硝化→还原→重氮化/Sandmeyer氯代→银镜反应→酸化，经典邻位氯代苯甲酸合成",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "Cl₂, 光照", product: "苄基氯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苄基氯", reagent: "NaOH, H₂O, △", product: "苯甲醇", reaction_type: "水解反应" },
      { step_number: 3, reactant: "苯甲醇", reagent: "PCC, CH₂Cl₂", product: "苯甲醛", reaction_type: "氧化反应" },
      { step_number: 4, reactant: "苯甲醛", reagent: "浓HNO₃, 浓H₂SO₄", product: "间硝基苯甲醛", reaction_type: "取代反应" },
      { step_number: 5, reactant: "间硝基苯甲醛", reagent: "Fe, HCl, △", product: "间氨基苯甲醛", reaction_type: "还原反应" },
      { step_number: 6, reactant: "间氨基苯甲醛", reagent: "NaNO₂, HCl, 0-5°C; (2) CuCl, △", product: "间氯苯甲醛", reaction_type: "取代反应" },
      { step_number: 7, reactant: "间氯苯甲醛", reagent: "Ag(NH₃)₂OH, △", product: "间氯苯甲酸铵", reaction_type: "氧化反应" },
      { step_number: 8, reactant: "间氯苯甲酸铵", reagent: "HCl, H₂O", product: "间氯苯甲酸", reaction_type: "酸碱反应" }
    ]
  },
  {
    id: 72,
    title: "α-叠氮苯丙酮合成路线",
    desc: "苯→α-叠氮苯丙酮(7步)，FC酰基化→卤仿→酸化→酰氯化→Grignard加成→α-溴代→叠氮取代，经典α-叠氮芳酮合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "CH₃COCl, AlCl₃", product: "苯乙酮", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯乙酮", reagent: "Br₂, NaOH, △", product: "苯甲酸钠", reaction_type: "取代反应" },
      { step_number: 3, reactant: "苯甲酸钠", reagent: "HCl, H₂O", product: "苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "苯甲酸", reagent: "SOCl₂, △", product: "苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "苯甲酰氯", reagent: "CH₃CH₂MgBr, 无水乙醚", product: "苯丙酮", reaction_type: "加成反应" },
      { step_number: 6, reactant: "苯丙酮", reagent: "Br₂, CH₃COOH, 0°C", product: "α-溴苯丙酮", reaction_type: "取代反应" },
      { step_number: 7, reactant: "α-溴苯丙酮", reagent: "NaN₃, DMF, 0°C", product: "α-叠氮苯丙酮", reaction_type: "取代反应" }
    ]
  },
  {
    id: 73,
    title: "对甲氧基苯乙酮肟合成路线",
    desc: "苯酚→对甲氧基苯乙酮肟(7步)，Williamson醚化→FC酰基化→卤仿→酸化→酰氯化→Grignard→肟化，经典对甲氧基芳酮肟合成",
    steps: [
      { step_number: 1, reactant: "苯酚", reagent: "CH₃I, K₂CO₃, DMF", product: "苯甲醚", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯甲醚", reagent: "CH₃COCl, AlCl₃", product: "对甲氧基苯乙酮", reaction_type: "取代反应" },
      { step_number: 3, reactant: "对甲氧基苯乙酮", reagent: "Br₂, NaOH, △", product: "对甲氧基苯甲酸钠", reaction_type: "取代反应" },
      { step_number: 4, reactant: "对甲氧基苯甲酸钠", reagent: "HCl, H₂O", product: "对甲氧基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 5, reactant: "对甲氧基苯甲酸", reagent: "SOCl₂, △", product: "对甲氧基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对甲氧基苯甲酰氯", reagent: "CH₃MgBr, 无水乙醚", product: "对甲氧基苯乙酮", reaction_type: "加成反应" },
      { step_number: 7, reactant: "对甲氧基苯乙酮", reagent: "NH₂OH·HCl, NaOAc, △", product: "对甲氧基苯乙酮肟", reaction_type: "加成反应" }
    ]
  },
  {
    id: 74,
    title: "对硝基苯乙酮肟合成路线",
    desc: "苯→对硝基苯乙酮肟(8步)，FC酰基化→硝化→还原→乙酰化→硝化→水解→重氮化→脱氨基→肟化，利用乙酰氨基定位的对位硝化策略",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "CH₃COCl, AlCl₃", product: "苯乙酮", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯乙酮", reagent: "浓HNO₃, 浓H₂SO₄", product: "间硝基苯乙酮", reaction_type: "取代反应" },
      { step_number: 3, reactant: "间硝基苯乙酮", reagent: "Fe, HCl, △", product: "间氨基苯乙酮", reaction_type: "还原反应" },
      { step_number: 4, reactant: "间氨基苯乙酮", reagent: "(CH₃CO)₂O, 吡啶", product: "间乙酰氨基苯乙酮", reaction_type: "取代反应" },
      { step_number: 5, reactant: "间乙酰氨基苯乙酮", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "间乙酰氨基对硝基苯乙酮", reaction_type: "取代反应" },
      { step_number: 6, reactant: "间乙酰氨基对硝基苯乙酮", reagent: "HCl, H₂O, △", product: "间氨基对硝基苯乙酮", reaction_type: "水解反应" },
      { step_number: 7, reactant: "间氨基对硝基苯乙酮", reagent: "NaNO₂, HCl, 0-5°C; (2) H₃PO₂, H₂O", product: "对硝基苯乙酮", reaction_type: "取代反应" },
      { step_number: 8, reactant: "对硝基苯乙酮", reagent: "NH₂OH·HCl, NaOAc, △", product: "对硝基苯乙酮肟", reaction_type: "加成反应" }
    ]
  },
  {
    id: 75,
    title: "间硝基苯甲酸合成路线",
    desc: "甲苯→间硝基苯甲酸(7步)，自由基卤代→水解→PCC氧化→硝化(间位)→银镜反应→酸化→纯化，利用甲酰基间位定位效应",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "Cl₂, 光照", product: "苄基氯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苄基氯", reagent: "NaOH, H₂O, △", product: "苯甲醇", reaction_type: "水解反应" },
      { step_number: 3, reactant: "苯甲醇", reagent: "PCC, CH₂Cl₂", product: "苯甲醛", reaction_type: "氧化反应" },
      { step_number: 4, reactant: "苯甲醛", reagent: "浓HNO₃, 浓H₂SO₄", product: "间硝基苯甲醛", reaction_type: "取代反应" },
      { step_number: 5, reactant: "间硝基苯甲醛", reagent: "Ag(NH₃)₂OH, △", product: "间硝基苯甲酸铵", reaction_type: "氧化反应" },
      { step_number: 6, reactant: "间硝基苯甲酸铵", reagent: "HCl, H₂O", product: "间硝基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 7, reactant: "间硝基苯甲酸", reagent: "SOCl₂, △; (2) NH₃, 0°C", product: "间硝基苯甲酰胺", reaction_type: "取代反应" }
    ]
  },
  {
    id: 76,
    title: "对羟基苯丙酮肟合成路线",
    desc: "苯酚→对羟基苯丙酮肟(8步)，Williamson醚化→FC酰基化→卤仿→酸化→酰氯化→Grignard→醚键断裂→肟化，经典对羟基芳酮肟合成",
    steps: [
      { step_number: 1, reactant: "苯酚", reagent: "CH₃I, K₂CO₃, DMF", product: "苯甲醚", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯甲醚", reagent: "CH₃COCl, AlCl₃", product: "对甲氧基苯乙酮", reaction_type: "取代反应" },
      { step_number: 3, reactant: "对甲氧基苯乙酮", reagent: "Br₂, NaOH, △", product: "对甲氧基苯甲酸钠", reaction_type: "取代反应" },
      { step_number: 4, reactant: "对甲氧基苯甲酸钠", reagent: "HCl, H₂O", product: "对甲氧基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 5, reactant: "对甲氧基苯甲酸", reagent: "SOCl₂, △", product: "对甲氧基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对甲氧基苯甲酰氯", reagent: "CH₃CH₂MgBr, 无水乙醚", product: "对甲氧基苯丙酮", reaction_type: "加成反应" },
      { step_number: 7, reactant: "对甲氧基苯丙酮", reagent: "HI, △", product: "对羟基苯丙酮", reaction_type: "取代反应" },
      { step_number: 8, reactant: "对羟基苯丙酮", reagent: "NH₂OH·HCl, NaOAc, △", product: "对羟基苯丙酮肟", reaction_type: "加成反应" }
    ]
  },
  {
    id: 77,
    title: "α-叠氮苯丁酮合成路线",
    desc: "苯→α-叠氮苯丁酮(7步)，FC酰基化→卤仿→酸化→酰氯化→Grignard加成→α-溴代→叠氮取代，经典α-叠氮芳酮合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "CH₃COCl, AlCl₃", product: "苯乙酮", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯乙酮", reagent: "Br₂, NaOH, △", product: "苯甲酸钠", reaction_type: "取代反应" },
      { step_number: 3, reactant: "苯甲酸钠", reagent: "HCl, H₂O", product: "苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "苯甲酸", reagent: "SOCl₂, △", product: "苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "苯甲酰氯", reagent: "CH₃CH₂CH₂MgBr, 无水乙醚", product: "苯丁酮", reaction_type: "加成反应" },
      { step_number: 6, reactant: "苯丁酮", reagent: "Br₂, CH₃COOH, 0°C", product: "α-溴苯丁酮", reaction_type: "取代反应" },
      { step_number: 7, reactant: "α-溴苯丁酮", reagent: "NaN₃, DMF, 0°C", product: "α-叠氮苯丁酮", reaction_type: "取代反应" }
    ]
  },
  {
    id: 78,
    title: "对羟基苯丙酮合成路线",
    desc: "苯酚→对羟基苯丙酮(7步)，Williamson醚化→FC酰基化→卤仿→酸化→酰氯化→Grignard→醚键断裂，经典对羟基芳酮合成",
    steps: [
      { step_number: 1, reactant: "苯酚", reagent: "CH₃I, K₂CO₃, DMF", product: "苯甲醚", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯甲醚", reagent: "CH₃COCl, AlCl₃", product: "对甲氧基苯乙酮", reaction_type: "取代反应" },
      { step_number: 3, reactant: "对甲氧基苯乙酮", reagent: "Br₂, NaOH, △", product: "对甲氧基苯甲酸钠", reaction_type: "取代反应" },
      { step_number: 4, reactant: "对甲氧基苯甲酸钠", reagent: "HCl, H₂O", product: "对甲氧基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 5, reactant: "对甲氧基苯甲酸", reagent: "SOCl₂, △", product: "对甲氧基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对甲氧基苯甲酰氯", reagent: "CH₃CH₂MgBr, 无水乙醚", product: "对甲氧基苯丙酮", reaction_type: "加成反应" },
      { step_number: 7, reactant: "对甲氧基苯丙酮", reagent: "HI, △", product: "对羟基苯丙酮", reaction_type: "取代反应" }
    ]
  },
  {
    id: 79,
    title: "α-叠氮苯乙酮合成路线",
    desc: "苯→α-叠氮苯乙酮(7步)，硝化→还原→重氮化→Sandmeyer氰化→甲基Grignard加成→α-溴代→叠氮取代，经典α-叠氮芳酮合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯重氮盐", reagent: "CuCN, △", product: "苯甲腈", reaction_type: "取代反应" },
      { step_number: 5, reactant: "苯甲腈", reagent: "CH₃MgBr, 无水乙醚; (2) H₂O", product: "苯乙酮", reaction_type: "加成反应" },
      { step_number: 6, reactant: "苯乙酮", reagent: "Br₂, CH₃COOH, 0°C", product: "α-溴苯乙酮", reaction_type: "取代反应" },
      { step_number: 7, reactant: "α-溴苯乙酮", reagent: "NaN₃, DMF, 0°C", product: "α-叠氮苯乙酮", reaction_type: "取代反应" }
    ]
  },
  {
    id: 80,
    title: "间甲基苯甲醛合成路线",
    desc: "间二甲苯→间甲基苯甲醛(8步)，自由基卤代→水解→PCC氧化→加成→酸化→氧化→酸化→Rosenmund还原，经典间位甲基芳醛合成",
    steps: [
      { step_number: 1, reactant: "间二甲苯", reagent: "Cl₂, 光照", product: "间甲基苄基氯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "间甲基苄基氯", reagent: "NaOH, H₂O, △", product: "间甲基苯甲醇", reaction_type: "水解反应" },
      { step_number: 3, reactant: "间甲基苯甲醇", reagent: "PCC, CH₂Cl₂", product: "间甲基苯甲醛", reaction_type: "氧化反应" },
      { step_number: 4, reactant: "间甲基苯甲醛", reagent: "NaHSO₃, H₂O", product: "间甲基苯甲醛亚硫酸氢钠", reaction_type: "加成反应" },
      { step_number: 5, reactant: "间甲基苯甲醛亚硫酸氢钠", reagent: "HCl, H₂O", product: "间甲基苯甲醛", reaction_type: "酸碱反应" },
      { step_number: 6, reactant: "间甲基苯甲醛", reagent: "Ag(NH₃)₂OH, △", product: "间甲基苯甲酸铵", reaction_type: "氧化反应" },
      { step_number: 7, reactant: "间甲基苯甲酸铵", reagent: "HCl, H₂O", product: "间甲基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 8, reactant: "间甲基苯甲酸", reagent: "(1) SOCl₂, △; (2) H₂, Pd/BaSO₄, 喹啉", product: "间甲基苯甲醛", reaction_type: "还原反应" }
    ]
  },
  {
    id: 81,
    title: "4-羟基二苯甲酮肟合成路线",
    desc: "苯酚→4-羟基二苯甲酮肟(8步)，Williamson醚化→FC酰基化→卤仿→酸化→酰氯化→FC酰基化→醚键断裂→肟化，经典羟基二苯甲酮肟合成",
    steps: [
      { step_number: 1, reactant: "苯酚", reagent: "CH₃I, K₂CO₃, DMF", product: "苯甲醚", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯甲醚", reagent: "CH₃COCl, AlCl₃", product: "对甲氧基苯乙酮", reaction_type: "取代反应" },
      { step_number: 3, reactant: "对甲氧基苯乙酮", reagent: "Br₂, NaOH, △", product: "对甲氧基苯甲酸钠", reaction_type: "取代反应" },
      { step_number: 4, reactant: "对甲氧基苯甲酸钠", reagent: "HCl, H₂O", product: "对甲氧基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 5, reactant: "对甲氧基苯甲酸", reagent: "SOCl₂, △", product: "对甲氧基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对甲氧基苯甲酰氯", reagent: "苯, AlCl₃", product: "4-甲氧基二苯甲酮", reaction_type: "取代反应" },
      { step_number: 7, reactant: "4-甲氧基二苯甲酮", reagent: "HI, △", product: "4-羟基二苯甲酮", reaction_type: "取代反应" },
      { step_number: 8, reactant: "4-羟基二苯甲酮", reagent: "NH₂OH·HCl, NaOAc, △", product: "4-羟基二苯甲酮肟", reaction_type: "加成反应" }
    ]
  },
  {
    id: 82,
    title: "α-叠氮对甲氧基苯丙酮合成路线",
    desc: "苯甲醚→α-叠氮对甲氧基苯丙酮(7步)，FC酰基化→卤仿→酸化→酰氯化→Grignard加成→α-溴代→叠氮取代，经典对甲氧基α-叠氮芳酮合成",
    steps: [
      { step_number: 1, reactant: "苯甲醚", reagent: "CH₃COCl, AlCl₃", product: "对甲氧基苯乙酮", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对甲氧基苯乙酮", reagent: "Br₂, NaOH, △", product: "对甲氧基苯甲酸钠", reaction_type: "取代反应" },
      { step_number: 3, reactant: "对甲氧基苯甲酸钠", reagent: "HCl, H₂O", product: "对甲氧基苯甲酸", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "对甲氧基苯甲酸", reagent: "SOCl₂, △", product: "对甲氧基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对甲氧基苯甲酰氯", reagent: "CH₃CH₂MgBr, 无水乙醚", product: "对甲氧基苯丙酮", reaction_type: "加成反应" },
      { step_number: 6, reactant: "对甲氧基苯丙酮", reagent: "Br₂, CH₃COOH, 0°C", product: "α-溴对甲氧基苯丙酮", reaction_type: "取代反应" },
      { step_number: 7, reactant: "α-溴对甲氧基苯丙酮", reagent: "NaN₃, DMF, 0°C", product: "α-叠氮对甲氧基苯丙酮", reaction_type: "取代反应" }
    ]
  },
  {
    id: 83,
    title: "α-叠氮对溴苯乙酮合成路线",
    desc: "苯→α-叠氮对溴苯乙酮(7步)，硝化→还原→重氮化→Sandmeyer溴代→FC酰基化→α-溴代→叠氮取代，经典对溴α-叠氮芳酮合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯重氮盐", reagent: "CuBr, △", product: "溴苯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "溴苯", reagent: "CH₃COCl, AlCl₃", product: "对溴苯乙酮", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对溴苯乙酮", reagent: "Br₂, CH₃COOH, 0°C", product: "α,对二溴苯乙酮", reaction_type: "取代反应" },
      { step_number: 7, reactant: "α,对二溴苯乙酮", reagent: "NaN₃, DMF, 0°C", product: "α-叠氮对溴苯乙酮", reaction_type: "取代反应" }
    ]
  },
  {
    id: 84,
    title: "4-甲基二苯甲酮合成路线",
    desc: "甲苯→4-甲基二苯甲酮(7步)，硝化→还原→重氮化→Sandmeyer氰化→水解→酰氯化→FC酰基化，经典不对称甲基二苯甲酮合成",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "Fe, HCl, △", product: "对甲苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "对甲苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "对甲基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "对甲基苯重氮盐", reagent: "CuCN, △", product: "对甲基苯甲腈", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对甲基苯甲腈", reagent: "HCl, H₂O, △", product: "对甲基苯甲酸", reaction_type: "水解反应" },
      { step_number: 6, reactant: "对甲基苯甲酸", reagent: "SOCl₂, △", product: "对甲基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对甲基苯甲酰氯", reagent: "苯, AlCl₃", product: "4-甲基二苯甲酮", reaction_type: "取代反应" }
    ]
  },
  {
    id: 85,
    title: "二苯乙炔合成路线",
    desc: "苯→二苯乙炔(7步)，FC酰基化→还原→卤代→消去→溴代→消去→纯化，经二苯乙烯二溴化的经典二苯乙炔合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "CH₃COCl, AlCl₃", product: "苯乙酮", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯乙酮", reagent: "NaBH₄, CH₃OH", product: "1-苯乙醇", reaction_type: "还原反应" },
      { step_number: 3, reactant: "1-苯乙醇", reagent: "PBr₃, 0°C", product: "1-苯基溴乙烷", reaction_type: "取代反应" },
      { step_number: 4, reactant: "1-苯基溴乙烷", reagent: "KOH, C₂H₅OH, △", product: "苯乙烯", reaction_type: "消去反应" },
      { step_number: 5, reactant: "苯乙烯", reagent: "Br₂, CCl₄, 0°C", product: "1,2-二溴-1-苯乙烷", reaction_type: "加成反应" },
      { step_number: 6, reactant: "1,2-二溴-1-苯乙烷", reagent: "KOH, C₂H₅OH, △", product: "苯乙炔", reaction_type: "消去反应" },
      { step_number: 7, reactant: "苯乙炔", reagent: "NaNH₂, NH₃(液); (2) C₆H₅Br, CuI", product: "二苯乙炔", reaction_type: "取代反应" }
    ]
  },
  {
    id: 86,
    title: "4-溴-4′-甲基二苯甲酮肟合成路线",
    desc: "甲苯→4-溴-4′-甲基二苯甲酮肟(8步)，硝化→还原→重氮化→Sandmeyer氰化→水解→酰氯化→FC酰基化→肟化，经典不对称卤代二苯甲酮肟合成",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "Fe, HCl, △", product: "对甲苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "对甲苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "对甲基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "对甲基苯重氮盐", reagent: "CuCN, △", product: "对甲基苯甲腈", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对甲基苯甲腈", reagent: "HCl, H₂O, △", product: "对甲基苯甲酸", reaction_type: "水解反应" },
      { step_number: 6, reactant: "对甲基苯甲酸", reagent: "SOCl₂, △", product: "对甲基苯甲酰氯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对甲基苯甲酰氯", reagent: "溴苯, AlCl₃", product: "4-溴-4′-甲基二苯甲酮", reaction_type: "取代反应" },
      { step_number: 8, reactant: "4-溴-4′-甲基二苯甲酮", reagent: "NH₂OH·HCl, NaOAc, △", product: "4-溴-4′-甲基二苯甲酮肟", reaction_type: "加成反应" }
    ]
  },
  {
    id: 87,
    title: "N-苯甲酰甲基乙酰胺合成路线",
    desc: "苯→N-苯甲酰甲基乙酰胺(7步)，FC酰基化→α-溴代→Gabriel胺化→水解→乙酰化→硝化→还原，经典α-氨基酮衍生物合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "CH₃COCl, AlCl₃", product: "苯乙酮", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯乙酮", reagent: "Br₂, CH₃COOH, 0°C", product: "α-溴苯乙酮", reaction_type: "取代反应" },
      { step_number: 3, reactant: "α-溴苯乙酮", reagent: "邻苯二甲酰亚胺钾, DMF, △", product: "N-苯甲酰甲基邻苯二甲酰亚胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "N-苯甲酰甲基邻苯二甲酰亚胺", reagent: "NH₂NH₂·H₂O, C₂H₅OH, △", product: "α-氨基苯乙酮", reaction_type: "取代反应" },
      { step_number: 5, reactant: "α-氨基苯乙酮", reagent: "(CH₃CO)₂O, 吡啶", product: "N-苯甲酰甲基乙酰胺", reaction_type: "取代反应" },
      { step_number: 6, reactant: "N-苯甲酰甲基乙酰胺", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "N-(对硝基苯甲酰甲基)乙酰胺", reaction_type: "取代反应" },
      { step_number: 7, reactant: "N-(对硝基苯甲酰甲基)乙酰胺", reagent: "Fe, HCl, △", product: "N-(对氨基苯甲酰甲基)乙酰胺", reaction_type: "还原反应" }
    ]
  },
  {
    id: 88,
    title: "对苯二酚合成路线",
    desc: "苯→对苯二酚(7步)，硝化→还原→重氮化水解→亚硝化→还原→重氮化→水解",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯重氮盐", reagent: "H₂O, △", product: "苯酚", reaction_type: "取代反应" },
      { step_number: 5, reactant: "苯酚", reagent: "NaNO₂, HCl, 0-5°C", product: "对亚硝基苯酚", reaction_type: "亚硝化反应" },
      { step_number: 6, reactant: "对亚硝基苯酚", reagent: "Na₂S₂O₄, NaOH, H₂O", product: "对氨基苯酚", reaction_type: "还原反应" },
      { step_number: 7, reactant: "对氨基苯酚", reagent: "(1) NaNO₂, HCl, 0-5°C; (2) H₂O, △", product: "对苯二酚", reaction_type: "取代反应" }
    ]
  },
  {
    id: 89,
    title: "对氨基苯乙醚合成路线",
    desc: "苯→对氨基苯乙醚(7步)，硝化→还原→重氮化→水解→Williamson醚化→硝化→还原",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯重氮盐", reagent: "H₂O, △", product: "苯酚", reaction_type: "取代反应" },
      { step_number: 5, reactant: "苯酚", reagent: "C₂H₅Br, K₂CO₃, DMF", product: "苯乙醚", reaction_type: "取代反应" },
      { step_number: 6, reactant: "苯乙醚", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基苯乙醚", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对硝基苯乙醚", reagent: "Fe, HCl, △", product: "对氨基苯乙醚", reaction_type: "还原反应" }
    ]
  },
  {
    id: 90,
    title: "对氯苯酚合成路线",
    desc: "苯→对氯苯酚(7步)，硝化→还原→重氮化Sandmeyer氯代→硝化→还原→重氮化→水解",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯重氮盐", reagent: "CuCl, HCl, △", product: "氯苯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "氯苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基氯苯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对硝基氯苯", reagent: "Fe, HCl, △", product: "对氯苯胺", reaction_type: "还原反应" },
      { step_number: 7, reactant: "对氯苯胺", reagent: "(1) NaNO₂, HCl, 0-5°C; (2) H₂O, △", product: "对氯苯酚", reaction_type: "取代反应" }
    ]
  },
  {
    id: 91,
    title: "邻甲基水杨酸合成路线",
    desc: "甲苯→邻甲基水杨酸(7步)，硝化→还原→重氮化→水解→成盐→Kolbe-Schmitt羧化→酸化",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "邻硝基甲苯(主)和对硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "邻硝基甲苯", reagent: "Fe, HCl, △", product: "邻甲苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "邻甲苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "邻甲基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "邻甲基苯重氮盐", reagent: "H₂O, △", product: "邻甲苯酚", reaction_type: "取代反应" },
      { step_number: 5, reactant: "邻甲苯酚", reagent: "NaOH, H₂O", product: "邻甲苯酚钠", reaction_type: "酸碱反应" },
      { step_number: 6, reactant: "邻甲苯酚钠", reagent: "CO₂, 加压, 120°C", product: "邻甲基水杨酸钠", reaction_type: "取代反应" },
      { step_number: 7, reactant: "邻甲基水杨酸钠", reagent: "HCl, H₂O", product: "邻甲基水杨酸", reaction_type: "酸碱反应" }
    ]
  },
  {
    id: 92,
    title: "4-溴-1-萘酚合成路线",
    desc: "萘→4-溴-1-萘酚(7步)，硝化→还原→乙酰化→溴代→水解脱保护→重氮化→水解",
    steps: [
      { step_number: 1, reactant: "萘", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "1-硝基萘", reaction_type: "取代反应" },
      { step_number: 2, reactant: "1-硝基萘", reagent: "Fe, HCl, △", product: "α-萘胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "α-萘胺", reagent: "(CH₃CO)₂O, 吡啶", product: "α-乙酰氨基萘", reaction_type: "取代反应" },
      { step_number: 4, reactant: "α-乙酰氨基萘", reagent: "Br₂, CH₃COOH", product: "1-乙酰氨基-4-溴萘", reaction_type: "取代反应" },
      { step_number: 5, reactant: "1-乙酰氨基-4-溴萘", reagent: "NaOH, H₂O, △", product: "1-氨基-4-溴萘", reaction_type: "水解反应" },
      { step_number: 6, reactant: "1-氨基-4-溴萘", reagent: "NaNO₂, HCl, 0-5°C", product: "4-溴-1-萘重氮盐", reaction_type: "取代反应" },
      { step_number: 7, reactant: "4-溴-1-萘重氮盐", reagent: "H₂O, △", product: "4-溴-1-萘酚", reaction_type: "取代反应" }
    ]
  },
  {
    id: 93,
    title: "对溴苯酚合成路线",
    desc: "苯→对溴苯酚(7步)，硝化→还原→重氮化Sandmeyer溴代→硝化→还原→重氮化→水解",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯重氮盐", reagent: "CuBr, △", product: "溴苯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "溴苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基溴苯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对硝基溴苯", reagent: "Fe, HCl, △", product: "对溴苯胺", reaction_type: "还原反应" },
      { step_number: 7, reactant: "对溴苯胺", reagent: "(1) NaNO₂, HCl, 0-5°C; (2) H₂O, △", product: "对溴苯酚", reaction_type: "取代反应" }
    ]
  },
  {
    id: 94,
    title: "2,4-二溴苯酚合成路线",
    desc: "苯→2,4-二溴苯酚(7步)，硝化→还原→乙酰化→对位溴代→邻位溴代→水解脱保护→重氮化水解",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "Br₂, CH₃COOH", product: "对溴乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对溴乙酰苯胺", reagent: "Br₂, FeBr₃", product: "2,4-二溴乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 6, reactant: "2,4-二溴乙酰苯胺", reagent: "NaOH, H₂O, △", product: "2,4-二溴苯胺", reaction_type: "水解反应" },
      { step_number: 7, reactant: "2,4-二溴苯胺", reagent: "(1) NaNO₂, HCl, 0-5°C; (2) H₂O, △", product: "2,4-二溴苯酚", reaction_type: "取代反应" }
    ]
  },
  {
    id: 95,
    title: "间苯二酚合成路线",
    desc: "苯→间苯二酚(8步)，磺化→硝化→还原→重氮化→水解→再磺化→碱熔→酸化",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓H₂SO₄, △", product: "苯磺酸", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯磺酸", reagent: "浓HNO₃, 浓H₂SO₄", product: "间硝基苯磺酸", reaction_type: "取代反应" },
      { step_number: 3, reactant: "间硝基苯磺酸", reagent: "Fe, HCl, △", product: "间氨基苯磺酸", reaction_type: "还原反应" },
      { step_number: 4, reactant: "间氨基苯磺酸", reagent: "NaNO₂, HCl, 0-5°C", product: "间磺酸基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 5, reactant: "间磺酸基苯重氮盐", reagent: "H₂O, △", product: "间羟基苯磺酸", reaction_type: "取代反应" },
      { step_number: 6, reactant: "间羟基苯磺酸", reagent: "发烟H₂SO₄, △", product: "间羟基间苯二磺酸", reaction_type: "取代反应" },
      { step_number: 7, reactant: "间羟基间苯二磺酸", reagent: "NaOH, 熔融, 300°C", product: "间苯二酚钠", reaction_type: "取代反应" },
      { step_number: 8, reactant: "间苯二酚钠", reagent: "HCl, H₂O", product: "间苯二酚", reaction_type: "酸碱反应" }
    ]
  },
  {
    id: 96,
    title: "1,4-萘醌合成路线",
    desc: "萘→1,4-萘醌(8步)，硝化→还原→乙酰化→磺化→碱熔→水解脱保护→重氮化水解→氧化",
    steps: [
      { step_number: 1, reactant: "萘", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "1-硝基萘", reaction_type: "取代反应" },
      { step_number: 2, reactant: "1-硝基萘", reagent: "Fe, HCl, △", product: "α-萘胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "α-萘胺", reagent: "(CH₃CO)₂O, 吡啶", product: "α-乙酰氨基萘", reaction_type: "取代反应" },
      { step_number: 4, reactant: "α-乙酰氨基萘", reagent: "浓H₂SO₄, 60°C", product: "1-乙酰氨基-4-萘磺酸", reaction_type: "取代反应" },
      { step_number: 5, reactant: "1-乙酰氨基-4-萘磺酸", reagent: "NaOH, 熔融, 300°C", product: "1-乙酰氨基-4-萘酚钠", reaction_type: "取代反应" },
      { step_number: 6, reactant: "1-乙酰氨基-4-萘酚钠", reagent: "HCl, H₂O, △", product: "1-氨基-4-萘酚", reaction_type: "水解反应" },
      { step_number: 7, reactant: "1-氨基-4-萘酚", reagent: "(1) NaNO₂, HCl, 0-5°C; (2) H₂O, △", product: "1,4-萘二酚", reaction_type: "取代反应" },
      { step_number: 8, reactant: "1,4-萘二酚", reagent: "Na₂Cr₂O₇, H₂SO₄, 0°C", product: "1,4-萘醌", reaction_type: "氧化反应" }
    ]
  },
  {
    id: 97,
    title: "对碘苯酚合成路线",
    desc: "苯→对碘苯酚(8步)，硝化→还原→重氮化→Sandmeyer碘代→硝化→还原→重氮化→水解",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯重氮盐", reagent: "KI, △", product: "碘苯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "碘苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基碘苯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "对硝基碘苯", reagent: "Fe, HCl, △", product: "对碘苯胺", reaction_type: "还原反应" },
      { step_number: 7, reactant: "对碘苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "对碘苯重氮盐", reaction_type: "取代反应" },
      { step_number: 8, reactant: "对碘苯重氮盐", reagent: "H₂O, △", product: "对碘苯酚", reaction_type: "取代反应" }
    ]
  },
  {
    id: 98,
    title: "邻氯硝基苯合成路线",
    desc: "苯→邻氯硝基苯(8步)，硝化→还原→乙酰化→对位氯代→邻位硝化→水解脱保护→重氮化→脱氨基还原",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "Cl₂, FeCl₃, 低温", product: "对氯乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对氯乙酰苯胺", reagent: "浓HNO₃, 浓H₂SO₄", product: "2-硝基-4-氯乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 6, reactant: "2-硝基-4-氯乙酰苯胺", reagent: "NaOH, H₂O, △", product: "2-硝基-4-氯苯胺", reaction_type: "水解反应" },
      { step_number: 7, reactant: "2-硝基-4-氯苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "2-硝基-4-氯苯重氮盐", reaction_type: "取代反应" },
      { step_number: 8, reactant: "2-硝基-4-氯苯重氮盐", reagent: "H₃PO₂, H₂O", product: "邻氯硝基苯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 99,
    title: "间溴苯甲酸合成路线",
    desc: "甲苯→间溴苯甲酸(8步)，硝化→还原→乙酰化→溴代→水解脱保护→重氮化→脱氨基还原→氧化",
    steps: [
      { step_number: 1, reactant: "甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "对硝基甲苯(主)和邻硝基甲苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对硝基甲苯", reagent: "Fe, HCl, △", product: "对甲苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "对甲苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "对甲基乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "对甲基乙酰苯胺", reagent: "Br₂, CH₃COOH", product: "2-溴-4-甲基乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 5, reactant: "2-溴-4-甲基乙酰苯胺", reagent: "NaOH, H₂O, △", product: "2-溴-4-甲基苯胺", reaction_type: "水解反应" },
      { step_number: 6, reactant: "2-溴-4-甲基苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "2-溴-4-甲基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 7, reactant: "2-溴-4-甲基苯重氮盐", reagent: "H₃PO₂, H₂O", product: "间溴甲苯", reaction_type: "取代反应" },
      { step_number: 8, reactant: "间溴甲苯", reagent: "KMnO₄, H₂O, △", product: "间溴苯甲酸", reaction_type: "氧化反应" }
    ]
  },
  {
    id: 100,
    title: "5-硝基水杨酸合成路线",
    desc: "苯→5-硝基水杨酸(8步)，硝化→还原→重氮化→水解→成盐→Kolbe-Schmitt羧化→酸化→硝化",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "苯重氮盐", reaction_type: "取代反应" },
      { step_number: 4, reactant: "苯重氮盐", reagent: "H₂O, △", product: "苯酚", reaction_type: "取代反应" },
      { step_number: 5, reactant: "苯酚", reagent: "NaOH, H₂O", product: "苯酚钠", reaction_type: "酸碱反应" },
      { step_number: 6, reactant: "苯酚钠", reagent: "CO₂, 加压, 120°C", product: "水杨酸钠", reaction_type: "取代反应" },
      { step_number: 7, reactant: "水杨酸钠", reagent: "HCl, H₂O", product: "水杨酸", reaction_type: "酸碱反应" },
      { step_number: 8, reactant: "水杨酸", reagent: "浓HNO₃, 浓H₂SO₄", product: "5-硝基水杨酸", reaction_type: "取代反应" }
    ]
  },
  {
    id: 101,
    title: "2,4-二甲基苯酚合成路线",
    desc: "间二甲苯→2,4-二甲基苯酚(8步)，硝化→还原→乙酰化→磺化→碱熔→酸化→重氮化→脱氨基还原",
    steps: [
      { step_number: 1, reactant: "间二甲苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "2,4-二甲基硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "2,4-二甲基硝基苯", reagent: "Fe, HCl, △", product: "2,4-二甲基苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "2,4-二甲基苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "2,4-二甲基乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "2,4-二甲基乙酰苯胺", reagent: "浓H₂SO₄, 60°C", product: "2,4-二甲基-6-乙酰氨基苯磺酸", reaction_type: "取代反应" },
      { step_number: 5, reactant: "2,4-二甲基-6-乙酰氨基苯磺酸", reagent: "NaOH, 熔融, 300°C", product: "2,4-二甲基-6-氨基苯酚钠", reaction_type: "取代反应" },
      { step_number: 6, reactant: "2,4-二甲基-6-氨基苯酚钠", reagent: "HCl, H₂O", product: "2,4-二甲基-6-氨基苯酚", reaction_type: "酸碱反应" },
      { step_number: 7, reactant: "2,4-二甲基-6-氨基苯酚", reagent: "NaNO₂, HCl, 0-5°C", product: "2,4-二甲基-6-羟基苯重氮盐", reaction_type: "取代反应" },
      { step_number: 8, reactant: "2,4-二甲基-6-羟基苯重氮盐", reagent: "H₃PO₂, H₂O", product: "2,4-二甲基苯酚", reaction_type: "取代反应" }
    ]
  },
  {
    id: 102,
    title: "2-溴-1,4-二氯苯合成路线",
    desc: "苯→2-溴-1,4-二氯苯(8步)，硝化→还原→乙酰化→对位氯代→邻位溴代→水解脱保护→重氮化→Sandmeyer氯代，经典多卤代芳烃合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "Cl₂, FeCl₃, 低温", product: "对氯乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对氯乙酰苯胺", reagent: "Br₂, FeBr₃", product: "2-溴-4-氯乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 6, reactant: "2-溴-4-氯乙酰苯胺", reagent: "NaOH, H₂O, △", product: "2-溴-4-氯苯胺", reaction_type: "水解反应" },
      { step_number: 7, reactant: "2-溴-4-氯苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "2-溴-4-氯苯重氮盐", reaction_type: "取代反应" },
      { step_number: 8, reactant: "2-溴-4-氯苯重氮盐", reagent: "CuCl, HCl, △", product: "2-溴-1,4-二氯苯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 103,
    title: "对羟基苯乙酮肟合成路线",
    desc: "苯→对羟基苯乙酮肟(7步)，硝化→还原→乙酰化保护→Friedel-Crafts酰化→脱保护→重氮化水解→肟化，经典对位羟基芳酮肟合成",
    steps: [
      { step_number: 1, reactant: "苯", reagent: "浓HNO₃, 浓H₂SO₄", product: "硝基苯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "硝基苯", reagent: "Fe, HCl, △", product: "苯胺", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯胺", reagent: "(CH₃CO)₂O, △", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "乙酰苯胺", reagent: "CH₃COCl, AlCl₃", product: "对乙酰氨基苯乙酮", reaction_type: "取代反应" },
      { step_number: 5, reactant: "对乙酰氨基苯乙酮", reagent: "NaOH, H₂O, △", product: "对氨基苯乙酮", reaction_type: "水解反应" },
      { step_number: 6, reactant: "对氨基苯乙酮", reagent: "NaNO₂, HCl, 0-5°C; (2) H₂O, △", product: "对羟基苯乙酮", reaction_type: "取代反应" },
      { step_number: 7, reactant: "对羟基苯乙酮", reagent: "NH₂OH·HCl, NaOAc, △", product: "对羟基苯乙酮肟", reaction_type: "加成反应" }
    ]
  },
  {
    id: 104,
    title: "丁酸合成路线",
    desc: "乙酸→丁酸(7步)，酯化→Claisen缩合→成盐→烷基化→酸式水解→酯化→水解，经乙酰乙酸乙酯法合成丁酸",
    steps: [
      { step_number: 1, reactant: "乙酸", reagent: "C₂H₅OH, 浓H₂SO₄, △", product: "乙酸乙酯", reaction_type: "酯化反应" },
      { step_number: 2, reactant: "乙酸乙酯", reagent: "NaOEt, C₂H₅OH", product: "乙酰乙酸乙酯", reaction_type: "缩合反应" },
      { step_number: 3, reactant: "乙酰乙酸乙酯", reagent: "NaOEt, C₂H₅OH", product: "乙酰乙酸乙酯钠盐", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "乙酰乙酸乙酯钠盐", reagent: "C₂H₅Br, △", product: "α-乙基乙酰乙酸乙酯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "α-乙基乙酰乙酸乙酯", reagent: "浓NaOH, H₂O, △", product: "丁酸钠", reaction_type: "水解反应" },
      { step_number: 6, reactant: "丁酸钠", reagent: "(1) HCl, H₂O; (2) C₂H₅OH, 浓H₂SO₄, △", product: "丁酸乙酯", reaction_type: "酯化反应" },
      { step_number: 7, reactant: "丁酸乙酯", reagent: "NaOH, H₂O, △; (2) HCl", product: "丁酸", reaction_type: "水解反应" }
    ]
  },
  {
    id: 105,
    title: "正丁醇合成路线",
    desc: "丙酸→正丁醇(7步)，酰氯化→酯化→还原→卤代→腈化→水解→还原，经腈水解法增碳合成正丁醇",
    steps: [
      { step_number: 1, reactant: "丙酸", reagent: "SOCl₂, △", product: "丙酰氯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "丙酰氯", reagent: "C₂H₅OH, 吡啶", product: "丙酸乙酯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "丙酸乙酯", reagent: "LiAlH₄, 无水乙醚", product: "正丙醇", reaction_type: "还原反应" },
      { step_number: 4, reactant: "正丙醇", reagent: "PBr₃, 0°C", product: "1-溴丙烷", reaction_type: "取代反应" },
      { step_number: 5, reactant: "1-溴丙烷", reagent: "KCN, C₂H₅OH, △", product: "丁腈", reaction_type: "取代反应" },
      { step_number: 6, reactant: "丁腈", reagent: "H₂O, H⁺, △", product: "丁酸", reaction_type: "水解反应" },
      { step_number: 7, reactant: "丁酸", reagent: "LiAlH₄, 无水乙醚", product: "正丁醇", reaction_type: "还原反应" }
    ]
  },
  {
    id: 106,
    title: "2-乙基戊酸合成路线",
    desc: "丙二酸二乙酯→2-乙基戊酸(7步)，成盐→烷基化→成盐→烷基化→水解→酸化→脱羧，经丙二酸酯双烷基化法合成",
    steps: [
      { step_number: 1, reactant: "丙二酸二乙酯", reagent: "NaOEt, C₂H₅OH", product: "丙二酸二乙酯钠盐", reaction_type: "酸碱反应" },
      { step_number: 2, reactant: "丙二酸二乙酯钠盐", reagent: "CH₃CH₂CH₂Br, △", product: "丙基丙二酸二乙酯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "丙基丙二酸二乙酯", reagent: "NaOEt, C₂H₅OH", product: "丙基丙二酸二乙酯钠盐", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "丙基丙二酸二乙酯钠盐", reagent: "CH₃CH₂Br, △", product: "乙基丙基丙二酸二乙酯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "乙基丙基丙二酸二乙酯", reagent: "NaOH, H₂O, △", product: "乙基丙基丙二酸钠", reaction_type: "水解反应" },
      { step_number: 6, reactant: "乙基丙基丙二酸钠", reagent: "HCl, H₂O", product: "乙基丙基丙二酸", reaction_type: "酸碱反应" },
      { step_number: 7, reactant: "乙基丙基丙二酸", reagent: "△, 160°C", product: "2-乙基戊酸", reaction_type: "消去反应" }
    ]
  },
  {
    id: 107,
    title: "己酸乙酯合成路线",
    desc: "丙二酸二乙酯→己酸乙酯(7步)，成盐→烷基化→水解→酸化→脱羧→酰氯化→酯化，经丙二酸酯法合成",
    steps: [
      { step_number: 1, reactant: "丙二酸二乙酯", reagent: "NaOEt, C₂H₅OH", product: "丙二酸二乙酯钠盐", reaction_type: "酸碱反应" },
      { step_number: 2, reactant: "丙二酸二乙酯钠盐", reagent: "CH₃(CH₂)₃Br, △", product: "正丁基丙二酸二乙酯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "正丁基丙二酸二乙酯", reagent: "NaOH, H₂O, △", product: "正丁基丙二酸钠", reaction_type: "水解反应" },
      { step_number: 4, reactant: "正丁基丙二酸钠", reagent: "HCl, H₂O", product: "正丁基丙二酸", reaction_type: "酸碱反应" },
      { step_number: 5, reactant: "正丁基丙二酸", reagent: "△, 160°C", product: "己酸", reaction_type: "消去反应" },
      { step_number: 6, reactant: "己酸", reagent: "SOCl₂, △", product: "己酰氯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "己酰氯", reagent: "C₂H₅OH, 吡啶", product: "己酸乙酯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 108,
    title: "2-甲基丁酸乙酯合成路线",
    desc: "丙二酸二乙酯→2-甲基丁酸乙酯(7步)，成盐→烷基化→水解→酸化→脱羧→酰氯化→酯化，经丙二酸酯法合成",
    steps: [
      { step_number: 1, reactant: "丙二酸二乙酯", reagent: "NaOEt, C₂H₅OH", product: "丙二酸二乙酯钠盐", reaction_type: "酸碱反应" },
      { step_number: 2, reactant: "丙二酸二乙酯钠盐", reagent: "CH₃CH₂Br, △", product: "乙基丙二酸二乙酯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "乙基丙二酸二乙酯", reagent: "NaOH, H₂O, △", product: "乙基丙二酸钠", reaction_type: "水解反应" },
      { step_number: 4, reactant: "乙基丙二酸钠", reagent: "HCl, H₂O", product: "乙基丙二酸", reaction_type: "酸碱反应" },
      { step_number: 5, reactant: "乙基丙二酸", reagent: "△, 160°C", product: "2-甲基丁酸", reaction_type: "消去反应" },
      { step_number: 6, reactant: "2-甲基丁酸", reagent: "SOCl₂, △", product: "2-甲基丁酰氯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "2-甲基丁酰氯", reagent: "C₂H₅OH, 吡啶", product: "2-甲基丁酸乙酯", reaction_type: "取代反应" }
    ]
  },
  {
    id: 109,
    title: "N-乙基丁胺合成路线",
    desc: "正丁醇→N-乙基丁胺(7步)，卤代→腈化→水解→酰氯化→酰胺化→Hofmann降解→还原胺化，经Hofmann重排合成",
    steps: [
      { step_number: 1, reactant: "正丁醇", reagent: "PBr₃, 0°C", product: "1-溴丁烷", reaction_type: "取代反应" },
      { step_number: 2, reactant: "1-溴丁烷", reagent: "KCN, C₂H₅OH, △", product: "戊腈", reaction_type: "取代反应" },
      { step_number: 3, reactant: "戊腈", reagent: "H₂O, H⁺, △", product: "戊酸", reaction_type: "水解反应" },
      { step_number: 4, reactant: "戊酸", reagent: "SOCl₂, △", product: "戊酰氯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "戊酰氯", reagent: "NH₃, 0°C", product: "戊酰胺", reaction_type: "取代反应" },
      { step_number: 6, reactant: "戊酰胺", reagent: "Br₂, NaOH, H₂O", product: "正丁胺", reaction_type: "重排反应" },
      { step_number: 7, reactant: "正丁胺", reagent: "CH₃CHO, NaBH₄, CH₃OH", product: "N-乙基丁胺", reaction_type: "还原胺化" }
    ]
  },
  {
    id: 110,
    title: "丁酸乙酯合成路线",
    desc: "乙酸→丁酸乙酯(7步)，酯化→Claisen缩合→成盐→烷基化→酸式水解→酸化→酯化，经乙酰乙酸乙酯法合成",
    steps: [
      { step_number: 1, reactant: "乙酸", reagent: "C₂H₅OH, 浓H₂SO₄, △", product: "乙酸乙酯", reaction_type: "酯化反应" },
      { step_number: 2, reactant: "乙酸乙酯", reagent: "NaOEt, C₂H₅OH", product: "乙酰乙酸乙酯", reaction_type: "缩合反应" },
      { step_number: 3, reactant: "乙酰乙酸乙酯", reagent: "NaOEt, C₂H₅OH", product: "乙酰乙酸乙酯钠盐", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "乙酰乙酸乙酯钠盐", reagent: "C₂H₅Br, △", product: "α-乙基乙酰乙酸乙酯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "α-乙基乙酰乙酸乙酯", reagent: "浓NaOH, H₂O, △", product: "丁酸钠", reaction_type: "水解反应" },
      { step_number: 6, reactant: "丁酸钠", reagent: "HCl, H₂O", product: "丁酸", reaction_type: "酸碱反应" },
      { step_number: 7, reactant: "丁酸", reagent: "C₂H₅OH, 浓H₂SO₄, △", product: "丁酸乙酯", reaction_type: "酯化反应" }
    ]
  },
  {
    id: 111,
    title: "3-己酮合成路线",
    desc: "乙酰乙酸乙酯→3-己酮(8步)，成盐→烷基化→酮式水解→还原→卤代→Grignard试剂→醛加成→氧化，经Grignard增碳合成",
    steps: [
      { step_number: 1, reactant: "乙酰乙酸乙酯", reagent: "NaOEt, C₂H₅OH", product: "乙酰乙酸乙酯钠盐", reaction_type: "酸碱反应" },
      { step_number: 2, reactant: "乙酰乙酸乙酯钠盐", reagent: "CH₃CH₂Br, △", product: "α-乙基乙酰乙酸乙酯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "α-乙基乙酰乙酸乙酯", reagent: "稀NaOH, H₂O, △", product: "2-戊酮", reaction_type: "水解反应" },
      { step_number: 4, reactant: "2-戊酮", reagent: "NaBH₄, CH₃OH", product: "2-戊醇", reaction_type: "还原反应" },
      { step_number: 5, reactant: "2-戊醇", reagent: "PBr₃, 0°C", product: "2-溴戊烷", reaction_type: "取代反应" },
      { step_number: 6, reactant: "2-溴戊烷", reagent: "Mg, 无水乙醚", product: "2-戊基溴化镁", reaction_type: "加成反应" },
      { step_number: 7, reactant: "2-戊基溴化镁", reagent: "CH₃CHO, 无水乙醚; (2) H₂O", product: "3-己醇", reaction_type: "加成反应" },
      { step_number: 8, reactant: "3-己醇", reagent: "PCC, CH₂Cl₂", product: "3-己酮", reaction_type: "氧化反应" }
    ]
  },
  {
    id: 112,
    title: "N-乙基戊胺合成路线",
    desc: "正戊醇→N-乙基戊胺(8步)，卤代→腈化→水解→酰氯化→酰胺化→Hofmann降解→乙酰化→还原，经Hofmann重排合成",
    steps: [
      { step_number: 1, reactant: "正戊醇", reagent: "PBr₃, 0°C", product: "1-溴戊烷", reaction_type: "取代反应" },
      { step_number: 2, reactant: "1-溴戊烷", reagent: "KCN, C₂H₅OH, △", product: "己腈", reaction_type: "取代反应" },
      { step_number: 3, reactant: "己腈", reagent: "H₂O, H⁺, △", product: "己酸", reaction_type: "水解反应" },
      { step_number: 4, reactant: "己酸", reagent: "SOCl₂, △", product: "己酰氯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "己酰氯", reagent: "NH₃, 0°C", product: "己酰胺", reaction_type: "取代反应" },
      { step_number: 6, reactant: "己酰胺", reagent: "Br₂, NaOH, H₂O", product: "正戊胺", reaction_type: "重排反应" },
      { step_number: 7, reactant: "正戊胺", reagent: "(CH₃CO)₂O, 吡啶", product: "N-乙酰基正戊胺", reaction_type: "取代反应" },
      { step_number: 8, reactant: "N-乙酰基正戊胺", reagent: "LiAlH₄, 无水乙醚", product: "N-乙基戊胺", reaction_type: "还原反应" }
    ]
  },
  {
    id: 113,
    title: "2-乙基戊醇合成路线",
    desc: "丙二酸二乙酯→2-乙基戊醇(8步)，成盐→烷基化→成盐→烷基化→水解→酸化→脱羧→还原，经丙二酸酯双烷基化法合成",
    steps: [
      { step_number: 1, reactant: "丙二酸二乙酯", reagent: "NaOEt, C₂H₅OH", product: "丙二酸二乙酯钠盐", reaction_type: "酸碱反应" },
      { step_number: 2, reactant: "丙二酸二乙酯钠盐", reagent: "CH₃CH₂CH₂Br, △", product: "丙基丙二酸二乙酯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "丙基丙二酸二乙酯", reagent: "NaOEt, C₂H₅OH", product: "丙基丙二酸二乙酯钠盐", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "丙基丙二酸二乙酯钠盐", reagent: "CH₃CH₂Br, △", product: "乙基丙基丙二酸二乙酯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "乙基丙基丙二酸二乙酯", reagent: "NaOH, H₂O, △", product: "乙基丙基丙二酸钠", reaction_type: "水解反应" },
      { step_number: 6, reactant: "乙基丙基丙二酸钠", reagent: "HCl, H₂O", product: "乙基丙基丙二酸", reaction_type: "酸碱反应" },
      { step_number: 7, reactant: "乙基丙基丙二酸", reagent: "△, 160°C", product: "2-乙基戊酸", reaction_type: "消去反应" },
      { step_number: 8, reactant: "2-乙基戊酸", reagent: "LiAlH₄, 无水乙醚", product: "2-乙基戊醇", reaction_type: "还原反应" }
    ]
  },
  {
    id: 114,
    title: "1-庚醇合成路线",
    desc: "丙二酸二乙酯→1-庚醇(8步)，成盐→烷基化→水解→酸化→脱羧→酰氯化→酯化→还原，经丙二酸酯法合成",
    steps: [
      { step_number: 1, reactant: "丙二酸二乙酯", reagent: "NaOEt, C₂H₅OH", product: "丙二酸二乙酯钠盐", reaction_type: "酸碱反应" },
      { step_number: 2, reactant: "丙二酸二乙酯钠盐", reagent: "CH₃(CH₂)₄Br, △", product: "正戊基丙二酸二乙酯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "正戊基丙二酸二乙酯", reagent: "NaOH, H₂O, △", product: "正戊基丙二酸钠", reaction_type: "水解反应" },
      { step_number: 4, reactant: "正戊基丙二酸钠", reagent: "HCl, H₂O", product: "正戊基丙二酸", reaction_type: "酸碱反应" },
      { step_number: 5, reactant: "正戊基丙二酸", reagent: "△, 160°C", product: "庚酸", reaction_type: "消去反应" },
      { step_number: 6, reactant: "庚酸", reagent: "SOCl₂, △", product: "庚酰氯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "庚酰氯", reagent: "C₂H₅OH, 吡啶", product: "庚酸乙酯", reaction_type: "取代反应" },
      { step_number: 8, reactant: "庚酸乙酯", reagent: "LiAlH₄, 无水乙醚", product: "1-庚醇", reaction_type: "还原反应" }
    ]
  },
  {
    id: 115,
    title: "N,N-二乙基环己胺合成路线",
    desc: "环己醇→N,N-二乙基环己胺(8步)，卤代→Gabriel合成→肼解→乙酰化→还原→乙酰化→还原→季铵化，经Gabriel法合成",
    steps: [
      { step_number: 1, reactant: "环己醇", reagent: "PBr₃, 0°C", product: "溴代环己烷", reaction_type: "取代反应" },
      { step_number: 2, reactant: "邻苯二甲酰亚胺", reagent: "KOH, C₂H₅OH", product: "邻苯二甲酰亚胺钾", reaction_type: "酸碱反应" },
      { step_number: 3, reactant: "邻苯二甲酰亚胺钾", reagent: "溴代环己烷, DMF, △", product: "N-环己基邻苯二甲酰亚胺", reaction_type: "取代反应" },
      { step_number: 4, reactant: "N-环己基邻苯二甲酰亚胺", reagent: "H₂NNH₂, C₂H₅OH, △", product: "环己胺", reaction_type: "取代反应" },
      { step_number: 5, reactant: "环己胺", reagent: "CH₃COCl, 吡啶", product: "N-乙酰基环己胺", reaction_type: "取代反应" },
      { step_number: 6, reactant: "N-乙酰基环己胺", reagent: "LiAlH₄, 无水乙醚", product: "N-乙基环己胺", reaction_type: "还原反应" },
      { step_number: 7, reactant: "N-乙基环己胺", reagent: "CH₃COCl, 吡啶", product: "N-乙酰基-N-乙基环己胺", reaction_type: "取代反应" },
      { step_number: 8, reactant: "N-乙酰基-N-乙基环己胺", reagent: "LiAlH₄, 无水乙醚", product: "N,N-二乙基环己胺", reaction_type: "还原反应" }
    ]
  },
  {
    id: 116,
    title: "环戊酮合成路线",
    desc: "1,4-丁二醇→环戊酮(8步)，卤代→腈化→水解→酯化→Dieckmann缩合→水解→酸化→脱羧，经Dieckmann环化合成",
    steps: [
      { step_number: 1, reactant: "1,4-丁二醇", reagent: "PBr₃, 0°C", product: "1,4-二溴丁烷", reaction_type: "取代反应" },
      { step_number: 2, reactant: "1,4-二溴丁烷", reagent: "KCN, C₂H₅OH, △", product: "己二腈", reaction_type: "取代反应" },
      { step_number: 3, reactant: "己二腈", reagent: "NaOH, H₂O, △; (2) HCl", product: "己二酸", reaction_type: "水解反应" },
      { step_number: 4, reactant: "己二酸", reagent: "C₂H₅OH, 浓H₂SO₄, △", product: "己二酸二乙酯", reaction_type: "酯化反应" },
      { step_number: 5, reactant: "己二酸二乙酯", reagent: "NaOEt, C₂H₅OH, △", product: "2-乙氧羰基环戊酮", reaction_type: "缩合反应" },
      { step_number: 6, reactant: "2-乙氧羰基环戊酮", reagent: "NaOH, H₂O, △", product: "2-羧基环戊酮钠", reaction_type: "水解反应" },
      { step_number: 7, reactant: "2-羧基环戊酮钠", reagent: "HCl, H₂O", product: "2-羧基环戊酮", reaction_type: "酸碱反应" },
      { step_number: 8, reactant: "2-羧基环戊酮", reagent: "△, 160°C", product: "环戊酮", reaction_type: "消去反应" }
    ]
  },
  {
    id: 117,
    title: "6-乙酰氨基己酸合成路线",
    desc: "环己醇→6-乙酰氨基己酸(8步)，氧化→肟化→Beckmann重排→水解→酯化→乙酰化→水解→酸化，经Beckmann重排合成",
    steps: [
      { step_number: 1, reactant: "环己醇", reagent: "PCC, CH₂Cl₂", product: "环己酮", reaction_type: "氧化反应" },
      { step_number: 2, reactant: "环己酮", reagent: "NH₂OH·HCl, NaOAc, H₂O", product: "环己酮肟", reaction_type: "加成反应" },
      { step_number: 3, reactant: "环己酮肟", reagent: "浓H₂SO₄, 100°C", product: "己内酰胺", reaction_type: "重排反应" },
      { step_number: 4, reactant: "己内酰胺", reagent: "HCl, H₂O, △", product: "6-氨基己酸", reaction_type: "水解反应" },
      { step_number: 5, reactant: "6-氨基己酸", reagent: "C₂H₅OH, 浓H₂SO₄, △", product: "6-氨基己酸乙酯", reaction_type: "酯化反应" },
      { step_number: 6, reactant: "6-氨基己酸乙酯", reagent: "(CH₃CO)₂O, 吡啶", product: "6-乙酰氨基己酸乙酯", reaction_type: "取代反应" },
      { step_number: 7, reactant: "6-乙酰氨基己酸乙酯", reagent: "NaOH, H₂O, △", product: "6-乙酰氨基己酸钠", reaction_type: "水解反应" },
      { step_number: 8, reactant: "6-乙酰氨基己酸钠", reagent: "HCl, H₂O", product: "6-乙酰氨基己酸", reaction_type: "酸碱反应" }
    ]
  },
  {
    id: 118,
    title: "3-乙酰氨基-2-苯基吲哚合成路线",
    desc: "苯胺→3-乙酰氨基-2-苯基吲哚(7步)，重氮化→还原→苯腙化→Fischer吲哚合成→硝化→还原→乙酰化，经典含氮杂环合成",
    steps: [
      { step_number: 1, reactant: "苯胺", reagent: "NaNO₂, HCl, 0-5°C", product: "苯重氮盐", reaction_type: "取代反应" },
      { step_number: 2, reactant: "苯重氮盐", reagent: "SnCl₂, HCl, 0°C", product: "苯肼", reaction_type: "还原反应" },
      { step_number: 3, reactant: "苯肼", reagent: "苯乙酮, H⁺, C₂H₅OH", product: "苯乙酮苯腙", reaction_type: "加成反应" },
      { step_number: 4, reactant: "苯乙酮苯腙", reagent: "ZnCl₂, △", product: "2-苯基吲哚", reaction_type: "重排反应" },
      { step_number: 5, reactant: "2-苯基吲哚", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "3-硝基-2-苯基吲哚", reaction_type: "取代反应" },
      { step_number: 6, reactant: "3-硝基-2-苯基吲哚", reagent: "Fe, HCl, △", product: "3-氨基-2-苯基吲哚", reaction_type: "还原反应" },
      { step_number: 7, reactant: "3-氨基-2-苯基吲哚", reagent: "(CH₃CO)₂O, 吡啶", product: "3-乙酰氨基-2-苯基吲哚", reaction_type: "取代反应" }
    ]
  },
  {
    id: 119,
    title: "2-呋喃乙酸乙酯合成路线",
    desc: "呋喃→2-呋喃乙酸乙酯(7步)，Friedel-Crafts→还原→卤代→腈化→水解→酸化→酯化，经典含氧杂环衍生物合成",
    steps: [
      { step_number: 1, reactant: "呋喃", reagent: "(CH₃CO)₂O, BF₃, 0°C", product: "2-乙酰基呋喃", reaction_type: "取代反应" },
      { step_number: 2, reactant: "2-乙酰基呋喃", reagent: "NaBH₄, CH₃OH", product: "1-(2-呋喃基)乙醇", reaction_type: "还原反应" },
      { step_number: 3, reactant: "1-(2-呋喃基)乙醇", reagent: "PBr₃, 0°C", product: "1-(2-呋喃基)溴乙烷", reaction_type: "取代反应" },
      { step_number: 4, reactant: "1-(2-呋喃基)溴乙烷", reagent: "KCN, C₂H₅OH, △", product: "2-呋喃乙腈", reaction_type: "取代反应" },
      { step_number: 5, reactant: "2-呋喃乙腈", reagent: "NaOH, H₂O, △", product: "2-呋喃乙酸钠", reaction_type: "水解反应" },
      { step_number: 6, reactant: "2-呋喃乙酸钠", reagent: "HCl, H₂O", product: "2-呋喃乙酸", reaction_type: "酸碱反应" },
      { step_number: 7, reactant: "2-呋喃乙酸", reagent: "C₂H₅OH, 浓H₂SO₄, △", product: "2-呋喃乙酸乙酯", reaction_type: "酯化反应" }
    ]
  },
  {
    id: 120,
    title: "2-噻吩甲胺合成路线",
    desc: "噻吩→2-噻吩甲胺(7步)，溴代→Grignard→CO₂羧化→酸化→酰氯化→酰胺化→LiAlH₄还原，经典含硫杂环衍生物合成",
    steps: [
      { step_number: 1, reactant: "噻吩", reagent: "Br₂, CH₃COOH, 0°C", product: "2-溴噻吩", reaction_type: "取代反应" },
      { step_number: 2, reactant: "2-溴噻吩", reagent: "Mg, 无水乙醚, △", product: "2-噻吩溴化镁", reaction_type: "加成反应" },
      { step_number: 3, reactant: "2-噻吩溴化镁", reagent: "CO₂, 无水乙醚", product: "2-噻吩甲酸镁盐", reaction_type: "加成反应" },
      { step_number: 4, reactant: "2-噻吩甲酸镁盐", reagent: "HCl, H₂O", product: "2-噻吩甲酸", reaction_type: "酸碱反应" },
      { step_number: 5, reactant: "2-噻吩甲酸", reagent: "SOCl₂, △", product: "2-噻吩甲酰氯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "2-噻吩甲酰氯", reagent: "NH₃, 0°C", product: "2-噻吩甲酰胺", reaction_type: "取代反应" },
      { step_number: 7, reactant: "2-噻吩甲酰胺", reagent: "LiAlH₄, 无水乙醚, △", product: "2-噻吩甲胺", reaction_type: "还原反应" }
    ]
  },
  {
    id: 121,
    title: "2-吡咯甲醛合成路线",
    desc: "吡咯→2-吡咯甲醛(7步)，Friedel-Crafts→卤仿反应→酸化→酰氯化→酯化→LiAlH₄还原→PCC氧化，经典含氮杂环醛合成",
    steps: [
      { step_number: 1, reactant: "吡咯", reagent: "(CH₃CO)₂O, BF₃, 0°C", product: "2-乙酰基吡咯", reaction_type: "取代反应" },
      { step_number: 2, reactant: "2-乙酰基吡咯", reagent: "Br₂, NaOH, H₂O, △", product: "2-吡咯甲酸钠", reaction_type: "氧化反应" },
      { step_number: 3, reactant: "2-吡咯甲酸钠", reagent: "HCl, H₂O", product: "2-吡咯甲酸", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "2-吡咯甲酸", reagent: "SOCl₂, △", product: "2-吡咯甲酰氯", reaction_type: "取代反应" },
      { step_number: 5, reactant: "2-吡咯甲酰氯", reagent: "C₂H₅OH, 吡啶", product: "2-吡咯甲酸乙酯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "2-吡咯甲酸乙酯", reagent: "LiAlH₄, 无水乙醚, △", product: "2-吡咯甲醇", reaction_type: "还原反应" },
      { step_number: 7, reactant: "2-吡咯甲醇", reagent: "PCC, CH₂Cl₂, 25°C", product: "2-吡咯甲醛", reaction_type: "氧化反应" }
    ]
  },
  {
    id: 122,
    title: "3-氨基吡啶合成路线",
    desc: "吡啶→3-氨基吡啶(7步)，溴代→Grignard→CO₂羧化→酸化→酰氯化→酰胺化→Hofmann重排，经典含氮杂环胺合成",
    steps: [
      { step_number: 1, reactant: "吡啶", reagent: "Br₂, Fe, 300°C", product: "3-溴吡啶", reaction_type: "取代反应" },
      { step_number: 2, reactant: "3-溴吡啶", reagent: "Mg, 无水乙醚, △", product: "3-吡啶溴化镁", reaction_type: "加成反应" },
      { step_number: 3, reactant: "3-吡啶溴化镁", reagent: "CO₂, 无水乙醚", product: "3-吡啶甲酸镁盐", reaction_type: "加成反应" },
      { step_number: 4, reactant: "3-吡啶甲酸镁盐", reagent: "HCl, H₂O", product: "3-吡啶甲酸", reaction_type: "酸碱反应" },
      { step_number: 5, reactant: "3-吡啶甲酸", reagent: "SOCl₂, △", product: "3-吡啶甲酰氯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "3-吡啶甲酰氯", reagent: "NH₃, 0°C", product: "3-吡啶甲酰胺", reaction_type: "取代反应" },
      { step_number: 7, reactant: "3-吡啶甲酰胺", reagent: "Br₂, NaOH, H₂O, △", product: "3-氨基吡啶", reaction_type: "消去反应" }
    ]
  },
  {
    id: 123,
    title: "5-溴-2-吡啶甲酸合成路线",
    desc: "吡啶→5-溴-2-吡啶甲酸(7步)，氨基化→乙酰化→溴代→水解→重氮化→Sandmeyer氰化→水解，经典含氮杂环卤代酸合成",
    steps: [
      { step_number: 1, reactant: "吡啶", reagent: "NaNH₂, 液NH₃, -33°C", product: "2-氨基吡啶", reaction_type: "取代反应" },
      { step_number: 2, reactant: "2-氨基吡啶", reagent: "(CH₃CO)₂O, 吡啶", product: "2-乙酰氨基吡啶", reaction_type: "取代反应" },
      { step_number: 3, reactant: "2-乙酰氨基吡啶", reagent: "Br₂, CH₃COOH, 25°C", product: "2-乙酰氨基-5-溴吡啶", reaction_type: "取代反应" },
      { step_number: 4, reactant: "2-乙酰氨基-5-溴吡啶", reagent: "NaOH, H₂O, △", product: "2-氨基-5-溴吡啶", reaction_type: "水解反应" },
      { step_number: 5, reactant: "2-氨基-5-溴吡啶", reagent: "NaNO₂, HCl, 0-5°C", product: "5-溴-2-吡啶重氮盐", reaction_type: "取代反应" },
      { step_number: 6, reactant: "5-溴-2-吡啶重氮盐", reagent: "CuCN, KCN, 0°C", product: "5-溴-2-氰基吡啶", reaction_type: "取代反应" },
      { step_number: 7, reactant: "5-溴-2-氰基吡啶", reagent: "H₂O, H⁺, △", product: "5-溴-2-吡啶甲酸", reaction_type: "水解反应" }
    ]
  },
  {
    id: 124,
    title: "2-乙酰氨基-4-甲基噻唑合成路线",
    desc: "乙酸→2-乙酰氨基-4-甲基噻唑(7步)，酯化→Claisen缩合→酸化→酮式水解→α-溴代→Hantzsch噻唑合成→乙酰化，经典含硫氮杂环合成",
    steps: [
      { step_number: 1, reactant: "乙酸", reagent: "C₂H₅OH, 浓H₂SO₄, △", product: "乙酸乙酯", reaction_type: "酯化反应" },
      { step_number: 2, reactant: "乙酸乙酯", reagent: "NaOEt, C₂H₅OH", product: "乙酰乙酸乙酯钠盐", reaction_type: "缩合反应" },
      { step_number: 3, reactant: "乙酰乙酸乙酯钠盐", reagent: "HCl, H₂O", product: "乙酰乙酸乙酯", reaction_type: "酸碱反应" },
      { step_number: 4, reactant: "乙酰乙酸乙酯", reagent: "稀NaOH, H₂O, △", product: "丙酮", reaction_type: "水解反应" },
      { step_number: 5, reactant: "丙酮", reagent: "Br₂, CH₃COOH, 0°C", product: "溴丙酮", reaction_type: "取代反应" },
      { step_number: 6, reactant: "溴丙酮", reagent: "硫脲, C₂H₅OH, △", product: "2-氨基-4-甲基噻唑", reaction_type: "缩合反应" },
      { step_number: 7, reactant: "2-氨基-4-甲基噻唑", reagent: "(CH₃CO)₂O, 吡啶", product: "2-乙酰氨基-4-甲基噻唑", reaction_type: "取代反应" }
    ]
  },
  {
    id: 125,
    title: "酪氨醇合成路线",
    desc: "苯酚→酪氨醇(8步)，Reimer-Tiemann→Perkin缩合→水解→催化氢化→HVZ溴代→氨解→酯化→LiAlH₄还原，经典芳香族氨基醇合成",
    steps: [
      { step_number: 1, reactant: "苯酚", reagent: "CHCl₃, NaOH, H₂O, △", product: "对羟基苯甲醛", reaction_type: "取代反应" },
      { step_number: 2, reactant: "对羟基苯甲醛", reagent: "CH₃COONa, (CH₃CO)₂O, △", product: "对乙酰氧基肉桂酸", reaction_type: "缩合反应" },
      { step_number: 3, reactant: "对乙酰氧基肉桂酸", reagent: "NaOH, H₂O, △", product: "对羟基肉桂酸钠", reaction_type: "水解反应" },
      { step_number: 4, reactant: "对羟基肉桂酸钠", reagent: "(1) HCl, H₂O; (2) H₂, Pd/C, C₂H₅OH", product: "对羟基苯丙酸", reaction_type: "加成反应" },
      { step_number: 5, reactant: "对羟基苯丙酸", reagent: "Br₂, P, △", product: "α-溴-对羟基苯丙酸", reaction_type: "取代反应" },
      { step_number: 6, reactant: "α-溴-对羟基苯丙酸", reagent: "NH₃, C₂H₅OH, △", product: "酪氨酸", reaction_type: "取代反应" },
      { step_number: 7, reactant: "酪氨酸", reagent: "C₂H₅OH, 浓H₂SO₄, △", product: "酪氨酸乙酯", reaction_type: "酯化反应" },
      { step_number: 8, reactant: "酪氨酸乙酯", reagent: "LiAlH₄, 无水乙醚, △", product: "酪氨醇", reaction_type: "还原反应" }
    ]
  },
  {
    id: 126,
    title: "2-乙酰氨基喹啉合成路线",
    desc: "苯胺→2-乙酰氨基喹啉(8步)，乙酰化→Doebner-Miller环化→KMnO₄氧化→酸化→酰氯化→酰胺化→Hofmann重排→乙酰化，经典含氮杂环合成",
    steps: [
      { step_number: 1, reactant: "苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 2, reactant: "乙酰苯胺", reagent: "CH₃CHO, ZnCl₂, △", product: "2-甲基喹啉", reaction_type: "缩合反应" },
      { step_number: 3, reactant: "2-甲基喹啉", reagent: "KMnO₄, OH⁻, H₂O, △", product: "2-喹啉甲酸钾", reaction_type: "氧化反应" },
      { step_number: 4, reactant: "2-喹啉甲酸钾", reagent: "HCl, H₂O", product: "2-喹啉甲酸", reaction_type: "酸碱反应" },
      { step_number: 5, reactant: "2-喹啉甲酸", reagent: "SOCl₂, △", product: "2-喹啉甲酰氯", reaction_type: "取代反应" },
      { step_number: 6, reactant: "2-喹啉甲酰氯", reagent: "NH₃, 0°C", product: "2-喹啉甲酰胺", reaction_type: "取代反应" },
      { step_number: 7, reactant: "2-喹啉甲酰胺", reagent: "Br₂, NaOH, H₂O, △", product: "2-氨基喹啉", reaction_type: "消去反应" },
      { step_number: 8, reactant: "2-氨基喹啉", reagent: "(CH₃CO)₂O, 吡啶", product: "2-乙酰氨基喹啉", reaction_type: "取代反应" }
    ]
  },
  {
    id: 127,
    title: "3,5-二甲基-4-吡唑甲酸合成路线",
    desc: "乙酰乙酸乙酯→3,5-二甲基-4-吡唑甲酸(8步)，成盐→乙酰化→肼环化→硝化→还原→重氮化→Sandmeyer氰化→水解，经典含氮杂环合成",
    steps: [
      { step_number: 1, reactant: "乙酰乙酸乙酯", reagent: "NaOEt, C₂H₅OH", product: "乙酰乙酸乙酯钠盐", reaction_type: "酸碱反应" },
      { step_number: 2, reactant: "乙酰乙酸乙酯钠盐", reagent: "CH₃COCl, 0°C", product: "α-乙酰基乙酰乙酸乙酯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "α-乙酰基乙酰乙酸乙酯", reagent: "H₂NNH₂·H₂O, C₂H₅OH, △", product: "3,5-二甲基吡唑", reaction_type: "缩合反应" },
      { step_number: 4, reactant: "3,5-二甲基吡唑", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "4-硝基-3,5-二甲基吡唑", reaction_type: "取代反应" },
      { step_number: 5, reactant: "4-硝基-3,5-二甲基吡唑", reagent: "Fe, HCl, △", product: "4-氨基-3,5-二甲基吡唑", reaction_type: "还原反应" },
      { step_number: 6, reactant: "4-氨基-3,5-二甲基吡唑", reagent: "NaNO₂, HCl, 0-5°C", product: "3,5-二甲基-4-吡唑重氮盐", reaction_type: "取代反应" },
      { step_number: 7, reactant: "3,5-二甲基-4-吡唑重氮盐", reagent: "CuCN, KCN, 0°C", product: "4-氰基-3,5-二甲基吡唑", reaction_type: "取代反应" },
      { step_number: 8, reactant: "4-氰基-3,5-二甲基吡唑", reagent: "H₂O, H⁺, △", product: "3,5-二甲基-4-吡唑甲酸", reaction_type: "水解反应" }
    ]
  },
  {
    id: 128,
    title: "2-氨基-4,6-二甲基-5-嘧啶甲酸合成路线",
    desc: "乙酰丙酮→2-氨基-4,6-二甲基-5-嘧啶甲酸(8步)，环化→氯化→氨解→硝化→还原→重氮化→Sandmeyer氰化→水解，经典含氮杂环合成",
    steps: [
      { step_number: 1, reactant: "乙酰丙酮", reagent: "尿素, HCl, C₂H₅OH, △", product: "4,6-二甲基-2-嘧啶酮", reaction_type: "缩合反应" },
      { step_number: 2, reactant: "4,6-二甲基-2-嘧啶酮", reagent: "POCl₃, △", product: "2-氯-4,6-二甲基嘧啶", reaction_type: "取代反应" },
      { step_number: 3, reactant: "2-氯-4,6-二甲基嘧啶", reagent: "NH₃, C₂H₅OH, 150°C", product: "2-氨基-4,6-二甲基嘧啶", reaction_type: "取代反应" },
      { step_number: 4, reactant: "2-氨基-4,6-二甲基嘧啶", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "2-氨基-5-硝基-4,6-二甲基嘧啶", reaction_type: "取代反应" },
      { step_number: 5, reactant: "2-氨基-5-硝基-4,6-二甲基嘧啶", reagent: "Fe, HCl, △", product: "2,5-二氨基-4,6-二甲基嘧啶", reaction_type: "还原反应" },
      { step_number: 6, reactant: "2,5-二氨基-4,6-二甲基嘧啶", reagent: "NaNO₂, HCl, 0-5°C", product: "2-氨基-4,6-二甲基-5-嘧啶重氮盐", reaction_type: "取代反应" },
      { step_number: 7, reactant: "2-氨基-4,6-二甲基-5-嘧啶重氮盐", reagent: "CuCN, KCN, 0°C", product: "2-氨基-5-氰基-4,6-二甲基嘧啶", reaction_type: "取代反应" },
      { step_number: 8, reactant: "2-氨基-5-氰基-4,6-二甲基嘧啶", reagent: "H₂O, H⁺, △", product: "2-氨基-4,6-二甲基-5-嘧啶甲酸", reaction_type: "水解反应" }
    ]
  },
  {
    id: 129,
    title: "2-(1-苯乙基)呋喃合成路线",
    desc: "呋喃→2-(1-苯乙基)呋喃(8步)，溴代→Grignard→醛加成→PCC氧化→Clemmensen还原→溴代→消去→催化氢化，经典含氧杂环芳基化合成",
    steps: [
      { step_number: 1, reactant: "呋喃", reagent: "Br₂, 0°C", product: "2-溴呋喃", reaction_type: "取代反应" },
      { step_number: 2, reactant: "2-溴呋喃", reagent: "Mg, 无水乙醚, △", product: "2-呋喃溴化镁", reaction_type: "加成反应" },
      { step_number: 3, reactant: "2-呋喃溴化镁", reagent: "苯甲醛, 无水乙醚", product: "2-呋喃苯甲醇", reaction_type: "加成反应" },
      { step_number: 4, reactant: "2-呋喃苯甲醇", reagent: "PCC, CH₂Cl₂", product: "2-苯甲酰基呋喃", reaction_type: "氧化反应" },
      { step_number: 5, reactant: "2-苯甲酰基呋喃", reagent: "Zn-Hg, HCl, △", product: "2-苄基呋喃", reaction_type: "还原反应" },
      { step_number: 6, reactant: "2-苄基呋喃", reagent: "Br₂, 光照", product: "2-(α-溴苄基)呋喃", reaction_type: "取代反应" },
      { step_number: 7, reactant: "2-(α-溴苄基)呋喃", reagent: "KOH, C₂H₅OH, △", product: "2-(α-苯乙烯基)呋喃", reaction_type: "消去反应" },
      { step_number: 8, reactant: "2-(α-苯乙烯基)呋喃", reagent: "H₂, Pd/C, C₂H₅OH", product: "2-(1-苯乙基)呋喃", reaction_type: "加成反应" }
    ]
  },
  {
    id: 130,
    title: "5-溴-2-呋喃乙酸乙酯合成路线",
    desc: "呋喃→5-溴-2-呋喃乙酸乙酯(8步)，溴代→Friedel-Crafts→还原→卤代→腈化→水解→酸化→酯化，经典含氧杂环卤代酯合成",
    steps: [
      { step_number: 1, reactant: "呋喃", reagent: "Br₂, 0°C", product: "2-溴呋喃", reaction_type: "取代反应" },
      { step_number: 2, reactant: "2-溴呋喃", reagent: "(CH₃CO)₂O, BF₃, 0°C", product: "2-乙酰基-5-溴呋喃", reaction_type: "取代反应" },
      { step_number: 3, reactant: "2-乙酰基-5-溴呋喃", reagent: "NaBH₄, CH₃OH", product: "1-(5-溴-2-呋喃基)乙醇", reaction_type: "还原反应" },
      { step_number: 4, reactant: "1-(5-溴-2-呋喃基)乙醇", reagent: "PBr₃, 0°C", product: "1-(5-溴-2-呋喃基)溴乙烷", reaction_type: "取代反应" },
      { step_number: 5, reactant: "1-(5-溴-2-呋喃基)溴乙烷", reagent: "KCN, C₂H₅OH, △", product: "5-溴-2-呋喃乙腈", reaction_type: "取代反应" },
      { step_number: 6, reactant: "5-溴-2-呋喃乙腈", reagent: "NaOH, H₂O, △", product: "5-溴-2-呋喃乙酸钠", reaction_type: "水解反应" },
      { step_number: 7, reactant: "5-溴-2-呋喃乙酸钠", reagent: "HCl, H₂O", product: "5-溴-2-呋喃乙酸", reaction_type: "酸碱反应" },
      { step_number: 8, reactant: "5-溴-2-呋喃乙酸", reagent: "C₂H₅OH, 浓H₂SO₄, △", product: "5-溴-2-呋喃乙酸乙酯", reaction_type: "酯化反应" }
    ]
  },
  {
    id: 131,
    title: "5,6-二乙酰氨基苯并噻唑合成路线",
    desc: "苯胺→5,6-二乙酰氨基苯并噻唑(8步)，乙酰化→氯磺化→还原→环化→重氮化脱氨→苯环硝化→还原→乙酰化，经典含硫氮杂环合成",
    steps: [
      { step_number: 1, reactant: "苯胺", reagent: "(CH₃CO)₂O, 吡啶", product: "乙酰苯胺", reaction_type: "取代反应" },
      { step_number: 2, reactant: "乙酰苯胺", reagent: "ClSO₃H, 60°C", product: "对乙酰氨基苯磺酰氯", reaction_type: "取代反应" },
      { step_number: 3, reactant: "对乙酰氨基苯磺酰氯", reagent: "Zn, HCl, △", product: "对乙酰氨基苯硫酚", reaction_type: "还原反应" },
      { step_number: 4, reactant: "对乙酰氨基苯硫酚", reagent: "BrCN, C₂H₅OH, △", product: "2-氨基-6-乙酰氨基苯并噻唑", reaction_type: "缩合反应" },
      { step_number: 5, reactant: "2-氨基-6-乙酰氨基苯并噻唑", reagent: "NaNO₂, HCl, 0-5°C; 然后H₃PO₂", product: "6-乙酰氨基苯并噻唑", reaction_type: "取代反应" },
      { step_number: 6, reactant: "6-乙酰氨基苯并噻唑", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "5-硝基-6-乙酰氨基苯并噻唑", reaction_type: "取代反应" },
      { step_number: 7, reactant: "5-硝基-6-乙酰氨基苯并噻唑", reagent: "Fe, HCl, △", product: "5-氨基-6-乙酰氨基苯并噻唑", reaction_type: "还原反应" },
      { step_number: 8, reactant: "5-氨基-6-乙酰氨基苯并噻唑", reagent: "(CH₃CO)₂O, 吡啶", product: "5,6-二乙酰氨基苯并噻唑", reaction_type: "取代反应" }
    ]
  },
  {
    id: 132,
    title: "2-氨基-5-硝基-4,6-二(氰甲基)嘧啶合成路线",
    desc: "乙酰丙酮→2-氨基-5-硝基-4,6-二(氰甲基)嘧啶(8步)，环化→乙酰化保护→硝化→自由基溴代→腈化→脱保护→成盐→中和，经典含氮杂环多官能团合成",
    steps: [
      { step_number: 1, reactant: "乙酰丙酮", reagent: "硝酸胍, NaOEt, C₂H₅OH, △", product: "2-氨基-4,6-二甲基嘧啶", reaction_type: "缩合反应" },
      { step_number: 2, reactant: "2-氨基-4,6-二甲基嘧啶", reagent: "(CH₃CO)₂O, 吡啶", product: "2-乙酰氨基-4,6-二甲基嘧啶", reaction_type: "取代反应" },
      { step_number: 3, reactant: "2-乙酰氨基-4,6-二甲基嘧啶", reagent: "浓HNO₃, 浓H₂SO₄, 0°C", product: "2-乙酰氨基-5-硝基-4,6-二甲基嘧啶", reaction_type: "取代反应" },
      { step_number: 4, reactant: "2-乙酰氨基-5-硝基-4,6-二甲基嘧啶", reagent: "Br₂, 光照, CCl₄", product: "2-乙酰氨基-5-硝基-4,6-二(溴甲基)嘧啶", reaction_type: "取代反应" },
      { step_number: 5, reactant: "2-乙酰氨基-5-硝基-4,6-二(溴甲基)嘧啶", reagent: "KCN, C₂H₅OH, △", product: "2-乙酰氨基-5-硝基-4,6-二(氰甲基)嘧啶", reaction_type: "取代反应" },
      { step_number: 6, reactant: "2-乙酰氨基-5-硝基-4,6-二(氰甲基)嘧啶", reagent: "NaOH, H₂O, 0°C", product: "2-氨基-5-硝基-4,6-二(氰甲基)嘧啶", reaction_type: "水解反应" },
      { step_number: 7, reactant: "2-氨基-5-硝基-4,6-二(氰甲基)嘧啶", reagent: "HCl, 乙醚", product: "2-氨基-5-硝基-4,6-二(氰甲基)嘧啶盐酸盐", reaction_type: "酸碱反应" },
      { step_number: 8, reactant: "2-氨基-5-硝基-4,6-二(氰甲基)嘧啶盐酸盐", reagent: "NaOH, H₂O", product: "2-氨基-5-硝基-4,6-二(氰甲基)嘧啶", reaction_type: "酸碱反应" }
    ]
  }
];

export default ROUTE_LIBRARY;
