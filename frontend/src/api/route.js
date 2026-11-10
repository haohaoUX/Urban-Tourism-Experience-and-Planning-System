import { del, get, patch, post, put } from "./http"

export const createRoute = (payload) => post("/api/routes", payload)
export const fetchRoutes = () => get("/api/routes")
export const fetchRoute = (id) => get(`/api/routes/${id}`)
export const renameRoute = (id, name) =>
  patch(`/api/routes/${id}`, { name })
export const updateRouteItems = (id, items) =>
  put(`/api/routes/${id}/items`, { items })
export const copyRoute = (id) => post(`/api/routes/${id}/copy`, {})
export const deleteRoute = (id) => del(`/api/routes/${id}`)
