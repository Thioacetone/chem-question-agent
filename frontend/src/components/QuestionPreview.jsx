import { useState } from 'react'
import RichTextRenderer from './RichTextRenderer.jsx'
import RouteDiagram from './RouteDiagram.jsx'
import SynthesisAnswerRoute, { parseAnswerRoute } from './SynthesisAnswerRoute.jsx'

export default function QuestionPreview({ data, onRefine, onExport, loading, error }) {
  const [feedback, setFeedback] = useState('')
  const [showRefine, setShowRefine] = useState(false)

  if (!data) return null

  const { target_compound, stem, questions, answers, analysis, new_info, estimated_difficulty, validation, raw_route } = data

  const totalScore = questions?.reduce((sum, q) => sum + (q.score || 0), 0) || 15

  const difficultyLabel = (d) => {
    if (d <= 0.35) return '简单'
    if (d <= 0.45) return '较易'
    if (d <= 0.55) return '中等'
    if (d <= 0.65) return '较难'
    return '困难'
  }

  return (
    <div>
      <div className="card" style={{ marginBottom: '16px' }}>
        <div className="card-header">
          <div className="card-title">
            <span className="card-icon">📋</span>
            命题预览
          </div>
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            {estimated_difficulty && (
              <span className="badge badge-primary">
                难度: {typeof estimated_difficulty === 'number' ? estimated_difficulty.toFixed(2) : estimated_difficulty} ({difficultyLabel(typeof estimated_difficulty === 'number' ? estimated_difficulty : 0.55)})
              </span>
            )}
            <span className="badge badge-accent">
              {totalScore}分 / {questions?.length || 5}题
            </span>
          </div>
        </div>

      {/* 试卷样式预览 — 仿照真题排版 */}
      <div style={{
        padding: '24px 20px',
        background: '#fff',
        borderRadius: 'var(--radius)',
        border: '1px solid var(--border)',
        fontFamily: '"SimSun", "宋体", "PingFang SC", "Microsoft YaHei", serif',
        fontSize: '15px',
        lineHeight: '2',
        color: '#000',
      }}>

        {/* 题干 */}
        {stem && (
          <div style={{ marginBottom: '16px', textIndent: '2em' }}>
            <RichTextRenderer text={stem} structureSize="small" />
          </div>
        )}

        {/* 新信息（如果有） */}
        {new_info && (
          <div style={{
            marginBottom: '16px',
            padding: '8px 0',
            fontSize: '13px',
            lineHeight: '1.8',
          }}>
            <RichTextRenderer text={new_info} structureSize="small" />
          </div>
        )}

        {/* 合成路线图 */}
        {raw_route && raw_route.steps && raw_route.steps.length >= 2 && (
          <div style={{ marginBottom: '16px' }}>
            <RouteDiagram
              routeData={raw_route}
              title=""
            />
          </div>
        )}

        {/* 小题 — 仿照真题 (1)(2)(3)(4)(5) 格式 */}
        {questions?.map((q, i) => {
          const isIsomer = (q.type || '').includes('同分异构')

          return (
            <div key={i} style={{ marginBottom: '12px' }}>
              {/* 小题正文 */}
              <div style={{ textIndent: '2em', marginBottom: isIsomer ? '4px' : '0' }}>
                <span style={{ fontWeight: 600 }}>（{q.number || i + 1}）</span>
                <RichTextRenderer text={q.content} structureSize="small" />
              </div>

              
            </div>
          )
        })}
      </div>
      </div>

      {/* 各题分值明细 */}
      <div style={{
        marginTop: '12px',
        display: 'flex',
        gap: '8px',
        flexWrap: 'wrap',
        fontSize: '12px',
        color: 'var(--text-secondary)',
      }}>
        {questions?.map((q, i) => (
          <span key={i} className={`badge ${q.difficulty === 'easy' ? 'badge-success' : q.difficulty === 'hard' ? 'badge-warning' : 'badge-primary'}`}>
            ({q.number || i+1}) {q.type || '?'} · {q.score || '?'}分
          </span>
        ))}
      </div>

      {/* 答案 */}
      {answers?.length > 0 && (
        <div className="card">
          <div className="card-header">
            <div className="card-title">
              <span className="card-icon">✅</span>
              参考答案
            </div>
          </div>
          {answers.map((a, i) => {
            const isRouteAnswer = (a.number === 5 || a.number === '5') && a.content
            const hasRouteDiagram = isRouteAnswer && parseAnswerRoute(a.content)
            return (
            <div key={i} style={{ marginBottom: '8px' }}>
              <div style={{ fontWeight: 600 }}>（{a.number || i + 1}）</div>
              {hasRouteDiagram ? (
                <SynthesisAnswerRoute answerText={a.content} />
              ) : (
                <div style={{ textIndent: '2em' }}>
                  <RichTextRenderer text={a.content} structureSize="small" routeData={raw_route} />
                </div>
              )}
              {a.scoring_points?.length > 0 && (
                <div style={{ marginTop: '4px', fontSize: '12px', color: 'var(--success)', textIndent: '2em' }}>
                  {a.scoring_points.map((sp, j) => (
                    <div key={j}>踩分点：{sp}</div>
                  ))}
                </div>
              )}
            </div>
          )})}
        </div>
      )}

      {/* 解析 */}
      {analysis && (
        <div className="card">
          <div className="card-header">
            <div className="card-title">
              <span className="card-icon">💡</span>
              详细解析
            </div>
          </div>
          <div style={{ fontSize: '14px', lineHeight: '1.8', padding: '0 8px' }}>
            <RichTextRenderer text={analysis} structureSize="small" routeData={raw_route} />
          </div>
        </div>
      )}

      {/* 验证结果 */}
      {validation && (
        <div className={`validation-panel ${validation.is_valid ? 'valid' : 'error'}`} style={{ marginTop: '16px' }}>
          <strong>{validation.is_valid ? '命题质量检查通过' : '命题质量检查发现问题'}</strong>
          {validation.issues?.map((issue, i) => (
            <div key={i} style={{ color: 'var(--danger)' }}>{issue}</div>
          ))}
          {validation.warnings?.map((w, i) => (
            <div key={i} style={{ color: 'var(--warning)' }}>建议：{w}</div>
          ))}
        </div>
      )}

      {/* 错误提示 */}
      {error && (
        <div className="validation-panel error" style={{ marginTop: '12px' }}>
          {error}
        </div>
      )}

      {/* 教师修改 */}
      <div className="form-group" style={{ marginTop: '20px' }}>
        <button
          className="btn btn-outline btn-sm"
          onClick={() => setShowRefine(!showRefine)}
        >
          {showRefine ? '收起修改' : '教师修改意见'}
        </button>
        {showRefine && (
          <div style={{ marginTop: '10px' }}>
            <textarea
              className="form-textarea"
              rows={3}
              value={feedback}
              onChange={e => setFeedback(e.target.value)}
              placeholder="输入修改意见，例如：第(4)题同分异构体条件太简单，请增加手性碳限制..."
            />
            <button
              className="btn btn-primary btn-sm"
              style={{ marginTop: '8px' }}
              onClick={() => {
                if (feedback.trim()) {
                  onRefine(feedback)
                  setFeedback('')
                  setShowRefine(false)
                }
              }}
              disabled={loading || !feedback.trim()}
            >
              {loading ? '优化中...' : '提交优化'}
            </button>
          </div>
        )}
      </div>

      {/* 导出按钮 */}
      <div className="export-actions">
        <button
          className="btn btn-success btn-sm"
          onClick={() => onExport(true)}
        >
          导出教师版Word（含解析）
        </button>
        <button
          className="btn btn-outline btn-sm"
          onClick={() => onExport(false)}
        >
          导出学生版Word（无解析）
        </button>
      </div>
    </div>
  )
}