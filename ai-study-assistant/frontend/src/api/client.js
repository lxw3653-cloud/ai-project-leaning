// 统一的后端请求封装：以后所有接口调用都从这里走，
// 便于集中处理接口地址、错误提示以及将来加入登录凭证
const BASE_URL = import.meta.env.VITE_API_BASE_URL ?? '/api'

/**
 * 请求失败时抛出的错误。
 * 除了 message，还带上 status（HTTP 状态码）和 detail（后端原始返回），
 * 页面可以据此区分「找不到」和「参数不合法」两种情况。
 */
export class ApiError extends Error {
  constructor(message, { status = 0, detail = null } = {}) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.detail = detail
  }
}

/** 把后端返回的 detail 整理成一句能直接显示给用户的话 */
function buildErrorMessage(detail, response) {
  // 情况一：后端主动抛的 404 / 422，detail 是字符串
  if (typeof detail === 'string') {
    return detail
  }

  // 情况二：参数校验失败，detail 是数组，形如
  // [{ loc: ['body', 'title'], msg: 'String should have at least 1 character' }]
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        const field = Array.isArray(item.loc)
          ? item.loc.filter((part) => part !== 'body').join('.')
          : ''
        // Pydantic 会把自定义校验错误包成 "Value error, xxx"，这里去掉这层包装
        const message = (item.msg ?? '').replace(/^Value error,\s*/, '')
        return field ? `${field}：${message}` : message
      })
      .join('；')
  }

  // 情况三：后端没给出可读信息，退回状态码
  return `请求失败：${response.status} ${response.statusText}`
}

/** 读取响应体；没有 JSON 内容时返回 null，不让解析错误盖住真正的问题 */
async function readJson(response) {
  try {
    return await response.json()
  } catch {
    return null
  }
}

export async function request(path, { body, headers, ...options } = {}) {
  let response

  try {
    response = await fetch(`${BASE_URL}${path}`, {
      ...options,
      // 传对象时自动转成 JSON 字符串；已经是字符串或没传就原样交给 fetch
      body:
        typeof body === 'string' || body === undefined
          ? body
          : JSON.stringify(body),
      headers: {
        'Content-Type': 'application/json',
        ...(headers ?? {}),
      },
    })
  } catch {
    // fetch 自己抛错，说明请求根本没发出去：后端没启动、端口不对或断网
    throw new ApiError('无法连接后端服务，请确认后端已经启动', { status: 0 })
  }

  if (!response.ok) {
    const data = await readJson(response)
    throw new ApiError(buildErrorMessage(data?.detail, response), {
      status: response.status,
      detail: data?.detail ?? null,
    })
  }

  // 204（删除成功）没有响应体，直接返回 null
  return response.status === 204 ? null : readJson(response)
}

export function getHealth() {
  return request('/health')
}
