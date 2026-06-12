import { useState } from 'react'
import { List, Button, Popconfirm, Typography, Spin } from 'antd'
import { PlusOutlined, DeleteOutlined, MessageOutlined } from '@ant-design/icons'

const { Text } = Typography

export default function ConversationList({
  conversations,
  currentId,
  onSelect,
  onNew,
  onDelete,
  loading,
}) {
  const [deleting, setDeleting] = useState(null)

  const handleDelete = async (id) => {
    setDeleting(id)
    try {
      await onDelete(id)
    } finally {
      setDeleting(null)
    }
  }

  return (
    <div className="h-full flex flex-col">
      <div className="p-3 border-b border-gray-100">
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={onNew}
          block
          style={{ background: '#22c55e', borderColor: '#22c55e' }}
        >
          新对话
        </Button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {loading ? (
          <div className="flex justify-center py-8">
            <Spin size="small" />
          </div>
        ) : conversations.length === 0 ? (
          <div className="text-center py-8 text-gray-400 text-sm">
            暂无对话记录
          </div>
        ) : (
          <List
            dataSource={conversations}
            renderItem={(item) => (
              <List.Item
                onClick={() => onSelect(item.id)}
                className={`cursor-pointer px-3 py-2 hover:bg-gray-50 transition-colors ${
                  currentId === item.id ? 'bg-green-50 border-r-2 border-green-500' : ''
                }`}
                actions={[
                  <Popconfirm
                    key="delete"
                    title="确定删除此对话？"
                    onConfirm={(e) => {
                      e.stopPropagation()
                      handleDelete(item.id)
                    }}
                    onCancel={(e) => e.stopPropagation()}
                  >
                    <Button
                      type="text"
                      size="small"
                      icon={<DeleteOutlined />}
                      loading={deleting === item.id}
                      onClick={(e) => e.stopPropagation()}
                      className="text-gray-400 hover:text-red-500"
                    />
                  </Popconfirm>,
                ]}
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <MessageOutlined className="text-gray-400 text-xs" />
                    <Text ellipsis className="text-sm" style={{ maxWidth: 160 }}>
                      {item.title || '新对话'}
                    </Text>
                  </div>
                  <div className="text-xs text-gray-400 mt-0.5">
                    {item.message_count || 0} 条消息
                  </div>
                </div>
              </List.Item>
            )}
          />
        )}
      </div>
    </div>
  )
}
