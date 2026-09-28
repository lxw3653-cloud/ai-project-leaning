<script setup>
import { nextTick, ref } from 'vue'

import { chatWithAi } from '@/api/ai'

// 每次最多带上最近 10 条历史，和后端的上限保持一致
const MAX_HISTORY = 10

// messages 里每一项形如 { id, role: 'user' | 'assistant', content }
const messages = ref([])
const question = ref('')
const sending = ref(false)
const errorMessage = ref('')

const listRef = ref(null)
let nextMessageId = 1

/** 新消息进来后滚到底部，不然用户看不到最新一条 */
async function scrollToBottom() {
  await nextTick()
  if (listRef.value) {
    listRef.value.scrollTop = listRef.value.scrollHeight
  }
}

async function handleSend() {
  const text = question.value.trim()
  if (text === '' || sending.value) {
    return
  }

  errorMessage.value = ''
  messages.value.push({ id: nextMessageId++, role: 'user', content: text })
  question.value = ''
  sending.value = true
  await scrollToBottom()

  // 只把「发送之前」的对话当作历史；当前问题单独走 question 字段，避免重复发送
  const history = messages.value
    .slice(0, -1)
    .slice(-MAX_HISTORY)
    .map(({ role, content }) => ({ role, content }))

  try {
    const data = await chatWithAi(text, history)
    messages.value.push({ id: nextMessageId++, role: 'assistant', content: data.answer })
  } catch (error) {
    // client.js 已经把后端返回的 detail（例如 Key 无效）整理成可读文案
    errorMessage.value = error.message
  } finally {
    sending.value = false
    await scrollToBottom()
  }
}
</script>

<template>
  <section class="ai-chat">
    <header class="ai-chat__header">
      <h2 class="ai-chat__heading">AI 聊天助手</h2>
      <p class="ai-chat__hint">输入学习问题，AI 会在几秒内作答，也可以连续追问</p>
    </header>

    <div ref="listRef" class="ai-chat__messages">
      <p v-if="messages.length === 0 && !sending" class="ai-chat__empty">
        还没有对话。试着问一个，例如「解释一下 TCP 三次握手」。
      </p>

      <div
        v-for="message in messages"
        :key="message.id"
        class="ai-chat__message"
        :class="message.role === 'user' ? 'is-user' : 'is-assistant'"
      >
        <span class="ai-chat__role">{{ message.role === 'user' ? '我' : 'AI' }}</span>
        <p class="ai-chat__text">{{ message.content }}</p>
      </div>

      <div v-if="sending" class="ai-chat__message is-assistant">
        <span class="ai-chat__role">AI</span>
        <p class="ai-chat__text ai-chat__text--pending">正在思考…</p>
      </div>
    </div>

    <p v-if="errorMessage" class="ai-chat__error">{{ errorMessage }}</p>

    <form class="ai-chat__input" @submit.prevent="handleSend">
      <input
        v-model="question"
        type="text"
        maxlength="2000"
        placeholder="输入你的问题，按回车发送"
        :disabled="sending"
      />
      <button type="submit" :disabled="sending || question.trim() === ''">
        {{ sending ? '发送中…' : '发送' }}
      </button>
    </form>
  </section>
</template>

<style scoped>
.ai-chat__header {
  margin-bottom: 16px;
}

.ai-chat__heading {
  margin: 0;
  font-size: 20px;
}

.ai-chat__hint {
  margin: 4px 0 0;
  font-size: 13px;
  color: var(--color-muted);
}

.ai-chat__messages {
  display: flex;
  flex-direction: column;
  gap: 12px;
  height: 420px;
  padding: 16px;
  overflow-y: auto;
  background-color: #fff;
  border: 1px solid var(--color-border);
  border-radius: 10px;
}

.ai-chat__empty {
  margin: auto;
  color: var(--color-muted);
  font-size: 14px;
}

.ai-chat__message {
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-width: 80%;
}

.ai-chat__message.is-user {
  align-self: flex-end;
  align-items: flex-end;
}

.ai-chat__message.is-assistant {
  align-self: flex-start;
}

.ai-chat__role {
  font-size: 12px;
  color: var(--color-muted);
}

.ai-chat__text {
  margin: 0;
  padding: 10px 14px;
  font-size: 14px;
  line-height: 1.7;
  /* AI 的回答里有换行，用 pre-wrap 保留格式；不用 v-html，避免 XSS 风险 */
  white-space: pre-wrap;
  word-break: break-word;
  border-radius: 10px;
}

.is-user .ai-chat__text {
  color: #fff;
  background-color: var(--color-primary);
}

.is-assistant .ai-chat__text {
  color: var(--color-text);
  background-color: #f3f4f6;
}

.ai-chat__text--pending {
  color: var(--color-muted);
}

.ai-chat__error {
  margin: 12px 0 0;
  padding: 10px 12px;
  font-size: 14px;
  color: #b91c1c;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
}

.ai-chat__input {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.ai-chat__input input {
  flex: 1;
  padding: 10px 12px;
  font-family: inherit;
  font-size: 14px;
  color: var(--color-text);
  background-color: #fff;
  border: 1px solid var(--color-border);
  border-radius: 6px;
}

.ai-chat__input input:focus {
  border-color: var(--color-primary);
  outline: 2px solid #bfdbfe;
}

.ai-chat__input button {
  padding: 10px 22px;
  font-size: 14px;
  color: #fff;
  background-color: var(--color-primary);
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.ai-chat__input button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
