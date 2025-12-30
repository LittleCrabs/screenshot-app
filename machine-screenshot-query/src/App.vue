<template>
  <div class="app">
    <Transition name="fade" mode="out-in">
      <Login v-if="!isLoggedIn" @login-success="onLoginSuccess" key="login" />

      <div v-else key="main">
        <van-nav-bar title="Edoc Query" fixed placeholder>
          <template #right>
            <van-icon name="setting-o" size="20" color="#1989fa" @click="$refs.settingsRef.open()" style="cursor: pointer;" />
            <van-icon name="revoke" size="20" color="#ee0a24" @click="handleLogout" style="cursor: pointer; margin-left: 16px;" />
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

          <Transition name="slide-fade" mode="out-in">
            <ErrorCodeMode v-if="queryMode === 'errorCode'" :api-base="API_BASE" key="errorCode" />
            <ComponentIOCheckMode v-else-if="queryMode === 'ioCheck'" :api-base="API_BASE" key="ioCheck" />
            <VideoTutorialMode v-else-if="queryMode === 'video'" :api-base="API_BASE" key="video" />
          </Transition>
        </div>

        <Settings ref="settingsRef" :api-base="API_BASE" />
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { showDialog } from 'vant'
import Login from './components/Login.vue'
import ErrorCodeMode from './components/ErrorCodeMode.vue'
import ComponentIOCheckMode from './components/ComponentIOCheckMode.vue'
import VideoTutorialMode from './components/VideoTutorialMode.vue'
import Settings from './components/Settings.vue'

const API_BASE = import.meta.env.VITE_API_BASE || ''

const isLoggedIn = ref(false)
const user = ref(null)
const queryMode = ref('errorCode')
const settingsRef = ref(null)

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
    await showDialog({ title: 'Confirm logout?', showCancelButton: true, confirmButtonText: 'Confirm', cancelButtonText: 'Cancel' })
    await fetch(`${API_BASE}/api/users/logout/`, { method: 'POST', credentials: 'include' })
  } catch { return }
  localStorage.removeItem('user')
  isLoggedIn.value = false
  user.value = null
}
</script>

<style scoped>
.app { min-height: 100vh; background: #f7f8fa; overflow-x: hidden; }
.main-content { padding: 12px 0; overflow: hidden; }
.mode-radio { padding: 12px 16px; }

/* 淡入淡出动画 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 滑动淡入动画 */
.slide-fade-enter-active {
  transition: opacity 0.25s ease-out;
}
.slide-fade-leave-active {
  transition: opacity 0.2s ease-in;
}
.slide-fade-enter-from, .slide-fade-leave-to {
  opacity: 0;
}
</style>
