<script setup>
import { computed, reactive, ref, watch } from 'vue'

import { createStudyPlan, updateStudyPlan } from '@/api/studyPlans'
import { DEFAULT_STUDY_PLAN_STATUS, STUDY_PLAN_STATUSES } from '@/constants/studyPlan'

const props = defineProps({
  // null 表示新建；传入计划对象表示编辑，并会用它回填表单
  initialValue: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['saved', 'cancel'])

const isEditing = computed(() => props.initialValue !== null)

// 表单自己的副本：用户改的是这里，不动父组件传进来的对象，
// 这样点「取消」时不会污染原来的数据
const form = reactive({
  title: '',
  description: '',
  status: DEFAULT_STUDY_PLAN_STATUS,
  start_date: '',
  end_date: '',
})

const submitting = ref(false)
const errorMessage = ref('')

/** 把传进来的计划对象复制到表单；传 null 时恢复成空白表单 */
function applyInitialValue(value) {
  form.title = value?.title ?? ''
  form.description = value?.description ?? ''
  form.status = value?.status ?? DEFAULT_STUDY_PLAN_STATUS
  form.start_date = value?.start_date ?? ''
  form.end_date = value?.end_date ?? ''
  errorMessage.value = ''
}

// immediate 让首次挂载也执行一次；父组件切换 initialValue 时表单会自动跟着变
watch(() => props.initialValue, applyInitialValue, { immediate: true })

/** 空字符串要转成 null：日期字段传 "" 会被后端当成格式错误 */
function toNullable(value) {
  const trimmed = value.trim()
  return trimmed === '' ? null : trimmed
}

async function handleSubmit() {
  errorMessage.value = ''

  const title = form.title.trim()
  if (title === '') {
    errorMessage.value = '标题不能为空'
    return
  }

  if (form.start_date && form.end_date && form.end_date < form.start_date) {
    errorMessage.value = '结束日期不能早于开始日期'
    return
  }

  const payload = {
    title,
    description: toNullable(form.description),
    status: form.status,
    start_date: toNullable(form.start_date),
    end_date: toNullable(form.end_date),
  }

  submitting.value = true

  try {
    const savedPlan = isEditing.value
      ? await updateStudyPlan(props.initialValue.id, payload)
      : await createStudyPlan(payload)

    emit('saved', savedPlan)
  } catch (error) {
    // client.js 已经把后端的 detail 整理成可读文案，这里直接显示
    errorMessage.value = error.message
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <form class="plan-form" @submit.prevent="handleSubmit">
    <h2 class="plan-form__title">
      {{ isEditing ? '编辑学习计划' : '新建学习计划' }}
    </h2>

    <div class="plan-form__field">
      <label for="plan-title">标题 <span class="plan-form__required">*</span></label>
      <input
        id="plan-title"
        v-model="form.title"
        type="text"
        maxlength="200"
        placeholder="例如：背完 300 个单词"
      />
    </div>

    <div class="plan-form__field">
      <label for="plan-description">描述</label>
      <textarea
        id="plan-description"
        v-model="form.description"
        rows="3"
        placeholder="补充说明，可留空"
      ></textarea>
    </div>

    <div class="plan-form__field">
      <label for="plan-status">状态</label>
      <select id="plan-status" v-model="form.status">
        <option v-for="item in STUDY_PLAN_STATUSES" :key="item.value" :value="item.value">
          {{ item.label }}
        </option>
      </select>
    </div>

    <div class="plan-form__dates">
      <div class="plan-form__field">
        <label for="plan-start">开始日期</label>
        <input id="plan-start" v-model="form.start_date" type="date" />
      </div>

      <div class="plan-form__field">
        <label for="plan-end">结束日期</label>
        <input id="plan-end" v-model="form.end_date" type="date" />
      </div>
    </div>

    <p v-if="errorMessage" class="plan-form__error">{{ errorMessage }}</p>

    <div class="plan-form__actions">
      <button type="submit" class="btn-primary" :disabled="submitting">
        {{ submitting ? '保存中…' : isEditing ? '保存修改' : '创建计划' }}
      </button>
      <button
        type="button"
        class="btn-secondary"
        :disabled="submitting"
        @click="emit('cancel')"
      >
        取消
      </button>
    </div>
  </form>
</template>

<style scoped>
.plan-form {
  max-width: 720px;
  padding: 24px;
  background-color: #fff;
  border: 1px solid var(--color-border);
  border-radius: 10px;
}

.plan-form__title {
  margin: 0 0 16px;
  font-size: 18px;
}

.plan-form__field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 14px;
}

.plan-form__field label {
  font-size: 14px;
  color: #374151;
}

.plan-form__required {
  color: #b91c1c;
}

.plan-form__field input,
.plan-form__field textarea,
.plan-form__field select {
  padding: 8px 10px;
  font-family: inherit;
  font-size: 14px;
  color: var(--color-text);
  background-color: #fff;
  border: 1px solid var(--color-border);
  border-radius: 6px;
}

.plan-form__field textarea {
  resize: vertical;
}

.plan-form__field input:focus,
.plan-form__field textarea:focus,
.plan-form__field select:focus {
  border-color: var(--color-primary);
  outline: 2px solid #bfdbfe;
}

.plan-form__dates {
  display: flex;
  gap: 16px;
}

.plan-form__dates .plan-form__field {
  flex: 1;
}

.plan-form__error {
  margin: 0 0 14px;
  padding: 10px 12px;
  font-size: 14px;
  color: #b91c1c;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
}

.plan-form__actions {
  display: flex;
  gap: 8px;
}

.plan-form__actions button {
  padding: 8px 18px;
  font-size: 14px;
  border: 1px solid transparent;
  border-radius: 6px;
  cursor: pointer;
}

.plan-form__actions .btn-primary {
  color: #fff;
  background-color: var(--color-primary);
}

.plan-form__actions .btn-secondary {
  color: var(--color-text);
  background-color: #fff;
  border-color: var(--color-border);
}

.plan-form__actions button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
