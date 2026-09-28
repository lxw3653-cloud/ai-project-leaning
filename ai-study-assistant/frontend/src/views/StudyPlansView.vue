<script setup>
import { onMounted, ref } from 'vue'

import { deleteStudyPlan, listStudyPlans } from '@/api/studyPlans'
import StudyPlanForm from '@/components/StudyPlanForm.vue'
import StudyPlanList from '@/components/StudyPlanList.vue'

const plans = ref([])
const loading = ref(false)
const errorMessage = ref('')

// 表单是否展开，以及当前编辑的是哪一条（null 表示新建）
const formOpen = ref(false)
const editingPlan = ref(null)

// 正在等待删除确认的那一条（null 表示当前没有待确认的删除）
const deletingPlan = ref(null)

/** 拉取列表。加载失败时清空列表并显示错误，避免页面停在上一次的数据上 */
async function loadPlans() {
  loading.value = true
  errorMessage.value = ''

  try {
    plans.value = await listStudyPlans()
  } catch (error) {
    plans.value = []
    errorMessage.value = error.message
  } finally {
    loading.value = false
  }
}

function openCreateForm() {
  editingPlan.value = null
  formOpen.value = true
}

function openEditForm(plan) {
  editingPlan.value = plan
  formOpen.value = true
}

function closeForm() {
  formOpen.value = false
  editingPlan.value = null
}

/** 保存成功后收起表单并重新拉取列表，保证页面和后端一致 */
async function handleSaved() {
  closeForm()
  await loadPlans()
}

/** 点「删除」按钮时先不调接口，只记下待删除的记录，展开页面内的确认区域 */
function askDeletePlan(plan) {
  deletingPlan.value = plan
}

function cancelDelete() {
  deletingPlan.value = null
}

/** 确认删除：沿用原来的删除逻辑与错误处理 */
async function confirmDelete() {
  const plan = deletingPlan.value
  if (!plan) {
    return
  }

  errorMessage.value = ''

  try {
    await deleteStudyPlan(plan.id)

    // 如果删掉的正好是正在编辑的那一条，就把表单收起来
    if (editingPlan.value && editingPlan.value.id === plan.id) {
      closeForm()
    }

    await loadPlans()
  } catch (error) {
    if (error.status === 404) {
      // 404 表示这条记录在服务端已经不存在了，本地列表是过期数据：
      // 重新拉一次让它消失，再把原因告诉用户
      await loadPlans()
      if (!errorMessage.value) {
        errorMessage.value = '这条学习计划已经不存在了，列表已刷新'
      }
      return
    }

    // 其他错误（例如后端没启动）重新加载也拿不到数据，保留当前列表和错误提示
    errorMessage.value = error.message
  } finally {
    // 无论成功还是失败都收起确认区域，失败的原因由上方提示说明
    deletingPlan.value = null
  }
}

onMounted(loadPlans)
</script>

<template>
  <section class="study-plans">
    <header class="study-plans__header">
      <h2 class="study-plans__heading">学习计划</h2>
      <button v-if="!formOpen" type="button" class="btn-primary" @click="openCreateForm">
        新建计划
      </button>
    </header>

    <p v-if="errorMessage" class="study-plans__error">{{ errorMessage }}</p>

    <div v-if="deletingPlan" class="study-plans__confirm">
      <p class="study-plans__confirm-text">确定删除「{{ deletingPlan.title }}」？</p>
      <p class="study-plans__confirm-hint">删除后无法恢复</p>

      <div class="study-plans__confirm-actions">
        <button type="button" class="btn-secondary" @click="cancelDelete">取消</button>
        <button type="button" class="btn-danger" @click="confirmDelete">确认删除</button>
      </div>
    </div>

    <StudyPlanForm
      v-if="formOpen"
      class="study-plans__form"
      :initial-value="editingPlan"
      @saved="handleSaved"
      @cancel="closeForm"
    />

    <StudyPlanList
      class="study-plans__list"
      :plans="plans"
      :loading="loading"
      @edit="openEditForm"
      @delete="askDeletePlan"
    />
  </section>
</template>

<style scoped>
.study-plans__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 16px;
}

.study-plans__heading {
  margin: 0;
  font-size: 20px;
}

.study-plans__header .btn-primary {
  padding: 8px 18px;
  font-size: 14px;
  color: #fff;
  background-color: var(--color-primary);
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.study-plans__error {
  margin: 0 0 16px;
  padding: 10px 12px;
  font-size: 14px;
  color: #b91c1c;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
}

.study-plans__confirm {
  margin: 0 0 16px;
  padding: 16px 18px;
  background-color: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 10px;
}

.study-plans__confirm-text {
  margin: 0;
  font-size: 15px;
  font-weight: 600;
}

.study-plans__confirm-hint {
  margin: 4px 0 0;
  font-size: 13px;
  color: var(--color-muted);
}

.study-plans__confirm-actions {
  display: flex;
  gap: 8px;
  margin-top: 14px;
}

.study-plans__confirm-actions button {
  padding: 6px 16px;
  font-size: 14px;
  border-radius: 6px;
  cursor: pointer;
}

.study-plans__confirm-actions .btn-secondary {
  color: var(--color-text);
  background-color: #fff;
  border: 1px solid var(--color-border);
}

.study-plans__confirm-actions .btn-danger {
  color: #fff;
  background-color: #dc2626;
  border: 1px solid #dc2626;
}

.study-plans__form {
  margin-bottom: 20px;
}
</style>
