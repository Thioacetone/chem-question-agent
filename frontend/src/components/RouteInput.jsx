import { useState, useEffect } from 'react'
import InlineStructure from './InlineStructure.jsx'
import RouteDiagram from './RouteDiagram.jsx'

const BLANK_STEP = {
  step_number: 1,
  reactant: '',
  reagent: '',
  product: '',
  reaction_type: '',
}

const REACTION_TYPES = [
  '', '取代反应', '加成反应', '消去反应', '氧化反应',
  '还原反应', '酯化反应', '水解反应', '加聚反应', '缩聚反应',
]

export default function RouteInput({ onGenerate, loading, error, onReset }) {
  const [title, setTitle] = useState('')
  const [steps, setSteps] = useState([{ ...BLANK_STEP }])
  const [difficulty, setDifficulty] = useState(0.55)

  // 监听来自路线库页面的路线选择事件
  useEffect(() => {
    const handler = (e) => {
      const route = e.detail
      if (route && route.steps) {
        setTitle(route.title || '')
        setSteps(route.steps.map((s, i) => ({
          step_number: i + 1,
          reactant: s.reactant || '',
          reagent: s.reagent || '',
          product: s.product || '',
          reaction_type: s.reaction_type || '',
        })))
        setDifficulty(0.55)
      }
    }
    window.addEventListener('routeSelected', handler)
    return () => window.removeEventListener('routeSelected', handler)
  }, [])

  const updateStep = (index, field, value) => {
    const newSteps = [...steps]
    newSteps[index] = { ...newSteps[index], [field]: value, step_number: index + 1 }
    setSteps(newSteps)
  }

  const addStep = () => {
    if (steps.length >= 10) return
    setSteps([...steps, { ...BLANK_STEP, step_number: steps.length + 1 }])
  }

  const removeStep = (index) => {
    if (steps.length <= 1) return
    const newSteps = steps.filter((_, i) => i !== index)
    setSteps(newSteps.map((s, i) => ({ ...s, step_number: i + 1 })))
  }

  const handleSubmit = async () => {
    const validSteps = steps.filter(s => s.reactant && s.product)
    if (validSteps.length < 2) {
      alert('请至少填写2步反应')
      return
    }
    const routeData = { title: title || '合成路线', steps: validSteps }

    try {
      const enrichRes = await fetch('/api/render/enrich-route', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(routeData),
      })
      if (enrichRes.ok) {
        const enriched = await enrichRes.json()
        onGenerate(enriched, difficulty)
      } else {
        onGenerate(routeData, difficulty)
      }
    } catch {
      onGenerate(routeData, difficulty)
    }
  }

  const handleClear = () => {
    setTitle('')
    setSteps([{ ...BLANK_STEP }])
    setDifficulty(0.55)
    onReset()
  }

  const getDifficultyLabel = (val) => {
    if (val <= 0.35) return '简单'
    if (val <= 0.45) return '较易'
    if (val <= 0.55) return '中等'
    if (val <= 0.65) return '较难'
    return '困难'
  }

  return (
    <div className="card">
      <div className="card-header">
        <div className="card-title">
          <span className="card-icon">📝</span>
          合成路线输入
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <button className="btn btn-ghost btn-sm" onClick={handleClear}>
            🗑 清空
          </button>
        </div>
      </div>

      {/* 标题 */}
      <div className="form-group">
        <label className="form-label">路线标题（可选）</label>
        <input
          className="form-input"
          value={title}
          onChange={e => setTitle(e.target.value)}
          placeholder="例：芳香族化合物合成路线"
        />
      </div>

      {/* 反应步骤 */}
      <div className="form-group">
        <label className="form-label">反应步骤（{steps.length}步）</label>
        {steps.map((step, idx) => (
          <div key={idx}>
            <div className="step-card">
              <div className="step-header">
                <span className="step-number">{idx + 1}</span>
                <div className="step-actions">
                  <button
                    className="btn btn-outline btn-sm"
                    onClick={() => removeStep(idx)}
                    disabled={steps.length <= 1}
                    title="删除此步骤"
                  >
                    ✕
                  </button>
                </div>
              </div>
              <div className="step-grid">
                <div>
                  <label className="form-label">反应物</label>
                  <input
                    className="form-input"
                    value={step.reactant}
                    onChange={e => updateStep(idx, 'reactant', e.target.value)}
                    placeholder="名称或SMILES"
                  />
                  <InlineStructure name={step.reactant} size="small" showLabel={false} />
                </div>
                <div>
                  <label className="form-label">产物</label>
                  <input
                    className="form-input"
                    value={step.product}
                    onChange={e => updateStep(idx, 'product', e.target.value)}
                    placeholder="名称或SMILES"
                  />
                  <InlineStructure name={step.product} size="small" showLabel={false} />
                </div>
                <div className="full-width">
                  <label className="form-label">试剂与条件</label>
                  <input
                    className="form-input"
                    value={step.reagent}
                    onChange={e => updateStep(idx, 'reagent', e.target.value)}
                    placeholder="例：浓H₂SO₄, 170°C"
                  />
                </div>
                <div>
                  <label className="form-label">反应类型（可选）</label>
                  <select
                    className="form-select"
                    value={step.reaction_type}
                    onChange={e => updateStep(idx, 'reaction_type', e.target.value)}
                  >
                    {REACTION_TYPES.map(t => (
                      <option key={t} value={t}>{t || '-- 自动识别 --'}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
            {idx < steps.length - 1 && <div className="step-arrow">↓</div>}
          </div>
        ))}

        <button
          className="btn btn-outline btn-sm"
          onClick={addStep}
          disabled={steps.length >= 10}
          style={{ marginTop: '8px' }}
        >
          + 添加步骤
        </button>
      </div>

      {/* 合成路线图预览 */}
      {steps.filter(s => s.reactant && s.product).length >= 2 && (
        <div className="form-group">
          <label className="form-label">路线图预览</label>
          <RouteDiagram
            routeData={{ title, steps }}
            title={title || '合成路线'}
          />
        </div>
      )}

      {/* 难度调节 */}
      <div className="form-group">
        <label className="form-label">难度系数</label>
        <div className="difficulty-slider">
          <span style={{ fontSize: '12px', color: 'var(--success)' }}>简单</span>
          <input
            type="range"
            min="0.3"
            max="0.8"
            step="0.05"
            value={difficulty}
            onChange={e => setDifficulty(parseFloat(e.target.value))}
          />
          <span style={{ fontSize: '12px', color: 'var(--danger)' }}>困难</span>
          <span className="difficulty-label">
            {difficulty.toFixed(2)} ({getDifficultyLabel(difficulty)})
          </span>
        </div>
      </div>

      {/* 错误提示 */}
      {error && (
        <div className="validation-panel error" style={{ marginBottom: '12px' }}>
          ⚠ {error}
        </div>
      )}

      {/* 生成按钮 */}
      <button
        className="btn btn-primary btn-lg btn-block"
        onClick={handleSubmit}
        disabled={loading || steps.filter(s => s.reactant && s.product).length < 2}
      >
        {loading ? (
          <>
            <span className="spinner" style={{ width: '16px', height: '16px', borderWidth: '2px' }}></span>
            AI正在生成命题...
          </>
        ) : (
          <>🚀 生成命题</>
        )}
      </button>
    </div>
  )
}