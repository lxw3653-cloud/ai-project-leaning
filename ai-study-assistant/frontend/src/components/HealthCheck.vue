<script setup>
import { ref } from 'vue'

import { getHealth } from '@/api/client'

// idle：尚未检测 / loading：检测中 / success：成功 / error：失败
const status = ref('idle')
const result = ref(null)
const errorMessage = ref('')

async function check() {
  status.value = 'loading'
  errorMessage.value = ''

  try {
    result.value = await getHealth()
    status.value = 'success'
  } catch (error) {
    result.value = null
    errorMessage.value = error.message
    status.value = 'error'
  }
}
</script>

<template>
  <div class="health-check">
    <button type="button" :disabled="status === 'loading'" @click="check">
      {{ status === 'loading' ? '检测中…' : '检测后端连接' }}
    </button>

    <p v-if="status === 'success'" class="ok">
      后端正常：{{ result.service }} v{{ result.version }}
    </p>
    <p v-else-if="status === 'error'" class="err">
      连接失败：{{ errorMessage }}（请确认后端已在 8000 端口启动）
    </p>
  </div>
</template>
