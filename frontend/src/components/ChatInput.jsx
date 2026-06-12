import { useState, useRef, useEffect } from 'react'
import { Input, Button } from 'antd'
import { SendOutlined } from '@ant-design/icons'

export default function ChatInput({ onSend, loading, placeholder = '输入您的问题，AI为您规划旅行...' }) {
  const [value, setValue] = useState('')
  const inputRef = useRef(null)

  useEffect(() => {
    if (!loading) {
      inputRef.current?.focus()
    }
  }, [loading])

  const handleSend = () => {
    const trimmed = value.trim()
    if (!trimmed || loading) return
    onSend(trimmed)
    setValue('')
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex gap-2 items-end p-4 border-t border-gray-100 bg-white">
      <Input.TextArea
        ref={inputRef}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        autoSize={{ minRows: 1, maxRows: 4 }}
        disabled={loading}
        className="flex-1"
      />
      <Button
        type="primary"
        icon={<SendOutlined />}
        onClick={handleSend}
        loading={loading}
        disabled={!value.trim() || loading}
        style={{ background: loading ? undefined : '#22c55e', borderColor: loading ? undefined : '#22c55e' }}
      >
        发送
      </Button>
    </div>
  )
}
