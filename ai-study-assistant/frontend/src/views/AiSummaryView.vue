<script setup>
import { computed, ref } from 'vue'

import { summarizeNotes } from '@/api/ai'

// 和后端 schema 的上限保持一致
const MAX_LENGTH = 8000

const content = ref('')
const summarizing = ref(false)
const errorMessage = ref('')
// 形如 { summary: string, key_points: string[] }
const result = ref(null)

const canSubmit = computed(() => !summarizing.value && content.value.trim() !== '')

async function handleSummarize() {
  if (!canSubmit.value) {
    return
  }

  errorMessage.value = ''
  summarizing.value = true

  try {
    result.value = await summarizeNotes(content.value)
  } catch (error) {
    // 出错时保留输入框和上一次的结果，只在上方提示原因，页面不会变空
    errorMessage.value = error.message
  } finally {
    summarizing.value = false
  }
}
</script>

<template>
  <section class="ai-summary">
    <header class="ai-summary__header">
      <h2 class="ai-summary__heading">AI 笔记总结</h2>
      <p class="ai-summary__hint">
        把课程笔记、课堂内容或复习资料粘进下面的输入框，AI 会整理成总结和核心知识点
      </p>
    </header>

    <div class="ai-summary__card">
      <label class="ai-summary__label" for="summary-input">学习笔记</label>
      <textarea
        id="summary-input"
        v-model="content"
        :maxlength="MAX_LENGTH"
        rows="10"
        placeholder="例如：TCP 三次握手的过程是客户端先发送 SYN……"
        :disabled="summarizing"
      ></textarea>

      <div class="ai-summary__actions">
        <span class="ai-summary__counter">{{ content.length }} / {{ MAX_LENGTH }} 字</span>
        <button type="button" :disabled="!canSubmit" @click="handleSummarize">
          {{ summarizing ? 'AI 正在总结…' : '生成总结' }}
        </button>
      </div>
    </div>

    <p v-if="errorMessage" class="ai-summary__error">{{ errorMessage }}</p>

    <p v-if="summarizing" class="ai-summary__pending">AI 正在总结…</p>

    <template v-if="result">
      <section class="ai-summary__card">
        <h3 class="ai-summary__subheading">总结</h3>
        <p class="ai-summary__text">{{ result.summary }}</p>
      </section>

      <section class="ai-summary__card">
        <h3 class="ai-summary__subheading">核心知识点</h3>
        <ul v-if="result.key_points.length" class="ai-summary__points">
          <li v-for="(point, index) in result.key_points" :key="index">{{ point }}</li>
        </ul>
        <p v-else class="ai-summary__text ai-summary__text--muted">
          AI 这次没有返回独立的知识点条目，可以直接看上面的总结。
        </p>
      </section>
    </template>
  </section>
</template>

<style scoped>
.ai-summary__header {
  margin-bottom: 16px;
}

.ai-summary__heading {
  margin: 0;
  font-size: 20px;
}

.ai-summary__hint {
  margin: 4px 0 0;
  font-size: 13px;
  color: var(--color-muted);
}

.ai-summary__card {
  margin-bottom: 16px;
  padding: 18px;
  background-color: #fff;
  border: 1px solid var(--color-border);
  border-radius: 10px;
}

.ai-summary__label {
  display: block;
  margin-bottom: 8px;
  font-size: 14px;
  color: #374151;
}

.ai-summary__card textarea {
  width: 100%;
  padding: 10px 12px;
  font-family: inherit;
  font-size: 14px;
  line-height: 1.7;
  color: var(--color-text);
  background-color: #fff;
  border: 1px solid var(--color-border);
  border-radius: 6px;
  resize: vertical;
}

.ai-summary__card textarea:focus {
  border-color: var(--color-primary);
  outline: 2px solid #bfdbfe;
}

.ai-summary__actions {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-top: 12px;
}

.ai-summary__counter {
  font-size: 13px;
  color: var(--color-muted);
}

.ai-summary__actions button {
  padding: 9px 22px;
  font-size: 14px;
  color: #fff;
  background-color: var(--color-primary);
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.ai-summary__actions button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.ai-summary__error {
  margin: 0 0 16px;
  padding: 10px 12px;
  font-size: 14px;
  color: #b91c1c;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
}

.ai-summary__pending {
  margin: 0 0 16px;
  padding: 14px 16px;
  font-size: 14px;
  color: var(--color-muted);
  background-color: #fff;
  border: 1px dashed var(--color-border);
  border-radius: 10px;
}

.ai-summary__subheading {
  margin: 0 0 10px;
  font-size: 16px;
}

.ai-summary__text {
  margin: 0;
  font-size: 14px;
  line-height: 1.8;
  /* AI 输出的换行要保留；不使用 v-html，避免 XSS 风险 */
  white-space: pre-wrap;
  word-break: break-word;
}

.ai-summary__text--muted {
  color: var(--color-muted);
}

.ai-summary__points {
  margin: 0;
  padding-left: 20px;
  font-size: 14px;
  line-height: 1.9;
}

.ai-summary__points li {
  margin-bottom: 4px;
}
</style>
