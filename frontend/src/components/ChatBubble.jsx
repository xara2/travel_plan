import ReactMarkdown from 'react-markdown'
import { Avatar, Collapse, Tag } from 'antd'
import { UserOutlined, RobotOutlined, ToolOutlined } from '@ant-design/icons'

export default function ChatBubble({ message }) {
  const isUser = message.role === 'user'
  const toolCalls = message.metadata?.tool_calls || []

  return (
    <div
      className={`flex gap-3 mb-4 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}
    >
      <Avatar
        icon={isUser ? <UserOutlined /> : <RobotOutlined />}
        style={{
          backgroundColor: isUser ? '#22c55e' : '#3b82f6',
          flexShrink: 0,
        }}
      />

      <div className={`max-w-[75%] ${isUser ? 'items-end' : 'items-start'}`}>
        {toolCalls.length > 0 && (
          <Collapse
            size="small"
            ghost
            items={[{
              key: 'tools',
              label: (
                <span className="text-xs text-gray-400">
                  <ToolOutlined className="mr-1" />
                  工具调用 ({toolCalls.length})
                </span>
              ),
              children: toolCalls.map((tc, i) => (
                <div key={i} className="mb-2 text-xs">
                  <Tag color="blue">{tc.tool}</Tag>
                  <pre className="bg-gray-50 p-2 rounded mt-1 text-xs overflow-x-auto">
                    {tc.observation?.slice(0, 300)}
                  </pre>
                </div>
              )),
            }]}
            className="mb-1"
          />
        )}

        <div
          className={`rounded-xl px-4 py-2.5 text-sm leading-relaxed ${
            isUser
              ? 'bg-green-500 text-white rounded-tr-sm'
              : 'bg-white border border-gray-100 shadow-sm rounded-tl-sm'
          }`}
        >
          {isUser ? (
            <p className="whitespace-pre-wrap m-0">{message.content}</p>
          ) : (
            <div className="prose prose-sm max-w-none prose-headings:text-gray-800 prose-p:text-gray-700 prose-strong:text-gray-900 prose-li:text-gray-700 [&_pre]:bg-gray-50 [&_pre]:rounded [&_pre]:p-2 [&_pre]:text-xs [&_code]:text-xs">
              <ReactMarkdown>{message.content}</ReactMarkdown>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
