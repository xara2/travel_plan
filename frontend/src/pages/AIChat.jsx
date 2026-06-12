import { useState, useEffect, useRef, useCallback } from 'react'
import { message, Modal, Input, Button } from 'antd'
import { RobotOutlined, ArrowDownOutlined } from '@ant-design/icons'
import ChatBubble from '../components/ChatBubble'
import ChatInput from '../components/ChatInput'
import ConversationList from '../components/ConversationList'
import ImageGrid from '../components/ImageGrid'
import {
  sendChat,
  listConversations,
  getConversation,
  deleteConversation,
  searchImages,
} from '../services/api'

export default function AIChat() {
  const [conversations, setConversations] = useState([])
  const [convsLoading, setConvsLoading] = useState(true)
  const [currentId, setCurrentId] = useState(null)
  const [messages, setMessages] = useState([])
  const [sending, setSending] = useState(false)
  const [msgsLoading, setMsgsLoading] = useState(false)
  const [images, setImages] = useState([])
  const [imagesLoading, setImagesLoading] = useState(false)
  const [showImageModal, setShowImageModal] = useState(false)

  const messagesEndRef = useRef(null)
  const messagesContainerRef = useRef(null)

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [])

  useEffect(() => {
    scrollToBottom()
  }, [messages, scrollToBottom])

  useEffect(() => {
    fetchConversations()
  }, [])

  const fetchConversations = async () => {
    setConvsLoading(true)
    try {
      const res = await listConversations()
      setConversations(res.data || [])
    } catch {
      message.error('加载对话列表失败')
    } finally {
      setConvsLoading(false)
    }
  }

  const fetchMessages = async (convId) => {
    setMsgsLoading(true)
    try {
      const res = await getConversation(convId)
      setMessages((res.data?.messages || []).map((m) => ({
        ...m,
        metadata: m.metadata || {},
      })))
    } catch {
      message.error('加载消息失败')
      setMessages([])
    } finally {
      setMsgsLoading(false)
    }
  }

  const handleSelect = (id) => {
    setCurrentId(id)
    fetchMessages(id)
  }

  const handleNew = () => {
    setCurrentId(null)
    setMessages([])
    setImages([])
  }

  const handleDelete = async (id) => {
    try {
      await deleteConversation(id)
      message.success('已删除')
      if (currentId === id) {
        setCurrentId(null)
        setMessages([])
      }
      fetchConversations()
    } catch {
      message.error('删除失败')
    }
  }

  const handleSend = async (text) => {
    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: text,
      metadata: {},
      created_at: new Date().toISOString(),
    }
    setMessages((prev) => [...prev, userMsg])
    setSending(true)

    try {
      const res = await sendChat({
        conversation_id: currentId || undefined,
        message: text,
      })

      if (!currentId) {
        setCurrentId(res.data.conversation_id)
        fetchConversations()
      }

      const assistantMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        content: res.data.message,
        metadata: {
          tool_calls: res.data.tool_calls || [],
          attractions_found: res.data.attractions_found || [],
        },
        created_at: new Date().toISOString(),
      }
      setMessages((prev) => [...prev, assistantMsg])

      // If images were found, show them
      if (res.data.attractions_found?.length > 0) {
        handleImageSearch(res.data.attractions_found[0], text)
      }
    } catch (err) {
      message.error(err.response?.data?.detail || '发送失败，请重试')
    } finally {
      setSending(false)
    }
  }

  const handleImageSearch = async (query, destination) => {
    setImagesLoading(true)
    try {
      const res = await searchImages({ query, destination, count: 6 })
      if (res.data?.length > 0) {
        setImages(res.data)
      }
    } catch {
      // Non-critical, skip
    } finally {
      setImagesLoading(false)
    }
  }

  return (
    <div className="flex h-[calc(100vh-112px)] -m-6">
      {/* Left Sidebar */}
      <div className="w-[260px] flex-shrink-0 bg-white border-r border-gray-100">
        <ConversationList
          conversations={conversations}
          currentId={currentId}
          onSelect={handleSelect}
          onNew={handleNew}
          onDelete={handleDelete}
          loading={convsLoading}
        />
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col bg-gray-50">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 bg-white border-b border-gray-100">
          <div className="flex items-center gap-2">
            <RobotOutlined style={{ fontSize: 20, color: '#22c55e' }} />
            <span className="font-semibold text-gray-800">
              {currentId
                ? conversations.find((c) => c.id === currentId)?.title || '旅行助手'
                : 'AI 旅行助手'}
            </span>
          </div>
          {images.length > 0 && (
            <Button size="small" onClick={() => setShowImageModal(true)}>
              查看图片 ({images.length})
            </Button>
          )}
        </div>

        {/* Messages */}
        <div
          ref={messagesContainerRef}
          className="flex-1 overflow-y-auto px-4 py-6"
        >
          {msgsLoading ? (
            <div className="flex justify-center py-12">
              <div className="text-gray-400">加载消息中...</div>
            </div>
          ) : messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-gray-400">
              <RobotOutlined style={{ fontSize: 48, marginBottom: 16 }} />
              <p className="text-lg mb-2">您好！我是您的AI旅行助手</p>
              <p className="text-sm">我可以帮您搜索景点、规划行程、查找图片</p>
              <div className="mt-6 space-y-2">
                {[
                  '推荐北京适合亲子的景点',
                  '帮我规划一个3天的杭州旅行',
                  '看看黄山的风景照片',
                ].map((suggestion) => (
                  <div
                    key={suggestion}
                    className="px-4 py-2 bg-white rounded-lg border border-gray-100 cursor-pointer hover:border-green-300 hover:bg-green-50 transition-colors text-sm text-gray-600"
                    onClick={() => handleSend(suggestion)}
                  >
                    {suggestion}
                  </div>
                ))}
              </div>
            </div>
          ) : (
            messages.map((msg) => (
              <ChatBubble key={msg.id} message={msg} />
            ))
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Scroll to bottom button */}
        {messages.length > 4 && (
          <div className="flex justify-center -mt-2 mb-1">
            <Button
              size="small"
              shape="circle"
              icon={<ArrowDownOutlined />}
              onClick={scrollToBottom}
              className="shadow"
            />
          </div>
        )}

        {/* Input */}
        <ChatInput onSend={handleSend} loading={sending} />
      </div>

      {/* Image Modal */}
      <Modal
        title="相关图片"
        open={showImageModal}
        onCancel={() => setShowImageModal(false)}
        footer={null}
        width={640}
      >
        <ImageGrid images={images} loading={imagesLoading} />
      </Modal>
    </div>
  )
}
