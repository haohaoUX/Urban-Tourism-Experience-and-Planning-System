/* 模拟地图投影：把 GCJ-02 经纬度线性映射为画布百分比坐标 */
const BOUNDS = {
  minLng: 115.74,
  maxLng: 116.02,
  minLat: 28.57,
  maxLat: 28.73,
}

export function project(lng, lat) {
  const x =
    ((lng - BOUNDS.minLng) / (BOUNDS.maxLng - BOUNDS.minLng)) * 100
  const y =
    (1 - (lat - BOUNDS.minLat) / (BOUNDS.maxLat - BOUNDS.minLat)) * 100
  return { x, y }
}
