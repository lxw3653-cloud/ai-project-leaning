// AI 相关接口封装。
// 分工和 studyPlans.js 一致：这里只负责「调哪个地址、传什么参数」。

import { request } from '@/api/client'

/**
 * 向 AI 提一个问题。
 * history 是最近几轮对话（[{ role: 'user' | 'assistant', content }]），
 * 带上它 AI 才能理解「那它和 UDP 有什么区别」这类追问。
 */
export function chatWithAi(question, history = []) {
  return request('/ai/chat', {
    method: 'POST',
    body: { question, history },
  })
}

/**
 * 把一段学习笔记交给 AI 总结。
 * 返回 { summary, key_points }，key_points 是字符串数组。
 */
export function summarizeNotes(content) {
  return request('/ai/summarize', {
    method: 'POST',
    body: { content },
  })
}
