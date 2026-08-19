import { useState, useEffect, useRef } from 'react'

// 渲染缓存（同一会话内不重复请求）
const cache = {}

/**
 * 内联结构式渲染组件
 * 输入化合物名称，自动查询PubChem并渲染SVG结构式
 * @param {boolean} lazy - 是否启用懒加载（IntersectionObserver），默认false
 */
export default function InlineStructure({ name, size = 'small', showLabel = true, lazy = false }) {
  const [svg, setSvg] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(false)
  const [visible, setVisible] = useState(!lazy) // 非懒加载时直接可见
  const mountedRef = useRef(true)
  const containerRef = useRef(null)

  const sizes = {
    small:  { w: 120, h: 80 },
    medium: { w: 180, h: 120 },
    large:  { w: 280, h: 180 },
  }
  const { w, h } = sizes[size] || sizes.small

  // 懒加载：IntersectionObserver
  useEffect(() => {
    if (!lazy || !containerRef.current) return
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setVisible(true)
          observer.disconnect()
        }
      },
      { rootMargin: '200px' } // 提前200px开始加载
    )
    observer.observe(containerRef.current)
    return () => observer.disconnect()
  }, [lazy])

  // 加载结构式
  useEffect(() => {
    mountedRef.current = true
    if (!name || !name.trim()) return
    if (!visible) return // 懒加载：未进入视口不加载

    const load = async () => {
      // 检查缓存
      const cacheKey = `${name}_${w}_${h}`
      if (cache[cacheKey]) {
        setSvg(cache[cacheKey])
        return
      }

      setLoading(true)
      setError(false)

      // 最多重试 3 次，避免偶发性网络抖动 / 容器重启导致的 5xx 永久显示「错误占位」
      // 失败不写入全局缓存，以便用户下一次刷新时可以重跑
      let lastErr = null
      for (let attempt = 0; attempt < 3; attempt++) {
        try {
          const commonHeaders = { 'Content-Type': 'application/json' }
          // 1. 名称→SMILES（统一走后端 resolve_smiles：内置+离线映射+归一化+回退链）
          const nameRes = await fetch('/api/render/name-to-smiles', {
            method: 'POST',
            headers: commonHeaders,
            body: JSON.stringify({ name }),
          })
          if (!nameRes.ok) throw new Error('name HTTP ' + nameRes.status)
          const nameData = await nameRes.json()
          if (!nameData.smiles) throw new Error('no smiles: ' + (nameData.error || 'unknown'))

          // 2. SMILES→SVG
          const svgRes = await fetch('/api/render/svg', {
            method: 'POST',
            headers: commonHeaders,
            body: JSON.stringify({ smiles: nameData.smiles, label: '', width: w, height: h }),
          })
          if (!svgRes.ok) throw new Error('svg HTTP ' + svgRes.status)
          const svgText = await svgRes.text()
          if (!svgText || !svgText.includes('<svg')) throw new Error('svg payload invalid')

          if (mountedRef.current) {
            cache[cacheKey] = svgText   // 只缓存成功结果
            setSvg(svgText)
            setError(false)
          }
          lastErr = null
          return
        } catch (e) {
          lastErr = e
          if (attempt < 2) await new Promise(r => setTimeout(r, 400 * (attempt + 1)))
        }
      }
      if (lastErr && mountedRef.current) setError(true)
      if (mountedRef.current) setLoading(false)
    }

    load()
    return () => { mountedRef.current = false }
  }, [name, w, h, visible])

  if (!name || !name.trim()) return null

  return (
    <span ref={containerRef} style={{
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
      {!visible && !loading && !svg && !error && (
        <span style={{
          width: w,
          height: h,
          display: 'inline-flex',
          alignItems: 'center',
          justifyContent: 'center',
          background: '#fafafa',
          borderRadius: '4px',
          border: '1px dashed #eee',
        }}>
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