// 学习计划相关的接口封装。
// 这里只负责「调哪个地址、传什么参数」，不处理页面状态。

import { request } from '@/api/client'

const BASE_PATH = '/study-plans'

/** 查询全部学习计划（后端按创建时间倒序返回） */
export function listStudyPlans() {
  return request(BASE_PATH)
}

/** 查询单个学习计划，id 不存在时后端返回 404 */
export function getStudyPlan(planId) {
  return request(`${BASE_PATH}/${planId}`)
}

/** 创建学习计划，成功返回 201 和新记录 */
export function createStudyPlan(payload) {
  return request(BASE_PATH, { method: 'POST', body: payload })
}

/** 局部更新学习计划，payload 里只放要改的字段 */
export function updateStudyPlan(planId, payload) {
  return request(`${BASE_PATH}/${planId}`, { method: 'PATCH', body: payload })
}

/** 删除学习计划，成功返回 204，没有响应体 */
export function deleteStudyPlan(planId) {
  return request(`${BASE_PATH}/${planId}`, { method: 'DELETE' })
}
