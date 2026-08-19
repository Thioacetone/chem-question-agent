import { useState, useEffect, useRef } from 'react'

/**
 * 内联结构式组件 — 在答案文本中渲染小型SVG结构式
 * 
 * 用法：
 * <StructureInline name="苯酚" />
 * <StructureInline name="化合物A" routeData={routeData} />
 * <StructureInline name="c1ccccc1O" />
 */
export default function StructureInline({ name, routeData, width = 160, height = 100 }) {
  const [svg, setSvg] = useState(null)
  const [error, setError] = useState(null)
  const mountedRef = useRef(true)

  useEffect(() => {
    mountedRef.current = true
    if (!name) return

    let resolvedName = name

    // 解析"化合物X"格式：从路线数据中查找SMILES
    const compoundMatch = name.match(/^化合物([A-Z])$/)
    if (compoundMatch && routeData) {
      const code = compoundMatch[1]
      const codeIndex = code.charCodeAt(0) - 65  // A=0, B=1, ...
      const steps = routeData.steps || []

      let found = null
      if (codeIndex === 0 && steps.length > 0) {
        // 化合物A = 第一步的反应物 → 优先用 reactant_smiles
        found = steps[0].reactant_smiles || steps[0].reactant || steps[0].product
      } else if (codeIndex > 0 && codeIndex <= steps.length) {
        // 化合物B、C... = 对应步骤的产物 → 优先用 product_smiles
        found = steps[codeIndex - 1].product_smiles || steps[codeIndex - 1].product
      }
      // 只有找到有效SMILES或有效名称时才使用，否则保持原name让后端解析
      if (found && found.length > 1) {
        resolvedName = found
      }
    }

    const loadSvg = async () => {
      setError(null)
      // 最多重试 3 次，避免偶发网络抖动 / 容器重启时的 5xx 永久显示「错误占位」
      let lastErr = null
      for (let attempt = 0; attempt < 3; attempt++) {
        try {
          const res = await fetch('/api/render/inline-svg', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Cache-Control': 'no-cache, no-store',
              'Pragma': 'no-cache',
            },
            body: JSON.stringify({ name: resolvedName, width, height }),
          })
          if (!res.ok) throw new Error('HTTP ' + res.status)
          let svgText = await res.text()
          // inline-svg 可能返回 JSON 包裹（后端新版本）或纯 SVG 字符串
          if (svgText && svgText.trim().startsWith('{')) {
            try {
              const obj = JSON.parse(svgText)
              if (obj && typeof obj.svg === 'string') svgText = obj.svg
            } catch (_) { /* keep as-is */ }
          }
          if (!svgText || !svgText.includes('<svg')) throw new Error('invalid svg payload')
          if (mountedRef.current) {
            setSvg(svgText)
          }
          lastErr = null
          return
        } catch (e) {
          lastErr = e
          if (attempt < 2) await new Promise(r => setTimeout(r, 400 * (attempt + 1)))
        }
      }
      if (mountedRef.current) {
        setError(lastErr ? lastErr.message : '渲染失败')
      }
    }

    loadSvg()
    return () => { mountedRef.current = false }
  }, [name, routeData, width, height])

  if (error) {
    return <span style={{ color: '#999', fontSize: '12px' }}>[{name}]</span>
  }

  if (!svg) {
    return <span style={{ color: '#ccc', fontSize: '12px' }}>...</span>
  }

  return (
    <span
      dangerouslySetInnerHTML={{ __html: svg }}
      style={{
        display: 'inline-block',
        verticalAlign: 'middle',
        lineHeight: 0,
        margin: '0 2px',
        background: 'white',
      }}
    />
  )
}