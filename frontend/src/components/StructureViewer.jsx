import { useState, useEffect, useRef, useCallback } from 'react'

/**
 * 常用化合物快捷按钮（内置映射，无需联网）
 */
const QUICK_COMPOUNDS = [
  '苯', '甲苯', '苯酚', '苯胺', '硝基苯', '苯甲酸', '苯甲醛', '苯乙烯',
  '萘', '蒽', '吡啶', '呋喃', '噻吩', '吡咯', '吲哚', '喹啉',
  '乙酸乙酯', '水杨酸', '对乙酰氨基酚', '阿司匹林',
  '乙酸', '乙醇', '丙酮', '乙二醇', '甘油', '葡萄糖',
  '甘氨酸', '咖啡因', '尿素', '樟脑', '胆固醇',
]

export default function StructureViewer() {
  const [smiles, setSmiles] = useState('c1ccccc1')
  const [label, setLabel] = useState('苯')
  const [svgContent, setSvgContent] = useState('')
  const [loading, setLoading] = useState(false)
  const [lookupStatus, setLookupStatus] = useState('') // '', '查询中...', 'PubChem', '内置'
  const [error, setError] = useState(null)
  const [searchResults, setSearchResults] = useState([])
  const [showDropdown, setShowDropdown] = useState(false)
  const [copyStatus, setCopyStatus] = useState('') // '', 'copied'
  const debounceRef = useRef(null)
  const containerRef = useRef(null)

  const renderStructure = async (s, l) => {
    if (!s.trim()) return
    setLoading(true)
    setError(null)
    try {
      const res = await fetch('/api/render/svg', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ smiles: s, label: l, width: 380, height: 200 }),
      })
      if (!res.ok) throw new Error('渲染失败')
      const svg = await res.text()
      setSvgContent(svg)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  /**
   * 通过后端API将名称转换为SMILES（内置+PubChem在线）
   */
  const lookupName = useCallback(async (name) => {
    if (!name.trim()) return null
    setLookupStatus('查询中...')
    try {
      const res = await fetch('/api/render/name-to-smiles', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name }),
      })
      if (!res.ok) throw new Error('查询失败')
      const data = await res.json()
      if (data.smiles) {
        setLookupStatus(data.source === 'pubchem' ? 'PubChem' : '内置')
        return data.smiles
      }
      setLookupStatus('')
      return null
    } catch {
      setLookupStatus('')
      return null
    }
  }, [])

  /**
   * 搜索化合物（PubChem在线）
   */
  const searchCompounds = useCallback(async (keyword) => {
    if (!keyword.trim() || keyword.trim().length < 2) {
      setSearchResults([])
      return
    }
    try {
      const res = await fetch(`/api/render/search?q=${encodeURIComponent(keyword)}&limit=8`)
      if (!res.ok) throw new Error('搜索失败')
      const data = await res.json()
      setSearchResults(data.results || [])
    } catch {
      setSearchResults([])
    }
  }, [])

  const handleNameInput = (name) => {
    setLabel(name)
    setLookupStatus('')
    setError(null)

    // 防抖：输入停止500ms后查询
    if (debounceRef.current) clearTimeout(debounceRef.current)
    if (name.trim().length >= 2) {
      debounceRef.current = setTimeout(async () => {
        const s = await lookupName(name)
        if (s) {
          setSmiles(s)
          renderStructure(s, name)
        }
      }, 500)
    }
  }

  const handleNameSubmit = async () => {
    if (!label.trim()) return
    setError(null)
    const s = await lookupName(label)
    if (s) {
      setSmiles(s)
      renderStructure(s, label)
    } else {
      setError(`未找到化合物"${label}"，请尝试英文名或直接输入SMILES`)
    }
  }

  const handleSmilesInput = (s) => {
    setSmiles(s)
    setLookupStatus('')
    if (s.trim().length > 2) {
      renderStructure(s, label)
    }
  }

  const handleSelectCompound = async (name) => {
    setLabel(name)
    setShowDropdown(false)
    setError(null)
    const s = await lookupName(name)
    if (s) {
      setSmiles(s)
      renderStructure(s, name)
    }
  }

  const handleCopySVG = async () => {
    if (!svgContent) return
    try {
      await navigator.clipboard.writeText(svgContent)
      setCopyStatus('copied')
      setTimeout(() => setCopyStatus(''), 2000)
    } catch {
      // 降级方案：使用 textarea
      const textarea = document.createElement('textarea')
      textarea.value = svgContent
      textarea.style.position = 'fixed'
      textarea.style.opacity = '0'
      document.body.appendChild(textarea)
      textarea.select()
      document.execCommand('copy')
      document.body.removeChild(textarea)
      setCopyStatus('copied')
      setTimeout(() => setCopyStatus(''), 2000)
    }
  }

  // 初始渲染
  useEffect(() => {
    renderStructure(smiles, label)
  }, [])

  return (
    <div ref={containerRef}>
      <div className="card-title"><span className="card-icon">🧬</span>ChemDraw 结构式渲染</div>
      <p style={{ fontSize: '11px', color: 'var(--text-secondary)', marginBottom: '12px' }}>
        输入任意化合物名称（中英文均可），通过PubChem自动查询结构式
      </p>

      {/* 名称输入 */}
      <div className="form-group">
        <label className="form-label">化合物名称</label>
        <div style={{ position: 'relative' }}>
          <div style={{ display: 'flex', gap: '6px' }}>
            <input
              className="form-input"
              value={label}
              onChange={e => handleNameInput(e.target.value)}
              onFocus={() => setShowDropdown(true)}
              onBlur={() => setTimeout(() => setShowDropdown(false), 250)}
              onKeyDown={e => e.key === 'Enter' && handleNameSubmit()}
              placeholder="输入任意名称，如：布洛芬、aspirin、对乙酰氨基酚..."
              style={{ flex: 1 }}
            />
            <button
              className="btn btn-primary btn-sm"
              onClick={handleNameSubmit}
              disabled={loading || !label.trim()}
              style={{ whiteSpace: 'nowrap' }}
            >
              {lookupStatus === '查询中...' ? '查询中...' : '🔍 查询'}
            </button>
          </div>
          {lookupStatus && lookupStatus !== '查询中...' && (
            <span style={{
              fontSize: '10px',
              color: lookupStatus === 'PubChem' ? 'var(--success)' : 'var(--text-light)',
              marginTop: '2px',
              display: 'block',
            }}>
              来源：{lookupStatus}
            </span>
          )}
        </div>
      </div>

      {/* SMILES输入 */}
      <div className="form-group">
        <label className="form-label">SMILES（自动填充或手动输入）</label>
        <div style={{ display: 'flex', gap: '8px' }}>
          <input
            className="form-input"
            value={smiles}
            onChange={e => handleSmilesInput(e.target.value)}
            onBlur={() => renderStructure(smiles, label)}
            placeholder="c1ccccc1"
            style={{ fontFamily: 'monospace', fontSize: '12px' }}
          />
          <button
            className="btn btn-outline btn-sm"
            onClick={() => renderStructure(smiles, label)}
            disabled={loading}
          >
            渲染
          </button>
        </div>
      </div>

      {/* 渲染结果 */}
      {error && (
        <div className="validation-panel error" style={{ marginBottom: '12px' }}>
          ⚠ {error}
        </div>
      )}

      {loading && (
        <div className="loading" style={{ padding: '20px' }}>
          <div className="spinner"></div>
          <p>{lookupStatus === '查询中...' ? 'PubChem查询中...' : '渲染中...'}</p>
        </div>
      )}

      {svgContent && !loading && (
        <div style={{
          background: 'white',
          border: '1px solid var(--border)',
          borderRadius: 'var(--radius)',
          padding: '12px',
          textAlign: 'center',
          overflow: 'auto',
        }}>
          <div dangerouslySetInnerHTML={{ __html: svgContent }} />
          <div style={{ marginTop: '8px', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '8px' }}>
            <span style={{ fontSize: '11px', color: 'var(--text-light)' }}>
              {label} — {smiles}
            </span>
            <button
              className="btn btn-outline btn-sm"
              onClick={handleCopySVG}
              style={{ fontSize: '11px' }}
            >
              {copyStatus === 'copied' ? '✅ 已复制' : '📋 复制SVG'}
            </button>
          </div>
        </div>
      )}

      {/* 常用化合物快捷按钮 */}
      <div className="form-group" style={{ marginTop: '12px' }}>
        <label className="form-label">常用化合物（点击即查）</label>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
          {QUICK_COMPOUNDS.map(name => (
            <button
              key={name}
              className="btn btn-outline btn-sm"
              style={{ fontSize: '11px' }}
              onClick={() => handleSelectCompound(name)}
            >
              {name}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}