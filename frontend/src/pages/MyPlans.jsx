import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, Row, Col, Empty, Spin, Button, Popconfirm, message, Tag } from 'antd'
import {
  FileTextOutlined, CalendarOutlined, EnvironmentOutlined,
  DeleteOutlined, EyeOutlined, PlusOutlined,
} from '@ant-design/icons'
import { listPlans, deletePlan } from '../services/api'
import dayjs from 'dayjs'

export default function MyPlans() {
  const navigate = useNavigate()
  const [plans, setPlans] = useState([])
  const [loading, setLoading] = useState(true)

  const fetchPlans = () => {
    setLoading(true)
    listPlans()
      .then((res) => setPlans(res.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchPlans() }, [])

  const handleDelete = async (id) => {
    try {
      await deletePlan(id)
      message.success('删除成功')
      setPlans((prev) => prev.filter((p) => p.id !== id))
    } catch {
      message.error('删除失败')
    }
  }

  if (loading) {
    return (
      <div className="text-center py-20">
        <Spin size="large" tip="加载旅行计划..." />
      </div>
    )
  }

  return (
    <div>
      {/* Header */}
      <div
        className="flex items-center justify-between mb-6 rounded-2xl"
        style={{
          background: 'linear-gradient(135deg, #ecfdf5 0%, #d1fae5 50%, #a7f3d0 100%)',
          padding: '32px 32px',
        }}
      >
        <div>
          <h1 style={{ fontSize: 26, fontWeight: 800, color: '#065f46', marginBottom: 4 }}>
            📋 我的旅行计划
          </h1>
          <p style={{ fontSize: 14, color: '#047857' }}>
            共 {plans.length} 个计划，点击查看详情
          </p>
        </div>
        <Button
          type="primary"
          size="large"
          icon={<PlusOutlined />}
          onClick={() => navigate('/')}
          style={{
            background: 'linear-gradient(135deg, #16a34a, #22c55e)',
            border: 'none',
            fontWeight: 600,
          }}
        >
          创建新计划
        </Button>
      </div>

      {plans.length === 0 ? (
        <Card style={{ borderRadius: 12, textAlign: 'center', padding: 48 }}>
          <Empty description="还没有旅行计划">
            <Button
              type="primary"
              size="large"
              icon={<PlusOutlined />}
              onClick={() => navigate('/')}
              style={{
                background: 'linear-gradient(135deg, #16a34a, #22c55e)',
                border: 'none',
              }}
            >
              开始创建
            </Button>
          </Empty>
        </Card>
      ) : (
        <Row gutter={[20, 20]}>
          {plans.map((plan) => (
            <Col xs={24} sm={12} lg={8} key={plan.id}>
              <Card
                hoverable
                style={{
                  borderRadius: 14,
                  overflow: 'hidden',
                  border: '1px solid #e5e7eb',
                  boxShadow: '0 2px 12px rgba(0,0,0,0.04)',
                  transition: 'all 0.3s',
                }}
                actions={[
                  <EyeOutlined
                    key="view"
                    style={{ color: '#16a34a' }}
                    onClick={() => navigate(`/plans/${plan.id}`)}
                  />,
                  <Popconfirm
                    key="delete"
                    title="确定删除此计划？"
                    onConfirm={() => handleDelete(plan.id)}
                    okText="确定"
                    cancelText="取消"
                  >
                    <DeleteOutlined style={{ color: '#ef4444' }} />
                  </Popconfirm>,
                ]}
              >
                <div onClick={() => navigate(`/plans/${plan.id}`)}>
                  <div
                    style={{
                      background: 'linear-gradient(135deg, #16a34a, #22c55e, #4ade80)',
                      height: 6,
                    }}
                  />
                  <div style={{ padding: '20px 20px 12px' }}>
                    <h3 style={{ fontSize: 17, fontWeight: 700, marginBottom: 12, color: '#1f2937' }}>
                      <FileTextOutlined style={{ marginRight: 8, color: '#16a34a' }} />
                      {plan.title}
                    </h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: 8, fontSize: 13, color: '#6b7280' }}>
                      <div>
                        <EnvironmentOutlined style={{ marginRight: 6 }} />
                        目的地：<Tag color="green" style={{ marginLeft: 4 }}>{plan.destination}</Tag>
                      </div>
                      <div>
                        <CalendarOutlined style={{ marginRight: 6 }} />
                        {plan.start_date} ~ {plan.end_date}
                      </div>
                      <div>
                        🕐 共 <b style={{ color: '#16a34a' }}>{plan.duration}</b> 天
                      </div>
                    </div>
                  </div>
                </div>
              </Card>
            </Col>
          ))}
        </Row>
      )}
    </div>
  )
}
