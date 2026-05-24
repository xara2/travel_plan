import { useEffect, useRef } from 'react'

export default function MapView({ markers = [], height = '400px' }) {
  const mapRef = useRef(null)
  const mapInstance = useRef(null)

  useEffect(() => {
    if (!mapRef.current || mapInstance.current) return

    mapInstance.current = new AMap.Map(mapRef.current, {
      zoom: 5,
      center: [104.0, 35.0],
    })

    return () => {
      if (mapInstance.current) {
        mapInstance.current.destroy()
        mapInstance.current = null
      }
    }
  }, [])

  useEffect(() => {
    if (!mapInstance.current || markers.length === 0) return

    mapInstance.current.clearMap()
    const path = []

    markers.forEach((marker, idx) => {
      if (marker.lng && marker.lat) {
        const position = [marker.lng, marker.lat]
        path.push(position)

        const content =
          `<div style="background:#16a34a;color:#fff;padding:4px 10px;border-radius:14px;font-size:12px;white-space:nowrap;box-shadow:0 2px 6px rgba(0,0,0,0.15)">${idx + 1}. ${marker.name}</div>`

        const m = new AMap.Marker({
          position,
          content,
          offset: new AMap.Pixel(-15, -15),
          zIndex: 100 + markers.length - idx,
        })
        mapInstance.current.add(m)

        if (marker.description) {
          m.setTitle(marker.description)
          m.on('click', () => {
            const info = new AMap.InfoWindow({
              content: `<div style="padding:8px"><b>${marker.name}</b><p style="margin:4px 0 0;font-size:12px;color:#666">${marker.description}</p></div>`,
              offset: new AMap.Pixel(0, -30),
            })
            info.open(mapInstance.current, position)
          })
        }
      }
    })

    if (path.length > 1) {
      const polyline = new AMap.Polyline({
        path,
        strokeColor: '#16a34a',
        strokeWeight: 4,
        strokeDasharray: [10, 6],
        strokeOpacity: 0.8,
      })
      mapInstance.current.add(polyline)
    }

    if (path.length > 0) {
      mapInstance.current.setFitView(null, false, [60, 60, 60, 60])
    }
  }, [markers])

  return <div ref={mapRef} style={{ height, width: '100%', borderRadius: 12 }} />
}
