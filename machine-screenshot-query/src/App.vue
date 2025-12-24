<template>
  <div class="app">
    <Login v-if="!isLoggedIn" @login-success="onLoginSuccess" />

    <div v-else>
      <van-nav-bar title="Edoc Query" fixed placeholder>
        <template #right>
          <span class="logout-text" @click="handleLogout">Logout</span>
        </template>
      </van-nav-bar>

      <div class="main-content">
        <van-cell-group inset title="Mode">
          <van-radio-group v-model="queryMode" direction="horizontal" class="mode-radio">
            <van-radio name="errorCode">Error Code</van-radio>
            <van-radio name="ioCheck">Component IO Check</van-radio>
            <van-radio name="video">Video Tutorial</van-radio>
          </van-radio-group>
        </van-cell-group>

        <ErrorCodeMode v-if="queryMode === 'errorCode'" :api-base="API_BASE" />
        <ComponentIOCheckMode v-if="queryMode === 'ioCheck'" :api-base="API_BASE" />
        <VideoTutorialMode v-if="queryMode === 'video'" :api-base="API_BASE" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { showDialog } from 'vant'
import Login from './components/Login.vue'
import ErrorCodeMode from './components/ErrorCodeMode.vue'
import ComponentIOCheckMode from './components/ComponentIOCheckMode.vue'
import VideoTutorialMode from './components/VideoTutorialMode.vue'

const API_BASE = import.meta.env.VITE_API_BASE || ''

const isLoggedIn = ref(false)
const user = ref(null)
const queryMode = ref('errorCode')

onMounted(() => {
  const savedUser = localStorage.getItem('user')
  if (savedUser) {
    user.value = JSON.parse(savedUser)
    isLoggedIn.value = true
  }
})

const onLoginSuccess = (userData) => {
  user.value = userData
  isLoggedIn.value = true
}

const handleLogout = async () => {
  try {
    await showDialog({ title: 'Confirm logout?', showCancelButton: true })
    await fetch(`${API_BASE}/api/users/logout/`, { method: 'POST', credentials: 'include' })
  } catch { return }
  localStorage.removeItem('user')
  isLoggedIn.value = false
  user.value = null
}
</script>

<style scoped>
.app { min-height: 100vh; background: #f7f8fa; }
.logout-text { color: #1989fa; font-size: 14px; cursor: pointer; }
.main-content { padding: 12px 0; }
.mode-radio { padding: 12px 16px; }
</style>
