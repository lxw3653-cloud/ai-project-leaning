// 统一的后端请求封装：以后所有接口调用都从这里走，
// 便于集中处理接口地址、错误提示以及将来加入登录凭证
const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api'

export async function request(path, { headers, ...options } = {}) {
  const response = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(headers ?? {}),
    },
  })

  if (!response.ok) {
    throw new Error(`请求失败：${response.status} ${response.statusText}`)
  }

  return response.status === 204 ? null : response.json()
}

export function getHealth() {
  return request('/health')
}
