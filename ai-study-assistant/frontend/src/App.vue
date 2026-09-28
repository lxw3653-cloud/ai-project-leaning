<script setup>
import { computed, ref } from 'vue'

import AiChatView from '@/views/AiChatView.vue'
import AiSummaryView from '@/views/AiSummaryView.vue'
import StudyPlansView from '@/views/StudyPlansView.vue'

// 没有引入路由：用标签页 + <component :is> 完成最简单的页面切换
const tabs = [
  { key: 'plans', label: '学习计划', component: StudyPlansView },
  { key: 'ai', label: 'AI 聊天', component: AiChatView },
  { key: 'summary', label: 'AI 总结', component: AiSummaryView },
]

const activeKey = ref('plans')
const activeView = computed(
  () => tabs.find((tab) => tab.key === activeKey.value)?.component ?? tabs[0].component,
)
</script>

<template>
  <div class="app">
    <header class="app-header">
      <h1>AI 学习助手</h1>
      <p class="app-subtitle">学习计划管理 · AI 问答 · AI 总结</p>
    </header>

    <nav class="app-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        type="button"
        class="app-tabs__item"
        :class="{ 'is-active': tab.key === activeKey }"
        @click="activeKey = tab.key"
      >
        {{ tab.label }}
      </button>
    </nav>

    <main class="app-main">
      <!-- KeepAlive：切到别的标签再切回来时，对话内容不会丢 -->
      <KeepAlive>
        <component :is="activeView" />
      </KeepAlive>
    </main>

    <footer class="app-footer">Vue 3 + Vite + FastAPI</footer>
  </div>
</template>

<style scoped>
.app-tabs {
  display: flex;
  gap: 20px;
  padding: 0 32px;
  background-color: #fff;
  border-bottom: 1px solid var(--color-border);
}

.app-tabs__item {
  padding: 10px 2px;
  font-size: 14px;
  color: var(--color-muted);
  background: none;
  border: none;
  border-bottom: 2px solid transparent;
  cursor: pointer;
}

.app-tabs__item.is-active {
  font-weight: 600;
  color: var(--color-primary);
  border-bottom-color: var(--color-primary);
}
</style>
