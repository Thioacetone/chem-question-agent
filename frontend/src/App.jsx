import { useState, useEffect, useCallback, useRef } from 'react'
import RouteInput from './components/RouteInput.jsx'
import QuestionPreview from './components/QuestionPreview.jsx'
import RouteLibraryPage from './components/RouteLibraryPage.jsx'
import StructureViewer from './components/StructureViewer.jsx'

const NAV_ITEMS = [
  { id: 'library', icon: '📚', label: '路线库', section: '开始' },
  { id: 'input', icon: '📝', label: '合成路线输入', section: '工作区' },
  { id: 'preview', icon: '📋', label: '命题预览', section: '工作区', badge: true },
  { id: 'viewer', icon: '🔬', label: '结构式查看器', section: '工具' },
  { id: 'about', icon: 'ℹ️', label: '关于本站', section: '其他' },
]

const BREADCRUMB_MAP = {
  library: '路线库',
  input: '合成路线输入',
  preview: '命题预览',
  viewer: '结构式查看器',
  about: '关于本站',
}

export default function App() {
  const [apiStatus, setApiStatus] = useState('checking')
  const [activeTab, setActiveTab] = useState('library')
  const [questionData, setQuestionData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [loadingMsg, setLoadingMsg] = useState('')
  const [error, setError] = useState(null)
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const loadingTimerRef = useRef(null)

  useEffect(() => {
    checkApiStatus()
  }, [])

  const checkApiStatus = async () => {
    try {
      const res = await fetch('/api/health')
      if (res.ok) {
        const data = await res.json()
        setApiStatus(data.deepseek_api === '已配置' ? 'online' : 'offline')
      } else {
        setApiStatus('offline')
      }
    } catch {
      setApiStatus('offline')
    }
  }

  const handleGenerate = async (routeData, difficulty) => {
    setLoading(true)
    setLoadingMsg('正在调用AI生成命题...')
    setError(null)
    
    // 计时器：每5秒更新等待提示
    let elapsed = 0
    if (loadingTimerRef.current) clearInterval(loadingTimerRef.current)
    loadingTimerRef.current = setInterval(() => {
      elapsed += 5
      if (elapsed <= 30) {
        setLoadingMsg(`AI正在深度思考命题中...（已等待${elapsed}秒）`)
      } else if (elapsed <= 60) {
        setLoadingMsg(`AI正在精心设计每道小题...（已等待${elapsed}秒，请耐心等待）`)
      } else {
        setLoadingMsg(`AI正在校验答案格式...（已等待${elapsed}秒，推理模型较慢）`)
      }
    }, 5000)
    
    try {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), 300000) // 5分钟超时
      
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ route: routeData, difficulty }),
        signal: controller.signal,
      })
      clearTimeout(timeoutId)
      
      if (!res.ok) {
        const errData = await res.json().catch(() => ({}))
        const detail = errData.detail
        if (Array.isArray(detail)) {
          // FastAPI 422 验证错误
          const msgs = detail.map(d => `${d.msg} (${d.loc.join('.')})`).join('; ')
          throw new Error(`请求数据格式错误: ${msgs}`)
        }
        throw new Error(detail || `生成失败 (HTTP ${res.status})`)
      }
      const data = await res.json()
      setQuestionData(data)
      setActiveTab('preview')
    } catch (e) {
      if (e.name === 'AbortError') {
        setError('AI生成超时（超过5分钟），请重试或简化合成路线')
      } else {
        setError(e.message)
      }
    } finally {
      if (loadingTimerRef.current) {
        clearInterval(loadingTimerRef.current)
        loadingTimerRef.current = null
      }
      setLoading(false)
      setLoadingMsg('')
    }
  }

  const handleRefine = async (feedback) => {
    if (!questionData) return
    setLoading(true)
    setError(null)
    try {
      const res = await fetch('/api/refine', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question_data: questionData, feedback }),
      })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.detail || '优化失败')
      }
      const data = await res.json()
      setQuestionData(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleExport = async (includeAnswer) => {
    if (!questionData) return
    try {
      const res = await fetch(`/api/export/docx?include_answer=${includeAnswer}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(questionData),
      })
      if (!res.ok) throw new Error('导出失败')
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = includeAnswer ? '化学命题_教师版.docx' : '化学命题_学生版.docx'
      a.click()
      URL.revokeObjectURL(url)
    } catch (e) {
      setError(e.message)
    }
  }

  const handleReset = () => {
    setQuestionData(null)
    setActiveTab('library')
    setError(null)
  }

  const handleRouteSelectFromLibrary = (route) => {
    // 将路线库选中的路线数据传递给 RouteInput
    setActiveTab('input')
    // 用 setTimeout 确保 RouteInput 已挂载
    setTimeout(() => {
      window.__selectedRoute = route
      window.dispatchEvent(new CustomEvent('routeSelected', { detail: route }))
    }, 0)
  }

  const handleNavClick = (id) => {
    if (id === 'preview' && !questionData) return
    setActiveTab(id)
    setSidebarOpen(false)
  }

  const sectionGroups = {}
  NAV_ITEMS.forEach(item => {
    if (!sectionGroups[item.section]) sectionGroups[item.section] = []
    sectionGroups[item.section].push(item)
  })

  return (
    <div className="app-layout">
      {/* 移动端覆盖层 */}
      <div className={`sidebar-overlay ${sidebarOpen ? 'open' : ''}`} onClick={() => setSidebarOpen(false)} />

      {/* 侧边栏 */}
      <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`}>
        <div className="sidebar-brand">
          <span className="brand-icon">⚗</span>
          <h2>高考有机化学<br/>命题助手</h2>
          <div className="brand-subtitle">v2.1 · AI-Powered</div>
        </div>

        <nav className="sidebar-nav">
          {Object.entries(sectionGroups).map(([section, items]) => (
            <div key={section}>
              <div className="nav-section-title">{section}</div>
              {items.map(item => (
                <button
                  key={item.id}
                  className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
                  onClick={() => handleNavClick(item.id)}
                  disabled={item.id === 'preview' && !questionData}
                >
                  <span className="nav-icon">{item.icon}</span>
                  {item.label}
                  {item.badge && questionData && (
                    <span className="nav-badge">NEW</span>
                  )}
                </button>
              ))}
            </div>
          ))}

          <div className="nav-divider" />

          <div className="nav-section-title">快捷操作</div>
          <button className="nav-item" onClick={handleReset}>
            <span className="nav-icon">🔄</span>
            重置命题
          </button>
          {questionData && (
            <>
              <button className="nav-item" onClick={() => handleExport(true)}>
                <span className="nav-icon">📥</span>
                导出教师版
              </button>
              <button className="nav-item" onClick={() => handleExport(false)}>
                <span className="nav-icon">📤</span>
                导出学生版
              </button>
            </>
          )}
        </nav>

        <div className="sidebar-footer">
          <div className="security-badge">
            <span className="ssl-icon">🔒</span>
            <span>SSL 安全连接</span>
          </div>
          <div className="security-info">
            <div className="security-row">
              <span className={`status-dot ${apiStatus}`} />
              {apiStatus === 'online' ? 'DeepSeek 已连接' : apiStatus === 'checking' ? '检查连接中...' : 'API 未连接'}
            </div>
            <div className="security-row" style={{ marginTop: '6px', fontSize: '10px', color: 'rgba(255,255,255,0.35)', lineHeight: '1.5' }}>
              数据加密传输 · 不存储命题内容<br />
              网页由硫代丙酮制作
            </div>
          </div>
        </div>
      </aside>

      {/* 主内容区 */}
      <div className="main-area">
        {/* 顶部栏 */}
        <header className="topbar">
          <div className="topbar-breadcrumb">
            <button className="mobile-menu-btn" onClick={() => setSidebarOpen(!sidebarOpen)}>
              ☰
            </button>
            <span>命题助手</span>
            <span className="sep">›</span>
            <span className="current">{BREADCRUMB_MAP[activeTab]}</span>
          </div>
          <div className="topbar-actions">
            <span className="badge badge-secure" title="全站HTTPS加密，数据安全传输">
              🔒 安全连接
            </span>
            {error && (
              <span className="badge badge-warning" style={{ cursor: 'pointer' }} onClick={() => setError(null)}>
                ⚠ {error}
              </span>
            )}
            {activeTab === 'preview' && questionData && (
              <span className="badge badge-primary">
                {questionData.questions?.length || 5}题 · {questionData.questions?.reduce((s, q) => s + (q.score || 0), 0) || 15}分
              </span>
            )}
          </div>
        </header>

        {/* 内容区 */}
        <div className="content-container">
          {/* 页面标题 */}
          <div className="page-header">
            <h1>{BREADCRUMB_MAP[activeTab]}</h1>
            <p>
              {activeTab === 'library' && '选择一条合成路线作为命题基础，AI 将基于该路线创作原创高考化学命题'}
              {activeTab === 'input' && '确认或修改合成路线，调整难度，AI 将基于路线创作原创高考化学命题'}
              {activeTab === 'preview' && '查看生成的命题，支持教师修改意见优化和导出 Word 文档'}
              {activeTab === 'viewer' && '输入化合物名称或 SMILES，查看对应的化学结构式'}
            </p>
          </div>

          {/* 路线库页 */}
          {activeTab === 'library' && (
            <div className="animate-fade-up">
              <RouteLibraryPage onRouteSelect={handleRouteSelectFromLibrary} />
            </div>
          )}

          {/* 输入页 */}
          {activeTab === 'input' && (
            <div className="animate-fade-up">
              <RouteInput
                onGenerate={handleGenerate}
                loading={loading}
                error={error}
                onReset={handleReset}
              />
            </div>
          )}

          {/* 智能识别页 */}
          {activeTab === 'smart' && (
            <div className="animate-fade-up">
              <SmartParse
                onRouteParsed={handleRouteParsed}
                onGenerate={handleGenerate}
                loading={loading}
                setLoading={setLoading}
                setError={setError}
              />
            </div>
          )}

          {/* 命题预览页 */}
          {activeTab === 'preview' && questionData && (
            <div className="animate-fade-up">
              <QuestionPreview
                data={questionData}
                onRefine={handleRefine}
                onExport={handleExport}
                loading={loading}
                error={error}
              />
            </div>
          )}

          {/* 结构式查看器 */}
          {activeTab === 'viewer' && (
            <div className="animate-fade-up">
              <StructureViewer />
            </div>
          )}

          {/* 关于本站 */}
          {activeTab === 'about' && (
            <div className="animate-fade-up">
              <div className="about-page">
                <div className="about-section">
                  <h3>平台简介</h3>
                  <p>
                    本平台是一款基于人工智能技术的高考有机化学原创命题辅助工具。
                    依托DeepSeek大语言模型，结合200+条精选合成路线库，
                    能够自动生成符合高考命题规范的原创化学试题，涵盖官能团识别、
                    结构推断、反应条件选择、同分异构体分析、合成路线设计等核心题型。
                  </p>
                </div>

                <div className="about-section">
                  <h3>技术架构</h3>
                  <div className="tech-stack">
                    <div className="tech-item">
                      <span className="tech-label">AI模型</span>
                      <span className="tech-value">DeepSeek 大语言模型</span>
                    </div>
                    <div className="tech-item">
                      <span className="tech-label">结构渲染</span>
                      <span className="tech-value">RDKit + ChemDraw 风格</span>
                    </div>
                    <div className="tech-item">
                      <span className="tech-label">后端框架</span>
                      <span className="tech-value">FastAPI (Python)</span>
                    </div>
                    <div className="tech-item">
                      <span className="tech-label">前端框架</span>
                      <span className="tech-value">React + Vite</span>
                    </div>
                    <div className="tech-item">
                      <span className="tech-label">部署平台</span>
                      <span className="tech-value">Railway (云端24小时运行)</span>
                    </div>
                    <div className="tech-item">
                      <span className="tech-label">数据传输</span>
                      <span className="tech-value">全站 HTTPS 加密</span>
                    </div>
                  </div>
                </div>

                <div className="about-section">
                  <h3>使用声明</h3>
                  <ul className="disclaimer-list">
                    <li>本平台仅供教学参考和命题辅助使用，生成内容需经教师审核后使用。</li>
                    <li>AI生成的命题可能存在不完善之处，建议结合实际教学需求进行调整。</li>
                    <li>所有命题数据在生成后不会存储在服务器中，保障用户隐私安全。</li>
                    <li>合成路线库中的路线来源于公开的有机化学教材和文献资料。</li>
                    <li>本平台为非商业性质的教育工具，免费提供给教师和学生使用。</li>
                  </ul>
                </div>
              </div>
            </div>
          )}

          {/* 加载状态 */}
          {loading && (
            <div className="loading">
              <div className="spinner" />
              <p>{loadingMsg || 'AI 正在创作命题，请稍候...'}</p>
              <p style={{ fontSize: '11px', color: '#999', marginTop: '4px' }}>
                AI正在创作命题，通常需要30-90秒，请耐心等待
              </p>
            </div>
          )}
        </div>

        {/* 底部资质栏 */}
        <footer className="site-footer">
          <div className="footer-content">
            <div className="footer-left">
              <span className="footer-brand">高考有机化学命题助手 v2.1</span>
              <span className="footer-sep">|</span>
              <span>基于 DeepSeek AI 驱动</span>
            </div>
            <div className="footer-right">
              <span>© 2026 硫代丙酮 · 版权所有</span>
              <span className="footer-sep">|</span>
              <span>内容仅供教学参考，请以教材为准</span>
            </div>
          </div>
        </footer>
      </div>
    </div>
  )
}