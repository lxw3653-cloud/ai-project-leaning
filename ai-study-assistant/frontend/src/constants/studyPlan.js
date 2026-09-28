// 学习计划的状态定义，与后端 app/models/study_plan.py 里的 StudyPlanStatus 保持一致。
// 列表显示状态、表单渲染下拉选项都从这里取，保证两处不会各写一份。

export const STUDY_PLAN_STATUSES = [
  { value: 'not_started', label: '未开始' },
  { value: 'in_progress', label: '进行中' },
  { value: 'completed', label: '已完成' },
]

export const DEFAULT_STUDY_PLAN_STATUS = 'not_started'

/**
 * 把状态值转成中文标签。
 * 万一后端出现了前端还不认识的状态，就原样返回，避免页面上出现空白。
 */
export function getStatusLabel(value) {
  const matched = STUDY_PLAN_STATUSES.find((item) => item.value === value)
  return matched ? matched.label : value
}
