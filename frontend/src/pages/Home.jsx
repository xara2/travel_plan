import { useState, useEffect, useMemo } from 'react'
import { useNavigate } from 'react-router-dom'
import {
  Card, Input, Button, Select, DatePicker, Tag, Spin, message, Empty, Steps, Row, Col, Cascader,
  Drawer, Descriptions, Divider, TimePicker,
} from 'antd'
import {
  SearchOutlined, EnvironmentOutlined, StarOutlined, ClockCircleOutlined,
  CalendarOutlined, SendOutlined, CheckCircleOutlined,
  DollarOutlined, ExclamationCircleOutlined, ScheduleOutlined,
} from '@ant-design/icons'
import { searchAttractions, getCities, generatePlan } from '../services/api'
import dayjs from 'dayjs'

const { RangePicker } = DatePicker

export default function Home() {
  const navigate = useNavigate()
  const [provincesData, setProvincesData] = useState([])
  const [selectedCity, setSelectedCity] = useState('')
  const [selectedProvince, setSelectedProvince] = useState('')
  const [keyword, setKeyword] = useState('')
  const [attractions, setAttractions] = useState([])
  const [loading, setLoading] = useState(false)
  const [selectedIds, setSelectedIds] = useState([])
  const [dateRange, setDateRange] = useState(null)
  const [generating, setGenerating] = useState(false)
  const [currentStep, setCurrentStep] = useState(0)
  const [detailAttr, setDetailAttr] = useState(null)
  const [departTime, setDepartTime] = useState(dayjs('09:00', 'HH:mm'))

  useEffect(() => {
    getCities().then((res) => {
      const data = res.data
      if (Array.isArray(data) && data.length > 0) {
        // Province/city hierarchy
        if (data[0].province) {
          setProvincesData(data)
        } else {
          // Flat list fallback - wrap as single province
          setProvincesData([{ province: '全部', type: '', cities: data }])
        }
      }
    }).catch(() => {})
  }, [])

  // Build Cascader options: province → city
  // 直辖市可直接选择省份, 无需再选城市
  const cascaderOptions = useMemo(() => {
    return provincesData.map((p) => {
      const isMunicipality = p.type === '直辖市'
      if (isMunicipality) {
        return { label: p.province, value: p.province }
      }
      return {
        label: p.province,
        value: p.province,
        children: (p.cities || []).map((c) => ({ label: c, value: c })),
      }
    })
  }, [provincesData])

  // Track the type of selected province for display
  const selectedProvinceType = useMemo(() => {
    const p = provincesData.find((p) => p.province === selectedProvince)
    return p?.type || ''
  }, [selectedProvince, provincesData])

  // Flat city list for keyword search autocomplete
  const allCities = useMemo(() => {
    return provincesData.flatMap((p) => (p.cities || []).map((c) => ({ label: `${p.province} - ${c}`, value: c })))
  }, [provincesData])

  const handleSearch = async () => {
    if (!selectedCity && !selectedProvince && !keyword) {
      message.warning('请选择目的地或输入关键词')
      return
    }
    setLoading(true)
    try {
      const params = { keyword }
      if (selectedCity) {
        params.city = selectedCity
      }
      if (selectedProvince) {
        params.province = selectedProvince
      }
      const res = await searchAttractions(params)
      setAttractions(res.data)
      setSelectedIds([])
      setCurrentStep(1)
    } catch {
      message.error('搜索失败')
    } finally {
      setLoading(false)
    }
  }

  const toggleAttraction = (id) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id],
    )
  }

  const handleGenerate = async () => {
    if (!dateRange || selectedIds.length === 0) {
      message.warning('请选择旅行日期和至少一个景点')
      return
    }
    const [start, end] = dateRange
    const duration = end.diff(start, 'day') + 1
    if (duration < 1) {
      message.warning('结束日期不能早于开始日期')
      return
    }
    setGenerating(true)
    try {
      const res = await generatePlan({
        destination: selectedCity,
        start_date: start.format('YYYY-MM-DD'),
        end_date: end.format('YYYY-MM-DD'),
        duration,
        attraction_ids: selectedIds,
        title: `${selectedCity}${duration}日游`,
        depart_time: departTime.format('HH:mm'),
      })
      message.success('旅行计划生成成功！')
      navigate(`/plans/${res.data.id}`)
    } catch (err) {
      message.error(err.response?.data?.detail || '生成失败')
    } finally {
      setGenerating(false)
    }
  }

  const selectedAttractions = attractions.filter((a) => selectedIds.includes(a.id))

  const steps = [
    { title: '搜索目的地', icon: <SearchOutlined /> },
    { title: '选择景点', icon: <EnvironmentOutlined /> },
    { title: '设定日期', icon: <CalendarOutlined /> },
    { title: '生成计划', icon: <SendOutlined /> },
  ]

  return (
    <div>
      {/* Header Banner */}
      <div
        className="text-center mb-8 rounded-2xl"
        style={{
          background: 'linear-gradient(135deg, #ecfdf5 0%, #d1fae5 50%, #a7f3d0 100%)',
          padding: '48px 24px',
        }}
      >
        <h1 style={{ fontSize: 32, fontWeight: 800, color: '#065f46', marginBottom: 8 }}>
          🌍 开始你的旅行计划
        </h1>
        <p style={{ fontSize: 16, color: '#047857', marginBottom: 32 }}>
          选择目的地，发现精彩景点，一键生成定制行程
        </p>

        {/* Step Indicator */}
        <Steps
          current={currentStep}
          size="small"
          items={steps}
          style={{ maxWidth: 600, margin: '0 auto 32px' }}
        />

        {/* Search Bar */}
        <div className="flex gap-3 justify-center flex-wrap">
          <Cascader
            showSearch
            allowClear
            placeholder="选择目的地"
            onChange={(v) => {
              if (!v || v.length === 0) {
                setSelectedProvince('')
                setSelectedCity('')
              } else if (v.length === 1) {
                // 直辖市或仅选省份
                setSelectedProvince(v[0])
                setSelectedCity(v[0].replace('市', ''))
              } else {
                setSelectedProvince(v[0])
                setSelectedCity(v[1])
              }
              setAttractions([])
              setSelectedIds([])
            }}
            style={{ width: 220 }}
            size="large"
            options={cascaderOptions}
            suffixIcon={<EnvironmentOutlined />}
          />
          <Input
            placeholder="搜索景点名称、类型..."
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            onPressEnter={handleSearch}
            style={{ width: 300 }}
            size="large"
            prefix={<SearchOutlined />}
          />
          <Button
            type="primary"
            size="large"
            icon={<SearchOutlined />}
            onClick={handleSearch}
            loading={loading}
            style={{
              background: 'linear-gradient(135deg, #16a34a, #22c55e)',
              border: 'none',
              fontWeight: 600,
            }}
          >
            搜索景点
          </Button>
        </div>
      </div>

      {/* Attractions Grid */}
      {attractions.length > 0 && (
        <div className="mb-8">
          <h2 className="flex items-center gap-2 mb-4" style={{ fontSize: 20, fontWeight: 700, color: '#333' }}>
            <EnvironmentOutlined style={{ color: '#16a34a' }} />
            发现 {attractions.length} 个景点
            {selectedIds.length > 0 && (
              <span style={{ fontSize: 14, color: '#16a34a', fontWeight: 400 }}>
                — 已选择 {selectedIds.length} 个
              </span>
            )}
          </h2>

          <Row gutter={[16, 16]}>
            {attractions.map((attr) => {
              const selected = selectedIds.includes(attr.id)
              return (
                <Col xs={24} sm={12} md={8} lg={6} key={attr.id}>
                  <Card
                    hoverable
                    onClick={() => setDetailAttr(attr)}
                    style={{
                      borderRadius: 12,
                      overflow: 'hidden',
                      border: selected ? '2px solid #16a34a' : '1px solid #e5e7eb',
                      boxShadow: selected ? '0 4px 20px rgba(22,163,74,0.15)' : '0 2px 8px rgba(0,0,0,0.04)',
                      transition: 'all 0.3s',
                      height: '100%',
                    }}
                    cover={
                      <div style={{ position: 'relative', height: 160, overflow: 'hidden' }}>
                        <img
                          src={attr.image_url}
                          alt={attr.name}
                          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                          onError={(e) => {
                            e.target.src = `https://placehold.co/400x200/e2e8f0/94a3b8?text=${attr.name}`
                          }}
                        />
                        {selected && (
                          <div
                            style={{
                              position: 'absolute', top: 8, right: 8,
                              background: '#16a34a', color: '#fff',
                              borderRadius: '50%', width: 28, height: 28,
                              display: 'flex', alignItems: 'center', justifyContent: 'center',
                            }}
                          >
                            <CheckCircleOutlined />
                          </div>
                        )}
                      </div>
                    }
                    bodyStyle={{ padding: '12px 16px' }}
                  >
                    <h3 style={{ fontSize: 15, fontWeight: 600, marginBottom: 6 }}>{attr.name}</h3>
                    <div className="flex items-center gap-3" style={{ fontSize: 12, color: '#6b7280' }}>
                      <span><StarOutlined style={{ color: '#f59e0b' }} /> {attr.rating}</span>
                      <span><ClockCircleOutlined /> {attr.visit_duration}分钟</span>
                    </div>
                    <Tag color="green" style={{ marginTop: 8, fontSize: 11 }}>{attr.category}</Tag>
                  </Card>
                </Col>
              )
            })}
          </Row>
        </div>
      )}

      {attractions.length === 0 && !loading && currentStep >= 1 && (
        <Empty description="未找到景点，请尝试其他城市" style={{ marginTop: 24 }} />
      )}

      {loading && (
        <div className="text-center py-12">
          <Spin size="large" tip="搜索景点中..." />
        </div>
      )}

      {/* Selected & Date Section */}
      {selectedIds.length > 0 && (
        <Card
          style={{
            borderRadius: 16,
            boxShadow: '0 4px 24px rgba(0,0,0,0.06)',
            border: '1px solid #d1fae5',
          }}
        >
          <h2 className="flex items-center gap-2 mb-4" style={{ fontSize: 18, fontWeight: 700 }}>
            <CalendarOutlined style={{ color: '#16a34a' }} />
            设定旅行日期
          </h2>

          <div className="flex gap-4 flex-wrap items-end">
            <div>
              <div style={{ marginBottom: 4, fontSize: 13, color: '#6b7280' }}>选择起止日期</div>
              <RangePicker
                size="large"
                value={dateRange}
                onChange={setDateRange}
                disabledDate={(d) => d.isBefore(dayjs().startOf('day'))}
                format="YYYY-MM-DD"
                style={{ minWidth: 260 }}
              />
            </div>
            <div>
              <div style={{ marginBottom: 4, fontSize: 13, color: '#6b7280' }}>每日出发时间</div>
              <TimePicker
                size="large"
                value={departTime}
                onChange={setDepartTime}
                format="HH:mm"
                minuteStep={15}
              />
            </div>

            <div>
              <Button
                type="primary"
                size="large"
                icon={<SendOutlined />}
                onClick={handleGenerate}
                loading={generating}
                style={{
                  background: 'linear-gradient(135deg, #16a34a, #22c55e)',
                  border: 'none',
                  fontWeight: 600,
                  height: 48,
                  paddingLeft: 32,
                  paddingRight: 32,
                }}
              >
                生成旅行计划
              </Button>
            </div>
          </div>

          {dateRange && (
            <div style={{ marginTop: 16, fontSize: 13, color: '#047857' }}>
              共 {dateRange[1].diff(dateRange[0], 'day') + 1} 天
              — {dateRange[0].format('M月D日')} 至 {dateRange[1].format('M月D日')}
            </div>
          )}

          {/* Selected attractions summary */}
          <div style={{ marginTop: 20 }}>
            <div style={{ fontSize: 14, fontWeight: 600, marginBottom: 8, color: '#333' }}>
              已选景点（{selectedIds.length}个）
            </div>
            <div className="flex gap-2 flex-wrap">
              {selectedAttractions.map((a) => (
                <Tag
                  key={a.id}
                  closable
                  onClose={() => toggleAttraction(a.id)}
                  color="green"
                  style={{ padding: '2px 10px', fontSize: 13 }}
                >
                  {a.name}
                </Tag>
              ))}
            </div>
          </div>
        </Card>
      )}
      {/* Attraction Detail Drawer */}
      <Drawer
        title={detailAttr?.name}
        open={!!detailAttr}
        onClose={() => setDetailAttr(null)}
        width={420}
        extra={
          detailAttr && (
            <Button
              type="primary"
              icon={selectedIds.includes(detailAttr.id) ? <CheckCircleOutlined /> : undefined}
              onClick={() => {
                toggleAttraction(detailAttr.id)
                setDetailAttr(null)
              }}
              style={{
                background: selectedIds.includes(detailAttr.id)
                  ? '#f59e0b'
                  : 'linear-gradient(135deg, #16a34a, #22c55e)',
                border: 'none',
                fontWeight: 600,
              }}
            >
              {selectedIds.includes(detailAttr.id) ? '取消选择' : '加入旅行计划'}
            </Button>
          )
        }
      >
        {detailAttr && (
          <>
            <img
              src={detailAttr.image_url}
              alt={detailAttr.name}
              style={{ width: '100%', borderRadius: 12, marginBottom: 16 }}
              onError={(e) => {
                e.target.src = `https://placehold.co/400x200/e2e8f0/94a3b8?text=${detailAttr.name}`
              }}
            />
            <Descriptions column={1} size="small" bordered>
              <Descriptions.Item label={<><StarOutlined style={{ color: '#f59e0b' }} /> 评分</>} >
                {detailAttr.rating}
              </Descriptions.Item>
              <Descriptions.Item label={<><EnvironmentOutlined /> 分类</>} >
                <Tag color="green">{detailAttr.category}</Tag>
              </Descriptions.Item>
              <Descriptions.Item label={<><ClockCircleOutlined /> 游玩时长</>} >
                {detailAttr.visit_duration} 分钟
              </Descriptions.Item>
              <Descriptions.Item label={<><DollarOutlined style={{ color: '#16a34a' }} /> 门票</>} >
                {detailAttr.ticket_price > 0 ? `￥${detailAttr.ticket_price}` : '免费'}
              </Descriptions.Item>
              <Descriptions.Item label={<><ExclamationCircleOutlined style={{ color: detailAttr.need_reservation ? '#ef4444' : '#6b7280' }} /> 预约</>} >
                {detailAttr.need_reservation ? (
                  <Tag color="red">需要预约</Tag>
                ) : (
                  <Tag color="default">无需预约</Tag>
                )}
              </Descriptions.Item>
              <Descriptions.Item label={<><ScheduleOutlined /> 开放时间</>} >
                {detailAttr.opening_hours}
              </Descriptions.Item>
            </Descriptions>
            <Divider />
            <p style={{ color: '#4b5563', lineHeight: 1.8, fontSize: 14 }}>
              {detailAttr.description}
            </p>
          </>
        )}
      </Drawer>
    </div>
  )
}
