import { useNavigate, useLocation } from 'react-router-dom'
import { Button, Space, Dropdown } from 'antd'
import {
  HomeOutlined,
  FileTextOutlined,
  UserOutlined,
  LogoutOutlined,
  GlobalOutlined,
} from '@ant-design/icons'

export default function Layout({ children }) {
  const navigate = useNavigate()
  const location = useLocation()
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  if (location.pathname === '/login') return children

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    navigate('/login')
  }

  const navItems = [
    { key: '/', label: '创建计划', icon: <HomeOutlined /> },
    { key: '/my-plans', label: '我的计划', icon: <FileTextOutlined /> },
  ]

  return (
    <div className="min-h-screen flex flex-col">
      <header
        style={{
          background: 'linear-gradient(135deg, #16a34a 0%, #22c55e 50%, #4ade80 100%)',
          padding: '0 24px',
          height: 64,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          boxShadow: '0 2px 12px rgba(22,163,74,0.25)',
        }}
      >
        <div
          className="flex items-center gap-3 cursor-pointer"
          onClick={() => navigate('/')}
        >
          <GlobalOutlined style={{ fontSize: 28, color: '#fff' }} />
          <span style={{ color: '#fff', fontSize: 20, fontWeight: 700, letterSpacing: 1 }}>
            Travel Plan
          </span>
        </div>

        {token && (
          <Space size="middle">
            {navItems.map((item) => (
              <Button
                key={item.key}
                type={location.pathname === item.key ? 'default' : 'text'}
                icon={item.icon}
                onClick={() => navigate(item.key)}
                style={
                  location.pathname === item.key
                    ? { fontWeight: 600 }
                    : { color: '#fff' }
                }
              >
                {item.label}
              </Button>
            ))}
            <Dropdown
              menu={{
                items: [
                  {
                    key: 'logout',
                    icon: <LogoutOutlined />,
                    label: '退出登录',
                    onClick: handleLogout,
                  },
                ],
              }}
            >
              <Button
                type="text"
                icon={<UserOutlined />}
                style={{ color: '#fff' }}
              >
                {user.nickname || '用户'}
              </Button>
            </Dropdown>
          </Space>
        )}
      </header>

      <main className="flex-1" style={{ padding: '24px', maxWidth: 1200, margin: '0 auto', width: '100%' }}>
        {children}
      </main>
    </div>
  )
}
