<template>
  <div class="login-page">
    <div class="login-header">
      <h2>机器截图查询系统</h2>
    </div>
    <van-form @submit="handleLogin" class="login-form">
      <van-cell-group inset>
        <van-field
          v-model="username"
          name="username"
          label="用户名"
          placeholder="请输入用户名"
          :rules="[{ required: true, message: '请输入用户名' }]"
        />
        <van-field
          v-model="password"
          type="password"
          name="password"
          label="密码"
          placeholder="请输入密码"
          :rules="[{ required: true, message: '请输入密码' }]"
        />
      </van-cell-group>
      <div class="login-btn-wrap">
        <van-button round block type="primary" native-type="submit" :loading="loading">
          登录
        </van-button>
      </div>
    </van-form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { showToast } from 'vant'

const emit = defineEmits(['login-success'])

const username = ref('')
const password = ref('')
const loading = ref(false)

const API_BASE = import.meta.env.VITE_API_BASE || ''

const handleLogin = async () => {
  loading.value = true

  try {
    const response = await fetch(`${API_BASE}/api/users/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    })

    const data = await response.json()

    if (response.ok) {
      localStorage.setItem('user', JSON.stringify(data.user))
      showToast({ message: '登录成功', type: 'success' })
      emit('login-success', data.user)
    } else {
      showToast({ message: data.error || '登录失败', type: 'fail' })
    }
  } catch {
    showToast({ message: '网络错误', type: 'fail' })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: #f7f8fa;
  padding-top: 100px;
}

.login-header {
  text-align: center;
  color: #323233;
  margin-bottom: 40px;
}

.login-header h2 {
  font-size: 22px;
  font-weight: 600;
}

.login-form {
  margin: 0 16px;
}

.login-btn-wrap {
  margin: 24px 16px;
}
</style>
