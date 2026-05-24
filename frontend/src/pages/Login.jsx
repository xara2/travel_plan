import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, Form, Input, Button, Tabs, message } from 'antd'
import { PhoneOutlined, MailOutlined, SendOutlined, GlobalOutlined } from '@ant-design/icons'
import { sendCode, login } from '../services/api'

export default function Login() {
  const [loading, setLoading] = useState(false)
  const [codeSent, setCodeSent] = useState(false)
  const [countdown, setCountdown] = useState(0)
  const [activeTab, setActiveTab] = useState('phone')
  const navigate = useNavigate()

  const startCountdown = () => {
    setCodeSent(true)
    let n = 60
    setCountdown(n)
    const timer = setInterval(() => {
      n -= 1
      setCountdown(n)
      if (n <= 0) {
        clearInterval(timer)
        setCodeSent(false)
      }
    }, 1000)
  }

  const handleSendCode = async (values) => {
    setLoading(true)
    try {
      const payload = activeTab === 'phone' ? { phone: values.phone } : { email: values.email }
      const res = await sendCode(payload)
      message.success(`验证码已发送 (开发模式: ${res.data.code})`)
      startCountdown()
    } catch {
      message.error('发送验证码失败')
    } finally {
      setLoading(false)
    }
  }

  const handleLogin = async (values) => {
    setLoading(true)
    try {
      const key = activeTab === 'phone' ? 'phone' : 'email'
      const res = await login({ [key]: values.identifier, code: values.code })
      localStorage.setItem('token', res.data.token)
      localStorage.setItem('user', JSON.stringify(res.data))
      message.success('登录成功')
      navigate('/')
    } catch {
      message.error('验证码错误')
    } finally {
      setLoading(false)
    }
  }

  const phoneTab = (
    <Form onFinish={handleLogin} layout="vertical" size="large">
      <Form.Item name="identifier" label="手机号" rules={[{ required: true, message: '请输入手机号' }]}>
        <Input prefix={<PhoneOutlined />} placeholder="请输入手机号" />
      </Form.Item>
      <Form.Item name="code" label="验证码" rules={[{ required: true, message: '请输入验证码' }]}>
        <Input
          prefix={<SendOutlined />}
          placeholder="请输入验证码"
          suffix={
            <Button
              type="link"
              size="small"
              loading={loading}
              disabled={codeSent}
              onClick={() => {
                const phone = document.querySelector('input[placeholder="请输入手机号"]')?.value
                if (!phone) { message.error('请先输入手机号'); return }
                handleSendCode({ phone })
              }}
            >
              {codeSent ? `${countdown}s` : '发送验证码'}
            </Button>
          }
        />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" block loading={loading}>
          登录 / 注册
        </Button>
      </Form.Item>
    </Form>
  )

  const emailTab = (
    <Form onFinish={handleLogin} layout="vertical" size="large">
      <Form.Item name="identifier" label="邮箱" rules={[{ required: true, message: '请输入邮箱' }, { type: 'email', message: '邮箱格式不正确' }]}>
        <Input prefix={<MailOutlined />} placeholder="请输入邮箱" />
      </Form.Item>
      <Form.Item name="code" label="验证码" rules={[{ required: true, message: '请输入验证码' }]}>
        <Input
          prefix={<SendOutlined />}
          placeholder="请输入验证码"
          suffix={
            <Button
              type="link"
              size="small"
              loading={loading}
              disabled={codeSent}
              onClick={() => {
                const email = document.querySelector('input[placeholder="请输入邮箱"]')?.value
                if (!email) { message.error('请先输入邮箱'); return }
                handleSendCode({ email })
              }}
            >
              {codeSent ? `${countdown}s` : '发送验证码'}
            </Button>
          }
        />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit" block loading={loading}>
          登录 / 注册
        </Button>
      </Form.Item>
    </Form>
  )

  return (
    <div
      className="flex items-center justify-center"
      style={{ minHeight: '80vh' }}
    >
      <Card
        style={{ width: 420, borderRadius: 16, boxShadow: '0 8px 40px rgba(0,0,0,0.08)' }}
        bodyStyle={{ padding: '32px' }}
      >
        <div className="text-center mb-6">
          <GlobalOutlined style={{ fontSize: 48, color: '#16a34a' }} />
          <h1 style={{ fontSize: 24, fontWeight: 700, marginTop: 12, color: '#333' }}>
            Travel Plan
          </h1>
          <p style={{ color: '#999', marginTop: 4 }}>登录后开始规划你的旅程</p>
        </div>

        <Tabs
          activeKey={activeTab}
          onChange={(key) => { setActiveTab(key); setCodeSent(false); }}
          centered
          items={[
            { key: 'phone', label: '手机号登录', children: phoneTab },
            { key: 'email', label: '邮箱登录', children: emailTab },
          ]}
        />

        <p style={{ textAlign: 'center', color: '#999', fontSize: 12, marginTop: 8 }}>
          开发模式：验证码可使用万能码 123456
        </p>
      </Card>
    </div>
  )
}
