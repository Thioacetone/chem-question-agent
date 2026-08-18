import { useState } from 'react'
import ROUTE_LIBRARY from '../data/routeLibrary.js'
import InlineStructure from './InlineStructure.jsx'

/**
 * 路线库页面 — 独立的全屏路线选择界面
 * 用户打开网站首先看到此页面，选择路线后进入输入页
 */
export default function RouteLibraryPage({ onRouteSelect }) {
  const [hoveredId, setHoveredId] = useState(null)
  const [filter, setFilter] = useState('all')

  const filteredRoutes = filter === 'all'
    ? ROUTE_LIBRARY
    : ROUTE_LIBRARY.filter(r => r.steps.length === parseInt(filter))

  // 动态计算步数分布
  const stepCounts = [...new Set(ROUTE_LIBRARY.map(r => r.steps.length))].sort()
  const counts = {}
  stepCounts.forEach(n => {
    counts[n] = ROUTE_LIBRARY.filter(r => r.steps.length === n).length
  })

  return (
    <div className="route-library-page">
      {/* 顶部标题区 */}
      <div className="library-hero">
        <h1>合成路线库</h1>
        <p>共 {ROUTE_LIBRARY.length} 条合成路线，涵盖经典人名反应与多样化起始原料，点击选中即可开始命题</p>
      </div>

      {/* 步数筛选 */}
      <div className="library-filters">
        <button
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
          onClick={() => setFilter('all')}
        >
          全部（{ROUTE_LIBRARY.length}）
        </button>
        {stepCounts.map(n => (
          <button
            key={n}
            className={`filter-btn ${filter === String(n) ? 'active' : ''}`}
            onClick={() => setFilter(String(n))}
          >
            {n}步（{counts[n]}）
          </button>
        ))}
      </div>

      {/* 路线卡片网格 */}
      <div className="library-grid">
        {filteredRoutes.map(route => (
          <div
            key={route.id}
            className={`library-card ${hoveredId === route.id ? 'hovered' : ''}`}
            onClick={() => onRouteSelect(route)}
            onMouseEnter={() => setHoveredId(route.id)}
            onMouseLeave={() => setHoveredId(null)}
          >
            <div className="library-card-header">
              <div style={{ flex: 1, minWidth: 0 }}>
                <span className={`step-badge step-${route.steps.length}`}>
                  {route.steps.length}步
                </span>
                <span className="route-title">{route.title}</span>
              </div>
              <div className="library-card-structure">
                <InlineStructure
                  name={route.steps[route.steps.length - 1].product}
                  size="small"
                  showLabel={false}
                  lazy={true}
                />
              </div>
            </div>
            <div className="library-card-body">
              <div className="route-path">
                <span className="path-start">{route.steps[0].reactant}</span>
                <span className="path-arrow">→</span>
                <span className="path-end">{route.steps[route.steps.length - 1].product}</span>
              </div>
              <div className="route-desc">{route.desc}</div>
            </div>
            <div className="library-card-footer">
              <span className="select-hint">点击选择此路线 →</span>
            </div>
          </div>
        ))}
      </div>

      {/* 底部 */}
      <div className="library-footer">
        <p>路线库持续更新中，如需更多路线请联系管理员</p>
      </div>
    </div>
  )
}