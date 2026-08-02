import StructureInline from './StructureInline.jsx'

/**
 * 富文本渲染组件
 * 支持纯文本 + {结构式:...} 或 {{结构式:...}} 占位符渲染为内联SVG结构式
 *
 * 用法：
 * <RichTextRenderer text="化合物B的结构式为{结构式:化合物B}" routeData={routeData} />
 */
export default function RichTextRenderer({ text, structureSize = 'small', showLabels = false, routeData }) {
  if (!text) return null

  // 防御：非字符串内容（如对象、数组），显示可读文本
  if (typeof text !== 'string') {
    try {
      return <span style={{ lineHeight: '2.2', color: 'var(--text-primary)' }}>{String(text)}</span>
    } catch {
      return <span style={{ lineHeight: '2.2', color: '#999' }}>[无法显示]</span>
    }
  }

  const str = text

  // === 标准化：将所有 {结构式:...} 变体统一为 {{结构式:xxx}} ===
  let normalized = str

  // 仅在存在结构式占位符（含花括号）时才进行标准化处理
  // 避免对纯中文文本（仅含"结构式"一词但无占位符）进行不必要的处理
  const hasPlaceholder = /\{+\s*结构式\s*[：:]/.test(normalized)
  if (hasPlaceholder) {
    try {
      // 1. 中文冒号 → 英文冒号（仅在占位符上下文中）
      normalized = normalized.replace(/结构式\s*[：:]/g, '结构式:')
      // 2. 双大括号 → 单大括号（统一处理）
      normalized = normalized.replace(/\{\{结构式:([^}]+?)\}\}/g, '{结构式:$1}')
      // 3. 去空格：{ 结构式 : xxx } → {结构式:xxx}
      normalized = normalized.replace(/\{\s*结构式\s*:\s*([^}]+?)\s*\}/g, '{结构式:$1}')
      // 4. 单大括号 → 双大括号（标准格式）
      normalized = normalized.replace(/\{结构式:([^}]+?)\}/g, '{{结构式:$1}}')
    } catch {
      // 正则处理失败，使用原始文本
      normalized = str
    }
  }

  // 解析 {{结构式:...}} 占位符
  const pattern = /\{\{结构式:([^}]+?)\}\}/g
  const segments = []
  let lastIndex = 0
  let match

  // 重置 lastIndex（安全的 exec 循环）
  pattern.lastIndex = 0
  while ((match = pattern.exec(normalized)) !== null) {
    // 前面的纯文本
    if (match.index > lastIndex) {
      const textContent = normalized.slice(lastIndex, match.index)
      if (textContent) {
        segments.push({ type: 'text', content: textContent })
      }
    }
    // 结构式
    const name = match[1].trim()
    if (name && name.length > 0) {
      segments.push({ type: 'structure', name })
    }
    lastIndex = match.index + match[0].length
  }

  // 剩余纯文本
  if (lastIndex < normalized.length) {
    const remaining = normalized.slice(lastIndex)
    if (remaining) {
      segments.push({ type: 'text', content: remaining })
    }
  }

  // 如果没有占位符，纯文本渲染（使用原始 str 确保未修改）
  if (segments.length === 0 || (segments.length === 1 && segments[0].type === 'text')) {
    const lines = str.split('\n')
    return (
      <span style={{ lineHeight: '2.2' }}>
        {lines.map((line, i) => (
          <span key={i}>
            {i > 0 && <br />}
            {line}
          </span>
        ))}
      </span>
    )
  }

  // 有占位符：分段渲染
  return (
    <span style={{ lineHeight: '2.2' }}>
      {segments.map((seg, i) => {
        if (seg.type === 'text') {
          // 纯文本段：处理换行
          return (
            <span key={i}>
              {seg.content.split('\n').map((line, j, arr) => (
                <span key={j}>
                  {j > 0 && <br />}
                  {line}
                </span>
              ))}
            </span>
          )
        }
        // 结构式段
        return (
          <StructureInline
            key={i}
            name={seg.name}
            routeData={routeData}
            width={160}
            height={100}
          />
        )
      })}
    </span>
  )
}