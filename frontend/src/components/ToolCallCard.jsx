import { Collapse, Tag, Spin } from 'antd'
import { ToolOutlined, CheckCircleOutlined, LoadingOutlined } from '@ant-design/icons'

export default function ToolCallCard({ toolCalls }) {
  if (!toolCalls || toolCalls.length === 0) return null

  return (
    <div className="mb-2">
      {toolCalls.map((tc, i) => (
        <Collapse
          key={i}
          size="small"
          ghost
          className="mb-1"
          items={[{
            key: `tool-${i}`,
            label: (
              <span className="text-xs text-gray-500">
                <ToolOutlined className="mr-1" />
                {tc.tool}
                {tc.status === 'running' ? (
                  <Spin indicator={<LoadingOutlined />} size="small" className="ml-2" />
                ) : (
                  <CheckCircleOutlined className="ml-2 text-green-500" />
                )}
              </span>
            ),
            children: (
              <div className="text-xs">
                {tc.input && (
                  <div className="mb-1">
                    <Tag color="blue" className="text-xs">输入</Tag>
                    <pre className="bg-gray-50 p-2 rounded mt-0.5 overflow-x-auto">
                      {typeof tc.input === 'string' ? tc.input : JSON.stringify(tc.input, null, 2)}
                    </pre>
                  </div>
                )}
                {tc.output && (
                  <div>
                    <Tag color="green" className="text-xs">输出</Tag>
                    <pre className="bg-gray-50 p-2 rounded mt-0.5 overflow-x-auto max-h-32">
                      {typeof tc.output === 'string' ? tc.output : JSON.stringify(tc.output, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            ),
          }]}
        />
      ))}
    </div>
  )
}
