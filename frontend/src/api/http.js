/* fetch 封装：统一处理 JSON 与错误信息 */
async function request(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  })
  const body = await res.json().catch(() => null)
  if (!res.ok) {
    throw new Error(body?.detail || `请求失败（${res.status}）`)
  }
  return body
}

export const get = (path) => request(path)
export const post = (path, data) =>
  request(path, { method: "POST", body: JSON.stringify(data) })
export const patch = (path, data) =>
  request(path, { method: "PATCH", body: JSON.stringify(data) })
export const put = (path, data) =>
  request(path, { method: "PUT", body: JSON.stringify(data) })
export const del = (path) => request(path, { method: "DELETE" })
