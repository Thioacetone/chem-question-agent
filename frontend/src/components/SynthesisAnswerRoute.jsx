import { useMemo } from 'react'
import RouteDiagram from './RouteDiagram.jsx'

/**
 * 解析第5题答案文本，提取路线步骤
 * 返回 { title, steps } 或 null
 *
 * 高考标准格式：
 * 第1步：{{结构式:SMILES}}（原料）→[条件] {{结构式:SMILES}}（产物）
 * 第2步：{{结构式:SMILES}}（原料）→[条件] {{结构式:SMILES}}（产物）
 *
 * 兼容旧格式：
 * 第N步：原料在条件下得{结构式:SMILES}（产物）；
 */
export function parseAnswerRoute(answerText) {
  if (!answerText) return null

  // 防御：非字符串内容
  if (typeof answerText !== 'string') {
    return null
  }

  const text = answerText.trim()
  if (text.length === 0) return null

  // === 检测格式类型 ===
  const hasArrowFormat = /→\s*\[/.test(text)

  try {
    if (hasArrowFormat) {
      return parseArrowFormat(text)
    }
    return parseLegacyFormat(text)
  } catch {
    return null
  }
}

/**
 * 解析高考标准箭头格式：→[条件]
 */
function parseArrowFormat(text) {
  // 先统一结构式占位符为单大括号
  const normalized = text.replace(/\{\{结构式:([^}]+?)\}\}/g, '{结构式:$1}')

  // 按"第N步"或"第N步："拆分
  const stepParts = text.split(/第\d+步[：:]\s*/).filter(s => s.trim())
  if (stepParts.length === 0) return null

  const steps = []
  let prevProductSmiles = ''

  for (let i = 0; i < stepParts.length; i++) {
    const stepText = stepParts[i].trim().replace(/[；;。.]$/, '').trim()

    // 从当前步骤文本中提取SMILES
    const stepNormalized = stepText.replace(/\{\{结构式:([^}]+?)\}\}/g, '{结构式:$1}')
    const stepSmilies = []
    const stepSmPattern = /\{结构式:([^}]+?)\}/g
    let ssm
    while ((ssm = stepSmPattern.exec(stepNormalized)) !== null) {
      stepSmilies.push(ssm[1].trim())
    }

    if (stepSmilies.length === 0) continue

    // 提取条件：→[条件]
    const condMatch = stepText.match(/→\s*\[([^\]]+)\]/)
    const reagent = condMatch ? condMatch[1].trim() : ''

    // 提取化合物名（括号内）
    const names = []
    const namePattern = /（([^）]+)）/g
    let nm
    while ((nm = namePattern.exec(stepText)) !== null) {
      names.push(nm[1].trim())
    }

    // 第1步：反应物=第一个SMILES（或上一步产物）
    // 产物=最后一个SMILES
    const productSmiles = stepSmilies[stepSmilies.length - 1]
    const reactantSmiles = i === 0 ? stepSmilies[0] : prevProductSmiles

    const reactantName = i === 0 && names.length > 0 ? names[0] : ''
    const productName = names.length > 1 ? names[names.length - 1] : (names.length === 1 ? names[0] : '')

    steps.push({
      step_number: i + 1,
      reactant: reactantSmiles,
      reagent: reagent,
      product: productSmiles,
      product_name: productName || `产物${i + 1}`,
      reactant_name: reactantName,
    })

    prevProductSmiles = productSmiles
  }

  if (steps.length === 0) return null
  return { title: '合成路线', steps }
}

/**
 * 解析旧格式：原料在条件下得{结构式:SMILES}（产物）
 */
