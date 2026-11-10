import { get } from "./http"

export function fetchPois(params = {}) {
  const query = new URLSearchParams(
    Object.entries(params).filter(([, v]) => v !== "" && v != null)
  ).toString()
  return get(`/api/pois${query ? `?${query}` : ""}`)
}

export const fetchPoi = (id) => get(`/api/pois/${id}`)

export const fetchNearby = (id, radius = 500) =>
  get(`/api/pois/${id}/nearby?radius=${radius}`)
