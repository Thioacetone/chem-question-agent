import { useState, useEffect } from 'react'
import RouteDiagram from './RouteDiagram.jsx'
import QuestionPreview from './QuestionPreview.jsx'

/**
 * 题库页面 — 展示结构简式推断题题库
 */
export default function QuestionBankPage({ onSelectQuestion }) {
  const [questions, setQuestions] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedQuestion, setSelectedQuestion] = useState(null)
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)
  const [total, setTotal] = useState(0)
  const PAGE_SIZE = 6

  useEffect(() => {
    loadQuestions(page)
  }, [page])

  const loadQuestions = async (p) => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`/api/questions/structure-inference?page=${p}&page_size=${PAGE_SIZE}`)
      if (!res.ok) throw new Error('加载题库失败')
      const data = await res.json()
      setQuestions(data.questions || [])
      setTotalPages(data.total_pages || 1)
      setTotal(data.total || 0)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleViewQuestion = (q, idx) => {
    setSelectedQuestion({ ...q, _index: (page - 1) * PAGE_SIZE + idx })
  }

  const handleBack = () => {
    setSelectedQuestion(null)
  }

  const handleUseQuestion = (q) => {
    if (onSelectQuestion) {
      onSelectQuestion(q)
    }
  }

  if (selectedQuestion) {
    return (
      <div className="question-bank-detail">
        <div className="qb-detail-header">
          <button className="btn-back" onClick={handleBack}>← 返回题库</button>
          <button className="btn-primary" onClick={() => handleUseQuestion(selectedQuestion)}>
            使用此题
          </button>
        </div>
        <QuestionPreview data={selectedQuestion} />
      </div>
    )
  }

  if (loading) {
    return (
      <div className="question-bank-loading">
        <div className="spinner" />
        <p>加载题库中...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="question-bank-error">
        <p>加载失败: {error}</p>
        <button className="btn-primary" onClick={() => loadQuestions(page)}>重试</button>
      </div>
    )
  }

  return (
    <div className="question-bank-page">
      <div className="qb-header">
        <h2>结构简式推断题题库</h2>
        <p>共 {total} 道题目，每道题包含结构推断、同分异构体、有机合成等题型</p>
      </div>

      <div className="qb-grid">
        {questions.map((q, idx) => {
          const warnings = q._warnings || []
          const hasWarnings = warnings.length > 0
          return (
            <div
              key={q.route_id || idx}
              className={`qb-card ${hasWarnings ? 'has-warnings' : ''}`}
              onClick={() => handleViewQuestion(q, idx)}
            >
              <div className="qb-card-header">
                <span className="qb-card-index">#{(page - 1) * PAGE_SIZE + idx + 1}</span>
                <span className="qb-card-title">{q.target_compound || q.route_title}</span>
                {hasWarnings && <span className="qb-card-warning" title={warnings.join('\n')}>⚠</span>}
              </div>
              <div className="qb-card-stem">
                {q.stem}
              </div>
              <div className="qb-card-meta">
                <span className="qb-tag">结构推断: {q.hidden_structure}</span>
                <span className="qb-tag">{q.route_steps}步路线</span>
                <span className="qb-tag">{q.questions?.length || 5}题 · {q.questions?.reduce((s, q) => s + (q.score || 0), 0) || 15}分</span>
              </div>
              <div className="qb-card-questions">
                {q.questions?.slice(0, 3).map((qst, i) => (
                  <div key={i} className="qb-card-q">
                    <span className="qb-q-num">({qst.number})</span>
                    <span className="qb-q-text">{qst.content?.substring(0, 60)}{qst.content?.length > 60 ? '...' : ''}</span>
                  </div>
                ))}
                {q.questions?.length > 3 && (
                  <div className="qb-card-q more">... 还有 {q.questions.length - 3} 道小题</div>
                )}
              </div>
            </div>
          )
        })}
      </div>

      {totalPages > 1 && (
        <div className="qb-pagination">
          <button
            className="btn-page"
            disabled={page <= 1}
            onClick={() => setPage(p => Math.max(1, p - 1))}
          >
            ← 上一页
          </button>
          <span className="qb-page-info">
            {page} / {totalPages}
          </span>
          <button
            className="btn-page"
            disabled={page >= totalPages}
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
          >
            下一页 →
          </button>
        </div>
      )}
    </div>
  )
}