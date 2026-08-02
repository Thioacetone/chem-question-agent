import { useState, useEffect, useRef } from 'react'

// 渲染缓存（同一会话内不重复请求）
const cache = {}

/**
 * 内联结构式渲染组件
 * 输入化合物名称，自动查询PubChem并渲染SVG结构式
 */
export default function InlineStructure({ name, size = 'small', showLabel = true }) {
  const [svg, setSvg] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(false)
  const mountedRef = useRef(true)

  const sizes = {
    small:  { w: 120, h: 80 },
    medium: { w: 180, h: 120 },
    large:  { w: 280, h: 180 },
  }
  const { w, h } = sizes[size] || sizes.small

  useEffect(() => {
    mountedRef.current = true
    if (!name || !name.trim()) return

    const load = async () => {
      // 检查缓存
      const cacheKey = `${name}_${w}_${h}`
      if (cache[cacheKey]) {
        setSvg(cache[cacheKey])
        return
      }

      setLoading(true)
      setError(false)
      try {
        // 1. 名称→SMILES
        const nameRes = await fetch('/api/render/name-to-smiles', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name }),
        })
        if (!nameRes.ok) throw new Error('查询失败')
        const nameData = await nameRes.json()
        if (!nameData.smiles) throw new Error('未找到')

        // 2. SMILES→SVG
        const svgRes = await fetch('/api/render/svg', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ smiles: nameData.smiles, label: '', width: w, height: h }),
        })
        if (!svgRes.ok) throw new Error('渲染失败')
        const svgText = await svgRes.text()

        if (mountedRef.current) {
          cache[cacheKey] = svgText
          setSvg(svgText)
        }
      } catch {
        if (mountedRef.current) setError(true)
      } finally {
        if (mountedRef.current) setLoading(false)
      }
    }

    load()
    return () => { mountedRef.current = false }
  }, [name, w, h])

  if (!name || !name.trim()) return null

  return (
    <span style={{
      display: 'inline-flex',
      flexDirection: 'column',
      alignItems: 'center',
      verticalAlign: 'middle',
      margin: '0 2px',
    }}>
      {loading && (
        <span style={{
          width: w,
          height: h,
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: '#f5f5f5',
          borderRadius: '4px',
          border: '1px dashed #ddd',
          fontSize: '11px',
          color: '#999',
        }}>
          ...
        </span>
      )}
      {error && (
        <span style={{
          fontSize: '11px',
          color: '#999',
          padding: '2px 6px',
          background: '#fafafa',
          borderRadius: '4px',
          border: '1px dashed #eee',
        }}>
          {name}
        </span>
      )}
      {svg && !loading && (
        <span
          dangerouslySetInnerHTML={{ __html: svg }}
          style={{ display: 'inline-block', lineHeight: 0 }}
        />
      )}
      {showLabel && svg && !loading && (
        <span style={{ fontSize: '10px', color: '#888', marginTop: '2px' }}>{name}</span>
      )}
    </span>
  )
}