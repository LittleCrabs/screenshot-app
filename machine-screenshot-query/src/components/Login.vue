<template>
  <div class="login-page">
    <div class="login-header">
      <h2>Edoc Query System</h2>
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
    <div class="notice-box">
      <strong>Important Notice</strong>
      <p>All resources provided by the Edoc query system are from the internet.</p>
      <p>I assume no legal responsibility for any content in this software!</p>
    </div>
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
  height: 100vh;
  background: #f7f8fa;
  padding: 60px 0 20px;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
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

.notice-box {
  margin: auto 16px 20px;
  padding: 12px;
  border: 2px solid #ee0a24;
    color: #ee0a24;

  border-radius: 8px;
  background: #fff;
    text-align: center;

}

.notice-box p {
  color: #ee0a24;
  font-size: 13px;
  line-height: 1.6;
  margin: 0;
  text-align: left;
}
</style>
