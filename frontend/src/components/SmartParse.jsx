import { useState, useRef } from 'react'
import RouteDiagram from './RouteDiagram.jsx'

const EXAMPLE_TEXT = `以苯为起始原料，合成化合物G（对氨基苯酚，药物中间体）：

步骤1：苯与浓硝酸、浓硫酸在加热条件下反应，生成硝基苯（A），反应类型为硝化反应（取代反应）。
步骤2：硝基苯（A）在Fe/HCl条件下还原，得到苯胺（B），反应类型为还原反应。
步骤3：苯胺（B）与乙酸酐在醋酸中反应，得到乙酰苯胺（C），反应类型为酰化反应（取代反应）。
步骤4：乙酰苯胺（C）在浓硝酸、浓硫酸条件下硝化，得到对硝基乙酰苯胺（D），反应类型为硝化反应（取代反应）。
步骤5：对硝基乙酰苯胺（D）在NaOH水溶液中加热水解，得到对硝基苯胺（E），反应类型为水解反应（取代反应）。
步骤6：对硝基苯胺（E）在NaNO₂、H₂SO₄条件下重氮化，再经加热水解，得到对硝基苯酚（F），反应类型为重氮化反应、水解反应。
步骤7：对硝基苯酚（F）在Fe/HCl条件下还原，得到对氨基苯酚（G），反应类型为还原反应。`

