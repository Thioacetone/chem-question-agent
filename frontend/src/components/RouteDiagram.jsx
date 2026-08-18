import { useState, useEffect, useRef } from 'react'

/**
 * 合成路线图组件 — 仿照高考真题格式
 * 显示结构A → 结构B → 结构C → ... 的流程图
 * 箭头上方标注试剂/条件，结构下方标注化合物编号
 */
export default function RouteDiagram({ routeData, title = '' }) {
  const [svg, setSvg] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const mountedRef = useRef(true)

  useEffect(() => {
    mountedRef.current = true
    if (!routeData || !routeData.steps || routeData.steps.length === 0) return

    const loadDiagram = async () => {
      setLoading(true)
      setError(null)
      try {
        const res = await fetch('/api/render/route-diagram', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            steps: routeData.steps,
            title: title || routeData.title || '',
            hidden_structure: routeData.hidden_structure || null,
          }),
        })
        if (!res.ok) {
          const errData = await res.json().catch(() => ({}))
          throw new Error(errData.detail || '路线图渲染失败')
        }
        const svgText = await res.text()
        if (mountedRef.current) {
          // 将固定宽高的 SVG 改为响应式：width="100%" height="auto"，保留 viewBox
          const responsive = svgText
            .replace(/<svg\s+width="[^"]*"\s+height="[^"]*"/, '<svg width="100%" height="auto"')
            .replace(/<svg\s+height="[^"]*"\s+width="[^"]*"/, '<svg width="100%" height="auto"')
          setSvg(responsive)
        }
      } catch (e) {
        if (mountedRef.current) {
          setError(e.message)
        }
      } finally {
        if (mountedRef.current) {
          setLoading(false)
        }
      }
    }

    loadDiagram()
    return () => { mountedRef.current = false }
  }, [routeData, title])

  // 无数据
  if (!routeData || !routeData.steps || routeData.steps.length === 0) return null

  // 加载中
  if (loading) {
    return (
      <div style={{
        padding: '16px',
        textAlign: 'center',
        marginBottom: '12px',
      }}>
        <span style={{ fontSize: '12px', color: '#aaa' }}>渲染路线图中...</span>
      </div>
    )
  }

  // 错误 — 降级为文字版路线
  if (error) {
    const steps = routeData.steps || []
    const textRoute = steps.map((s, i) => {
      const reactant = s.reactant || s.name || '?'
      const product = s.product || '?'
      const reagent = s.reagent || ''
      return `${chr(65 + i)}→${chr(65 + i + 1)}：${reactant} ${reagent ? `—${reagent}→` : '→'} ${product}`
    }).join('；')

    return (
      <div style={{
        padding: '10px 14px',
        background: '#fafafa',
        borderRadius: '6px',
        border: '1px solid #e0e0e0',
        marginBottom: '12px',
        fontSize: '13px',
        lineHeight: '1.8',
        color: '#555',
      }}>
        <div style={{ fontWeight: 600, marginBottom: '4px', fontSize: '12px', color: '#888' }}>合成路线</div>
        <div>{textRoute}</div>
      </div>
    )
  }

  // 成功渲染
  return (
    <div style={{
      padding: '4px 0',
      marginBottom: '12px',
      width: '100%',
      overflowX: 'auto',
      overflowY: 'visible',
    }}>
      <div
        dangerouslySetInnerHTML={{ __html: svg }}
        style={{
          display: 'block',
          lineHeight: 0,
          minWidth: '100%',
          background: 'white',
        }}
      />
    </div>
  )
}

// 辅助：数字转字母 A=0, B=1, C=2...
function chr(n) {
  return String.fromCharCode(65 + n)
}