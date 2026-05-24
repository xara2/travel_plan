import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { Card, Spin, Timeline, Tag, Empty, Drawer, Image, Button, Descriptions, Collapse, Badge } from 'antd'
import {
  EnvironmentOutlined, ClockCircleOutlined, StarOutlined,
  ArrowLeftOutlined, CalendarOutlined, CarOutlined,
  DollarOutlined, ExclamationCircleOutlined, ScheduleOutlined,
  CompassOutlined,
} from '@ant-design/icons'
import { getPlan, getRouteOptions } from '../services/api'
import MapView from '../components/MapView'
import dayjs from 'dayjs'

const TIME_SLOT_COLORS = { '上午': '#f59e0b', '下午': '#16a34a', '傍晚': '#8b5cf6' }

export default function PlanDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [plan, setPlan] = useState(null)
  const [loading, setLoading] = useState(true)
  const [drawerVisible, setDrawerVisible] = useState(false)
  const [selectedAttraction, setSelectedAttraction] = useState(null)
  const [routeMap, setRouteMap] = useState({})
  const [routesLoading, setRoutesLoading] = useState(false)

  useEffect(() => {
    getPlan(id)
      .then((res) => {
        setPlan(res.data)
        // Fetch route options between consecutive attractions
        fetchAllRoutes(res.data)
      })
      .catch(() => navigate('/'))
      .finally(() => setLoading(false))
  }, [id])

  const fetchAllRoutes = async (planData) => {
    const allAttractions = []
    planData.days.forEach((day) => {
      day.items.forEach((item) => {
        if (item.attraction?.lat && item.attraction?.lng) {
          allAttractions.push(item.attraction)
        }
      })
    })
    if (allAttractions.length < 2) return

    setRoutesLoading(true)
    const map = {}
    for (let i = 0; i < allAttractions.length - 1; i++) {
      const from = allAttractions[i]
      const to = allAttractions[i + 1]
      const key = `${from.id}-${to.id}`
      try {
        const res = await getRouteOptions({
          origin_lng: from.lng,
          origin_lat: from.lat,
          dest_lng: to.lng,
          dest_lat: to.lat,
        })
        map[key] = res.data.routes
      } catch {
        map[key] = []
      }
    }
    setRouteMap(map)
    setRoutesLoading(false)
  }

  if (loading) {
    return (
      <div className="text-center py-20">
        <Spin size="large" tip="加载旅行计划..." />
      </div>
    )
  }

  if (!plan) return <Empty description="计划不存在" />

  // Collect all markers for the map
  const allMarkers = []
  plan.days.forEach((day) => {
    day.items.forEach((item) => {
      if (item.attraction) {
        allMarkers.push({
          lat: item.attraction.lat,
          lng: item.attraction.lng,
          name: item.attraction.name,
          label: `${day.day_number}日 ${item.time_slot}: ${item.attraction.name}`,
          description: item.attraction.description?.slice(0, 60) || '',
        })
      }
    })
  })

  return (
    <div>
      {/* Back & Title */}
      <div className="flex items-center gap-4 mb-6">
        <Button
          icon={<ArrowLeftOutlined />}
          onClick={() => navigate('/my-plans')}
          type="text"
          size="large"
        />
        <div>
          <h1 style={{ fontSize: 24, fontWeight: 700, color: '#065f46' }}>
            {plan.title}
          </h1>
          <span style={{ color: '#6b7280', fontSize: 14 }}>
            <CalendarOutlined /> {plan.start_date} 至 {plan.end_date} · 共 {plan.duration} 天
          </span>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 24, flexWrap: 'wrap' }}>
        {/* Timeline Section */}
        <div style={{ flex: '1 1 450px', minWidth: 0 }}>
          {plan.days.map((day) => (
            <Card
              key={day.id}
              title={
                <span style={{ fontSize: 17, fontWeight: 700 }}>
                  📅 第 {day.day_number} 天 — {day.date}
                </span>
              }
              style={{
                marginBottom: 20,
                borderRadius: 12,
                border: '1px solid #d1fae5',
                boxShadow: '0 2px 12px rgba(0,0,0,0.04)',
              }}
              headStyle={{ borderBottom: '2px solid #d1fae5' }}
            >
              {day.items.length === 0 ? (
                <Empty description="暂无安排" />
              ) : (
                <Timeline
                  items={day.items.flatMap((item, idx) => {
                    const attractionCard = {
                      color: TIME_SLOT_COLORS[item.time_slot] || '#16a34a',
                      dot: <span style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        width: 24, height: 24,
                        borderRadius: '50%',
                        background: TIME_SLOT_COLORS[item.time_slot] || '#16a34a',
                        color: '#fff',
                        fontSize: 12,
                        fontWeight: 700,
                      }}>{idx + 1}</span>,
                      children: item.attraction ? (
                        <div
                          style={{
                            cursor: 'pointer',
                            padding: '8px 12px',
                            borderRadius: 8,
                            background: '#f9fafb',
                            transition: 'all 0.2s',
                          }}
                          onClick={() => {
                            setSelectedAttraction(item.attraction)
                            setDrawerVisible(true)
                          }}
                          onMouseEnter={(e) => e.currentTarget.style.background = '#ecfdf5'}
                          onMouseLeave={(e) => e.currentTarget.style.background = '#f9fafb'}
                        >
                          <div style={{ fontWeight: 600, fontSize: 15, marginBottom: 4 }}>
                            {item.attraction.name}
                            {item.attraction.need_reservation && (
                              <Tag color="red" style={{ marginLeft: 8, fontSize: 10 }}>需预约</Tag>
                            )}
                          </div>
                          <div style={{ fontSize: 12, color: '#6b7280', marginBottom: 4 }}>
                            <Tag color={TIME_SLOT_COLORS[item.time_slot]} style={{ fontSize: 11 }}>
                              {item.time_slot}
                            </Tag>
                            <ClockCircleOutlined /> {item.attraction.visit_duration}分钟
                            <StarOutlined style={{ color: '#f59e0b', marginLeft: 8 }} /> {item.attraction.rating}
                            <DollarOutlined style={{ marginLeft: 8 }} />
                            {item.attraction.ticket_price > 0 ? `￥${item.attraction.ticket_price}` : '免费'}
                          </div>
                          <div style={{ fontSize: 13, color: '#4b5563', lineHeight: 1.5 }}>
                            {item.attraction.description?.slice(0, 80)}...
                          </div>
                          <div style={{ fontSize: 11, color: '#16a34a', marginTop: 4 }}>
                            点击查看详情 →
                          </div>
                        </div>
                      ) : (
                        <span>景点信息已失效</span>
                      ),
                    }

                    // Check if there's a next item (same day or next day)
                    const nextItem = (() => {
                      const nextInDay = day.items[idx + 1]
                      if (nextInDay?.attraction) return { item: nextInDay, key: `${item.attraction?.id}-day${day.day_number}-${idx}` }
                      const nextDay = plan.days.find(d => d.day_number === day.day_number + 1)
                      if (nextDay?.items?.[0]?.attraction) return { item: nextDay.items[0], key: `${item.attraction?.id}-day${day.day_number}-x` }
                      return null
                    })()

                    const routeKey = nextItem && item.attraction && nextItem.item.attraction
                      ? `${item.attraction.id}-${nextItem.item.attraction.id}`
                      : null
                    const routes = routeKey ? routeMap[routeKey] : null

                    if (!nextItem) return [attractionCard]

                    return [
                      attractionCard,
                      {
                        color: 'gray',
                        dot: <CompassOutlined style={{ fontSize: 14, color: '#6b7280' }} />,
                        children: (
                          <div style={{
                            padding: '6px 10px', borderRadius: 6,
                            background: '#f0fdf4', border: '1px dashed #86efac',
                            fontSize: 12,
                          }}>
                            <span style={{ color: '#6b7280' }}>
                              ↓ 前往 <strong>{nextItem.item.attraction?.name}</strong>
                            </span>
                            {routesLoading && !routes && (
                              <Spin size="small" style={{ marginLeft: 8 }} />
                            )}
                            {routes && routes.length > 0 && (
                              <div style={{ marginTop: 4, display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                                {routes.map((r, ri) => (
                                  <Tag key={ri} color="blue" style={{ fontSize: 11, margin: 0 }}>
                                    {r.type}: {r.desc}
                                  </Tag>
                                ))}
                              </div>
                            )}
                          </div>
                        ),
                      },
                    ]
                  })}
                />
              )}
            </Card>
          ))}
        </div>

        {/* Map Section */}
        <div style={{ flex: '1 1 400px', minWidth: 0 }}>
          <Card
            title={
              <span style={{ fontWeight: 700, fontSize: 16 }}>
                <EnvironmentOutlined style={{ color: '#16a34a' }} /> 路线地图
              </span>
            }
            style={{
              borderRadius: 12,
              position: 'sticky',
              top: 24,
              border: '1px solid #d1fae5',
              boxShadow: '0 2px 12px rgba(0,0,0,0.04)',
            }}
            bodyStyle={{ padding: 12 }}
          >
            {allMarkers.length > 0 ? (
              <>
                <MapView markers={allMarkers} height="400px" />
                <div style={{ marginTop: 12 }}>
                  <div style={{ fontWeight: 600, fontSize: 14, marginBottom: 8 }}>路线概览</div>
                  {allMarkers.map((m, i) => (
                    <div key={i} style={{ fontSize: 12, color: '#6b7280', marginBottom: 4 }}>
                      {i + 1}. {m.name}
                      {i < allMarkers.length - 1 && (
                        <span style={{ color: '#16a34a', margin: '0 4px' }}>→</span>
                      )}
                    </div>
                  ))}
                </div>
              </>
            ) : (
              <Empty description="暂无路线信息" />
            )}
          </Card>
        </div>
      </div>

      {/* Attraction Detail Drawer */}
      <Drawer
        title={selectedAttraction?.name}
        open={drawerVisible}
        onClose={() => setDrawerVisible(false)}
        width={480}
        bodyStyle={{ padding: 0 }}
      >
        {selectedAttraction && (
          <div>
            <Image
              src={selectedAttraction.image_url}
              alt={selectedAttraction.name}
              style={{ width: '100%', maxHeight: 300, objectFit: 'cover' }}
              fallback={`https://placehold.co/600x300/e2e8f0/94a3b8?text=${selectedAttraction.name}`}
            />
            <div style={{ padding: 24 }}>
              <Descriptions column={1} size="small" bordered>
                <Descriptions.Item label="城市">{selectedAttraction.city}</Descriptions.Item>
                <Descriptions.Item label="分类">
                  <Tag color="green">{selectedAttraction.category}</Tag>
                </Descriptions.Item>
                <Descriptions.Item label="评分">
                  <StarOutlined style={{ color: '#f59e0b' }} /> {selectedAttraction.rating}
                </Descriptions.Item>
                <Descriptions.Item label="游玩时长">
                  {selectedAttraction.visit_duration} 分钟
                </Descriptions.Item>
                <Descriptions.Item label={<><DollarOutlined style={{ color: '#16a34a' }} /> 门票</>}>
                  {selectedAttraction.ticket_price > 0
                    ? `￥${selectedAttraction.ticket_price}`
                    : '免费'}
                </Descriptions.Item>
                <Descriptions.Item label={<><ExclamationCircleOutlined /> 预约</>}>
                  {selectedAttraction.need_reservation ? (
                    <Tag color="red">需要预约</Tag>
                  ) : (
                    <Tag color="default">无需预约</Tag>
                  )}
                </Descriptions.Item>
                <Descriptions.Item label={<><ScheduleOutlined /> 开放时间</>}>
                  {selectedAttraction.opening_hours || '暂无'}
                </Descriptions.Item>
              </Descriptions>
              <div style={{ marginTop: 16 }}>
                <div style={{ fontWeight: 600, marginBottom: 8 }}>详细介绍</div>
                <p style={{ lineHeight: 1.8, color: '#4b5563' }}>
                  {selectedAttraction.description}
                </p>
              </div>
            </div>
          </div>
        )}
      </Drawer>
    </div>
  )
}