export default function SmartParse({ onRouteParsed, onGenerate, loading, setLoading, setError }) {
  const [activeTab, setActiveTab] = useState('text')
  const [textInput, setTextInput] = useState('')
  const [parsedResult, setParsedResult] = useState(null)
  const [notes, setNotes] = useState('')
  const [difficulty, setDifficulty] = useState('中等')
  const fileInputRef = useRef(null)

  const handleParseText = async () => {
    if (!textInput.trim() || textInput.trim().length < 10) return
    setLoading(true)
    setError(null)
    setParsedResult(null)
    setNotes('')
    try {
      const res = await fetch('/api/parse/text', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ raw_text: textInput }),
      })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || '解析失败')
      }
      const data = await res.json()
      if (data.parse_error) {
        throw new Error('AI返回格式异常，请重试')
      }
      setParsedResult(data)
      setNotes(data.notes || '')
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleImageUpload = async (e) => {
    const file = e.target.files?.[0]
    if (!file) return
    setLoading(true)
    setError(null)
    setParsedResult(null)
    setNotes('')
    try {
      const formData = new FormData()
      formData.append('file', file)
      const res = await fetch('/api/parse/image-upload', {
        method: 'POST',
        body: formData,
      })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || '识别失败')
      }
      const data = await res.json()
      if (data.parse_error) {
        throw new Error('AI返回格式异常，请重试')
      }
      setParsedResult(data)
      setNotes(data.notes || '')
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleImagePaste = async (e) => {
    const items = e.clipboardData?.items
    if (!items) return
    for (let item of items) {
      if (item.type.startsWith('image/')) {
        const blob = item.getAsFile()
        if (!blob) continue
        setLoading(true)
        setError(null)
        setParsedResult(null)
        setNotes('')
        try {
          const formData = new FormData()
          formData.append('file', blob, 'paste.png')
          const res = await fetch('/api/parse/image-upload', {
            method: 'POST',
            body: formData,
          })
          if (!res.ok) {
            const err = await res.json()
            throw new Error(err.detail || '识别失败')
          }
          const data = await res.json()
          if (data.parse_error) {
            throw new Error('AI返回格式异常，请重试')
          }
          setParsedResult(data)
          setNotes(data.notes || '')
        } catch (e2) {
          setError(e2.message)
        } finally {
          setLoading(false)
        }
        break
      }
    }
  }

  const buildRouteData = () => {
    if (!parsedResult?.steps?.length) return null
    return {
      title: parsedResult.title || '智能识别的合成路线',
      steps: parsedResult.steps.map((s, i) => ({
        step_number: i + 1,
        reactant: s.reactant || '',
        reagent: s.reagent || '',
        product: s.product || '',
        reaction_type: s.reaction_type || '',
      })),
    }
  }

  const handleFillRoute = () => {
    const routeData = buildRouteData()
    if (!routeData) return
    onRouteParsed(routeData)
  }

  const handleGenerateFromParsed = () => {
    const routeData = buildRouteData()
    if (!routeData) return
    onGenerate(routeData, difficulty)
  }

  const loadExample = () => {
    setTextInput(EXAMPLE_TEXT)
  }

  const handleClear = () => {
    setTextInput('')
    setParsedResult(null)
    setNotes('')
    setError(null)
  }

  return (
    <div>
      <div className="card-title" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span>🤖 智能识别合成路线</span>
        <div style={{ display: 'flex', gap: '4px' }}>
          <button className="btn btn-outline btn-sm" onClick={loadExample}>📥 加载示例</button>
          <button className="btn btn-outline btn-sm" onClick={handleClear}>🗑 清空</button>
        </div>
      </div>

      <p style={{ fontSize: '12px', color: 'var(--text-secondary)', marginBottom: '14px' }}>
        将论文摘要、实验步骤、反应式文本粘贴到下方，或上传合成路线图片，AI会自动提取反应步骤并填充到左侧路线输入框。
      </p>

      {/* 标签切换 */}
      <div className="tabs" style={{ marginBottom: '12px' }}>
        <button
          className={`tab ${activeTab === 'text' ? 'active' : ''}`}
          onClick={() => setActiveTab('text')}
        >
          📝 文本粘贴
        </button>
        <button
          className={`tab ${activeTab === 'image' ? 'active' : ''}`}
          onClick={() => setActiveTab('image')}
        >
          🖼 图片上传
        </button>
      </div>

      {/* 文本粘贴 */}
      {activeTab === 'text' && (
        <div>
          <div className="form-group">
            <label className="form-label">粘贴合成路线文本</label>
            <textarea
              className="form-textarea"
              rows={8}
              value={textInput}
              onChange={e => setTextInput(e.target.value)}
              placeholder="粘贴论文摘要、实验步骤描述、反应式列表等...&#10;&#10;示例：&#10;以苯为起始原料，在浓硝酸/浓硫酸条件下硝化得到硝基苯(A)，&#10;然后在Fe/HCl条件下还原得到苯胺(B)..."
              style={{ fontSize: '13px', lineHeight: '1.8', fontFamily: 'inherit' }}
            />
          </div>
          <button
            className="btn btn-primary btn-block"
            onClick={handleParseText}
            disabled={loading || textInput.trim().length < 10}
          >
            {loading ? (
              <><span className="spinner" style={{ width: '14px', height: '14px', borderWidth: '2px' }}></span> AI正在解析...</>
            ) : (
              <>🔍 智能解析</>
            )}
          </button>
        </div>
      )}

      {/* 图片上传 */}
      {activeTab === 'image' && (
        <div>
          <div
            style={{
              border: '2px dashed var(--border)',
              borderRadius: 'var(--radius)',
              padding: '30px',
              textAlign: 'center',
              cursor: 'pointer',
              background: '#fafafa',
              transition: 'border-color 0.2s',
              marginBottom: '12px',
            }}
            onClick={() => fileInputRef.current?.click()}
            onPaste={handleImagePaste}
            tabIndex={0}
          >
            <div style={{ fontSize: '36px', marginBottom: '8px' }}>🖼</div>
            <p style={{ fontSize: '14px', color: 'var(--text-secondary)', marginBottom: '4px' }}>
              点击上传合成路线图片
            </p>
            <p style={{ fontSize: '11px', color: 'var(--text-light)' }}>
              支持 JPG、PNG、GIF、WebP（最大10MB）<br />
              也可以直接 Ctrl+V 粘贴截图
            </p>
            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              style={{ display: 'none' }}
              onChange={handleImageUpload}
            />
          </div>
          <p style={{ fontSize: '11px', color: 'var(--text-light)', textAlign: 'center' }}>
            支持 JPG、PNG、GIF、WebP 格式，通过OCR识别图片中的文字信息
          </p>
        </div>
      )}

      {/* 加载中 */}
      {loading && (
        <div className="loading" style={{ marginTop: '16px' }}>
          <div className="spinner"></div>
          <p>AI正在识别合成路线...</p>
        </div>
      )}

      {/* 解析结果 */}
      {parsedResult && !loading && (
        <div style={{ marginTop: '16px' }}>
          {parsedResult.steps?.length > 0 ? (
            <div style={{ marginBottom: '12px' }}>
              <div style={{
                padding: '10px 14px',
                background: '#e8f5e9',
                borderRadius: 'var(--radius)',
                border: '1px solid #a5d6a7',
                marginBottom: '12px',
              }}>
                <div style={{ fontWeight: 600, marginBottom: '4px', color: 'var(--success)' }}>
                  ✅ 识别成功！共 {parsedResult.steps?.length || 0} 步反应
                </div>
                {parsedResult.title && (
                  <div style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>
                    {parsedResult.title}
                  </div>
                )}
              </div>

              {/* 识别出的方程式：渲染为路线图 */}
              <div style={{
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius)',
                padding: '12px',
                background: '#fff',
              }}>
                <div style={{ fontWeight: 600, fontSize: '13px', marginBottom: '8px', color: 'var(--text-secondary)' }}>
                  📐 识别出的合成路线
                </div>
                <RouteDiagram
                  routeData={{
                    title: parsedResult.title || '',
                    steps: parsedResult.steps.map((s, i) => ({
                      step_number: i + 1,
                      reactant: s.reactant || '',
                      reagent: s.reagent || '',
                      product: s.product || '',
                      reaction_type: s.reaction_type || '',
                    })),
                  }}
                />
              </div>
            </div>
          ) : (
            <div style={{
              padding: '14px',
              background: '#fff3e0',
              borderRadius: 'var(--radius)',
              border: '1px solid #ffcc80',
              marginBottom: '12px',
            }}>
              <div style={{ fontWeight: 600, marginBottom: '8px', color: '#e65100' }}>
                ⚠ 未能识别出反应步骤
              </div>
              <div style={{ fontSize: '12px', lineHeight: '1.8', color: '#666' }}>
                {parsedResult.notes || '图片可能不包含可识别的文字信息。'}
              </div>
              <div style={{ fontSize: '11px', color: '#999', marginTop: '8px' }}>
                建议：① 确保图片清晰，文字可读 ② 图片中需包含化合物名称和反应条件 ③ 如含结构式请同时提供文字描述 ④ 可尝试用文本粘贴方式输入
              </div>
            </div>
          )}

          {/* OCR 原始文字（调试信息） */}
          {parsedResult._ocr_text && (
            <details style={{
              marginBottom: '12px',
              border: '1px solid #e0e0e0',
              borderRadius: 'var(--radius)',
              overflow: 'hidden',
            }}>
              <summary style={{
                padding: '8px 12px',
                background: '#f5f5f5',
                cursor: 'pointer',
                fontSize: '12px',
                fontWeight: 600,
                color: '#666',
                userSelect: 'none',
              }}>
                🔍 OCR识别到的原始文字（点击展开）
              </summary>
              <pre style={{
                margin: 0,
                padding: '10px 12px',
                fontSize: '11px',
                lineHeight: '1.6',
                color: '#555',
                background: '#fafafa',
                whiteSpace: 'pre-wrap',
                wordBreak: 'break-all',
                maxHeight: '200px',
                overflow: 'auto',
              }}>
                {parsedResult._ocr_text}
              </pre>
            </details>
          )}

          {/* 备注 */}
          {notes && parsedResult.steps?.length > 0 && (
            <div style={{
              padding: '10px 14px',
              background: '#fff3e0',
              borderRadius: 'var(--radius)',
              marginBottom: '12px',
              fontSize: '12px',
              border: '1px solid #ffcc80',
            }}>
              <strong>💡 备注：</strong>{notes}
            </div>
          )}

          {parsedResult.steps?.length > 0 && (
            <div>
              {/* 难度选择 + 生成命题 */}
              <div style={{
                border: '1px solid var(--border)',
                borderRadius: 'var(--radius)',
                padding: '14px',
                marginBottom: '12px',
                background: '#f9f9ff',
              }}>
                <div style={{ fontWeight: 600, fontSize: '13px', marginBottom: '10px', color: 'var(--text-secondary)' }}>
                  🎯 确认路线无误后，选择难度并生成命题
                </div>
                <div style={{ display: 'flex', gap: '8px', marginBottom: '12px', flexWrap: 'wrap' }}>
                  {['简单', '中等', '困难'].map(level => (
                    <button
                      key={level}
                      className={`btn btn-sm ${difficulty === level ? 'btn-primary' : 'btn-outline'}`}
                      onClick={() => setDifficulty(level)}
                      style={{ minWidth: '70px' }}
                    >
                      {level === '简单' ? '⭐' : level === '中等' ? '⭐⭐' : '⭐⭐⭐'} {level}
                    </button>
                  ))}
                </div>
                <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                  <button
                    className="btn btn-success"
                    onClick={handleGenerateFromParsed}
                    disabled={loading}
                    style={{ flex: 1, minWidth: '160px' }}
                  >
                    {loading ? (
                      <><span className="spinner" style={{ width: '14px', height: '14px', borderWidth: '2px' }}></span> 生成中...</>
                    ) : (
                      <>🚀 直接生成命题</>
                    )}
                  </button>
                  <button
                    className="btn btn-outline"
                    onClick={handleFillRoute}
                    disabled={loading}
                    style={{ flex: 1, minWidth: '160px' }}
                  >
                    📥 填充到路线输入框
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}