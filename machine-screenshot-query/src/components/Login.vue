<template>
  <div class="login-page">
    <div class="login-header">
      <h2>Screenshot Query System</h2>
    </div>
    <van-form @submit="handleLogin" class="login-form">
      <van-cell-group inset>
        <van-field
          v-model="username"
          name="username"
          label="Username"
          placeholder="Enter username"
          :rules="[{ required: true, message: 'Please enter username' }]"
        />
        <van-field
          v-model="password"
          type="password"
          name="password"
          label="Password"
          placeholder="Enter password"
          :rules="[{ required: true, message: 'Please enter password' }]"
        />
      </van-cell-group>
      <div class="login-btn-wrap">
        <van-button round block type="primary" native-type="submit" :loading="loading">
          Login
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
      showToast({ message: 'Login successful', type: 'success' })
      emit('login-success', data.user)
    } else {
      showToast({ message: data.error || 'Login failed', type: 'fail' })
    }
  } catch {
    showToast({ message: 'Network error', type: 'fail' })
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