function parseLegacyFormat(text) {
  // 先统一结构式占位符为单大括号
  const normalized = text.replace(/\{\{结构式:([^}]+?)\}\}/g, '{结构式:$1}')

  // 解析 {结构式:SMILES} 占位符
  const structurePattern = /\{结构式:([^}]+?)\}/g
  const smilies = []
  let sm
  while ((sm = structurePattern.exec(normalized)) !== null) {
    smilies.push(sm[1].trim())
  }
  if (smilies.length === 0) return null

  // 解析每步
  const stepPattern = /第(\d+)步[：:]\s*/g
  const stepPositions = []
  let sp
  while ((sp = stepPattern.exec(text)) !== null) {
    stepPositions.push({ num: parseInt(sp[1]), start: sp.index + sp[0].length })
  }

  if (stepPositions.length === 0) {
    return buildRouteFromSmilies(smilies, text)
  }

  if (stepPositions.length !== smilies.length) {
    return buildRouteFromSmilies(smilies, text)
  }

  const steps = []
  for (let i = 0; i < stepPositions.length; i++) {
    const stepStart = stepPositions[i].start
    const stepEnd = i < stepPositions.length - 1
      ? stepPositions[i + 1].start - 5
      : text.length
    let stepText = text.slice(stepStart, stepEnd).trim()
    stepText = stepText.replace(/[；;。.]$/, '').trim()

    // 提取试剂条件
    let reagent = stepText
    const deIdx = stepText.lastIndexOf('得')
    if (deIdx >= 0) {
      reagent = stepText.slice(0, deIdx).trim()
    }
    reagent = cleanReagentText(reagent, i === 0)

    let reactant = ''
    if (i === 0) {
      const startMatch = stepText.match(/^([^\s在，,与用和经\d]+)/)
      if (startMatch) {
        reactant = startMatch[1].trim()
      }
    } else {
      reactant = smilies[i - 1]
    }

    let productName = `产物${stepPositions[i].num}`
    const nameMatch = stepText.match(/（([^）]+)）/)
    if (nameMatch) {
      productName = nameMatch[1].trim()
    }

    steps.push({
      step_number: stepPositions[i].num,
      reactant: reactant,
      reagent: reagent,
      product: smilies[i],
      product_name: productName,
    })
  }

  if (steps.length === 0) return null
  return { title: '合成路线', steps }
}

/**
 * 清理试剂文本
 */
function cleanReagentText(text, isFirstStep) {
  if (!text) return ''
  let cleaned = text

  if (isFirstStep) {
    cleaned = cleaned.replace(/^[^\s在，,与用和经]+/, '').trim()
  }

  cleaned = cleaned.replace(/^在\s*/, '')
  cleaned = cleaned
    .replace(/\s*条件下$/, '')
    .replace(/\s*反应$/, '')
    .replace(/\s*作用$/, '')
    .replace(/\s*下$/, '')
    .trim()
  cleaned = cleaned.replace(/^与\s*/, '')
  cleaned = cleaned.replace(/，/g, ', ').replace(/、/g, ', ')

  if (cleaned.length > 6) {
    cleaned = cleaned
      .replace(/[,，]\s*氧化$/, '')
      .replace(/[,，]\s*还原$/, '')
      .replace(/[,，]\s*酯化$/, '')
      .replace(/[,，]\s*酰化$/, '')
      .replace(/[,，]\s*硝化$/, '')
      .replace(/[,，]\s*水解$/, '')
      .replace(/[,，]\s*消去$/, '')
  }

  return cleaned.trim()
}

function buildRouteFromSmilies(smilies, text) {
  const segments = text.split(/[；;。]/).filter(s => s.trim())
  const steps = []

  for (let i = 0; i < smilies.length; i++) {
    const reactant = i === 0 ? '' : smilies[i - 1]
    let reagent = ''

    if (i < segments.length) {
      const seg = segments[i].trim()
      const deIdx = seg.lastIndexOf('得')
      if (deIdx >= 0) {
        reagent = cleanReagentText(seg.slice(0, deIdx).trim(), i === 0)
      }
    }

    let productName = `产物${i + 1}`
    if (i < segments.length) {
      const nameMatch = segments[i].match(/（([^）]+)）/)
      if (nameMatch) {
        productName = nameMatch[1].trim()
      }
    }

    steps.push({
      step_number: i + 1,
      reactant: reactant,
      reagent: reagent,
      product: smilies[i],
      product_name: productName,
    })
  }
  return steps.length > 0 ? { title: '合成路线', steps } : null
}

/**
 * 合成路线答案组件
 */
export default function SynthesisAnswerRoute({ answerText }) {
  const routeData = useMemo(() => parseAnswerRoute(answerText), [answerText])

  if (!routeData || !routeData.steps || routeData.steps.length === 0) {
    return null
  }

  return (
    <div style={{ marginTop: '8px', marginBottom: '8px' }}>
      <RouteDiagram routeData={routeData} title="" />
    </div>
  )
}