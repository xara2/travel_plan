import { Image, Empty } from 'antd'

export default function ImageGrid({ images, loading }) {
  if (loading) {
    return (
      <div className="grid grid-cols-2 gap-2">
        {Array.from({ length: 4 }).map((_, i) => (
          <div key={i} className="aspect-[4/3] bg-gray-100 rounded-lg animate-pulse" />
        ))}
      </div>
    )
  }

  if (!images || images.length === 0) {
    return <Empty description="暂无图片" image={Empty.PRESENTED_IMAGE_SIMPLE} />
  }

  return (
    <div className="grid grid-cols-2 gap-2">
      {images.map((img, i) => (
        <Image
          key={i}
          src={img.thumbnail_url || img.url}
          alt={img.alt_text || '景点图片'}
          className="rounded-lg object-cover aspect-[4/3]"
          fallback="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='150'%3E%3Crect fill='%23f0f0f0' width='200' height='150'/%3E%3Ctext x='50%25' y='50%25' text-anchor='middle' dy='.3em' fill='%23aaa' font-size='14'%3E%E6%97%A0%E5%9B%BE%E7%89%87%3C/text%3E%3C/svg%3E"
          style={{ width: '100%' }}
          preview={{ mask: '查看大图' }}
        />
      ))}
    </div>
  )
}
