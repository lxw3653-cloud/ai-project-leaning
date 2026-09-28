<script setup>
import { getStatusLabel } from '@/constants/studyPlan'

defineProps({
  // 父组件传进来的学习计划数组
  plans: {
    type: Array,
    required: true,
  },
  // 是否正在加载，由父组件控制
  loading: {
    type: Boolean,
    default: false,
  },
})

// 这个组件不调用接口，只把用户的操作抛给父组件
const emit = defineEmits(['edit', 'delete'])
</script>

<template>
  <div class="plan-list">
    <p v-if="loading" class="plan-list__hint">加载中…</p>

    <p v-else-if="plans.length === 0" class="plan-list__hint">
      还没有学习计划，新建之后会显示在这里。
    </p>

    <ul v-else class="plan-list__items">
      <li v-for="plan in plans" :key="plan.id" class="plan-item">
        <div class="plan-item__head">
          <h3 class="plan-item__title">{{ plan.title }}</h3>
          <span class="plan-item__status" :class="`status-${plan.status}`">
            {{ getStatusLabel(plan.status) }}
          </span>
        </div>

        <p v-if="plan.description" class="plan-item__desc">{{ plan.description }}</p>
        <p v-else class="plan-item__desc plan-item__desc--empty">暂无描述</p>

        <dl class="plan-item__dates">
          <div>
            <dt>开始</dt>
            <dd>{{ plan.start_date || '未设置' }}</dd>
          </div>
          <div>
            <dt>结束</dt>
            <dd>{{ plan.end_date || '未设置' }}</dd>
          </div>
        </dl>

        <div class="plan-item__actions">
          <button type="button" class="btn-edit" @click="emit('edit', plan)">
            编辑
          </button>
          <button type="button" class="btn-delete" @click="emit('delete', plan)">
            删除
          </button>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.plan-list__hint {
  padding: 24px;
  color: var(--color-muted);
  text-align: center;
  background-color: #fff;
  border: 1px dashed var(--color-border);
  border-radius: 10px;
}

.plan-list__items {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.plan-item {
  padding: 16px 20px;
  background-color: #fff;
  border: 1px solid var(--color-border);
  border-radius: 10px;
}

.plan-item__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.plan-item__title {
  margin: 0;
  font-size: 17px;
}

.plan-item__status {
  flex-shrink: 0;
  padding: 2px 10px;
  font-size: 12px;
  border-radius: 999px;
}

/* 三种状态各用一种底色，方便一眼区分 */
.status-not_started {
  color: #4b5563;
  background-color: #f3f4f6;
}

.status-in_progress {
  color: #1d4ed8;
  background-color: #dbeafe;
}

.status-completed {
  color: #15803d;
  background-color: #dcfce7;
}

.plan-item__desc {
  margin: 8px 0 0;
  color: #374151;
  font-size: 14px;
}

.plan-item__desc--empty {
  color: var(--color-muted);
  font-style: italic;
}

.plan-item__dates {
  display: flex;
  gap: 24px;
  margin: 12px 0 0;
  font-size: 13px;
  color: var(--color-muted);
}

.plan-item__dates div {
  display: flex;
  gap: 6px;
}

.plan-item__dates dt {
  font-weight: 600;
}

.plan-item__dates dd {
  margin: 0;
}

.plan-item__actions {
  display: flex;
  gap: 8px;
  margin-top: 14px;
}

.plan-item__actions button {
  padding: 6px 14px;
  font-size: 13px;
  background-color: #fff;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  cursor: pointer;
}

.plan-item__actions .btn-edit {
  color: var(--color-primary);
  border-color: #bfdbfe;
}

.plan-item__actions .btn-delete {
  color: #b91c1c;
  border-color: #fecaca;
}
</style>
