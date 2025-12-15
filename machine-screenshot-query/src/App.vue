<template>
  <div class="app">
    <Login v-if="!isLoggedIn" @login-success="onLoginSuccess" />

    <div v-else>
      <!-- 顶部导航 -->
      <van-nav-bar title="机器截图查询" fixed placeholder>
        <template #right>
          <span class="logout-text" @click="handleLogout">退出</span>
        </template>
      </van-nav-bar>

      <div class="main-content">
        <!-- 型号选择 -->
        <van-cell-group inset title="查询条件">
          <van-field
            v-model="selectedModelText"
            is-link
            readonly
            label="机器型号"
            placeholder="请选择型号（必选）"
            @click="showModelPicker = true"
          />
          <van-field
            v-model="selectedVersionText"
            is-link
            readonly
            label="版本"
            placeholder="全部版本（可选）"
            @click="showVersionPicker = true"
            :disabled="!selectedModel"
          />
          <van-field
            v-model="inputCode"
            label="截图代码"
            placeholder="请输入代码，如 005-120"
            clearable
            @keyup.enter="queryImage"
          />
        </van-cell-group>

        <div class="query-btn-wrap">
          <van-button type="primary" block round :loading="loading" @click="queryImage">
            查询截图
          </van-button>
        </div>

        <!-- 搜索结果 -->
        <van-cell-group inset title="搜索结果" v-if="searchResults.length > 0">
          <van-cell
            v-for="item in searchResults"
            :key="item.path"
            :title="item.name"
            is-link
            @click="selectImage(item)"
          />
        </van-cell-group>

        <!-- 图片预览 -->
        <van-cell-group inset title="截图预览" v-if="imageUrl">
          <div class="image-preview">
            <van-image
              :src="imageUrl"
              fit="contain"
              @click="previewImage"
              @error="onImageError"
            />
          </div>
        </van-cell-group>
      </div>

      <!-- 型号选择器 -->
      <van-popup v-model:show="showModelPicker" position="bottom" round>
        <van-picker
          :columns="modelList"
          :columns-field-names="{ text: 'text', value: 'text' }"
          @confirm="onModelConfirm"
          @cancel="showModelPicker = false"
          title="选择机器型号"
        />
      </van-popup>

      <!-- 版本选择器 -->
      <van-popup v-model:show="showVersionPicker" position="bottom" round>
        <van-picker
          :columns="versionColumns"
          :columns-field-names="{ text: 'text', value: 'text' }"
          @confirm="onVersionConfirm"
          @cancel="showVersionPicker = false"
          title="选择版本"
        />
      </van-popup>

      <!-- 图片预览 -->
      <van-image-preview v-model:show="showPreview" :images="[imageUrl]" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { showToast, showDialog } from 'vant'
import Login from './components/Login.vue'

const API_BASE = import.meta.env.VITE_API_BASE || ''

// 登录状态
const isLoggedIn = ref(false)
const user = ref(null)

// 数据
const modelListRaw = ref([])
const versionListRaw = ref([])
const searchResults = ref([])
const selectedModel = ref('')
const selectedModelText = ref('')
const selectedVersion = ref('')
const selectedVersionText = ref('')
const inputCode = ref('')
const imageUrl = ref('')
const loading = ref(false)

// 弹窗控制
const showModelPicker = ref(false)
const showVersionPicker = ref(false)
const showPreview = ref(false)

// Vant Picker 需要 [{text: xxx}] 格式
const modelList = computed(() => modelListRaw.value.map((m) => ({ text: m })))
const versionColumns = computed(() => [
  { text: '全部版本' },
  ...versionListRaw.value.map((v) => ({ text: v })),
])

onMounted(() => {
  const savedUser = localStorage.getItem('user')
  if (savedUser) {
    user.value = JSON.parse(savedUser)
    isLoggedIn.value = true
    fetchModels()
  }
})

const onLoginSuccess = (userData) => {
  user.value = userData
  isLoggedIn.value = true
  fetchModels()
}

const handleLogout = async () => {
  try {
    await showDialog({ title: '确认退出？', showCancelButton: true })
    await fetch(`${API_BASE}/api/users/logout/`, {
      method: 'POST',
      credentials: 'include',
    })
  } catch {
    // 取消或请求失败
    return
  }
  localStorage.removeItem('user')
  isLoggedIn.value = false
  user.value = null
}

const fetchModels = async () => {
  try {
    const response = await fetch(`${API_BASE}/api/screenshots/models/`, {
      credentials: 'include',
    })
    if (response.ok) {
      const data = await response.json()
      modelListRaw.value = data.models
    } else if (response.status === 401 || response.status === 403) {
      handleLogout()
    }
  } catch {
    showToast('获取型号列表失败')
  }
}

const onModelConfirm = async ({ selectedValues }) => {
  const model = selectedValues[0]
  selectedModel.value = model
  selectedModelText.value = model
  selectedVersion.value = ''
  selectedVersionText.value = ''
  versionListRaw.value = []
  searchResults.value = []
  imageUrl.value = ''
  showModelPicker.value = false

  // 获取版本列表
  try {
    const response = await fetch(
      `${API_BASE}/api/screenshots/versions/?model=${encodeURIComponent(model)}`,
      { credentials: 'include' }
    )
    if (response.ok) {
      const data = await response.json()
      versionListRaw.value = data.versions
    }
  } catch {
    // ignore
  }
}

const onVersionConfirm = ({ selectedValues }) => {
  const ver = selectedValues[0]
  selectedVersionText.value = ver
  selectedVersion.value = ver === '全部版本' ? '' : ver
  showVersionPicker.value = false
}

const queryImage = async () => {
  if (!selectedModel.value) {
    showToast('请先选择机器型号')
    return
  }
  if (!inputCode.value.trim()) {
    showToast('请输入截图代码')
    return
  }

  loading.value = true
  searchResults.value = []
  imageUrl.value = ''

  try {
    let url = `${API_BASE}/api/screenshots/search/?model=${encodeURIComponent(selectedModel.value)}&keyword=${encodeURIComponent(inputCode.value.trim())}`
    if (selectedVersion.value) {
      url += `&version=${encodeURIComponent(selectedVersion.value)}`
    }

    const response = await fetch(url, { credentials: 'include' })
    if (response.ok) {
      const data = await response.json()
      if (data.images.length === 0) {
        showToast('未找到匹配的截图')
      } else if (data.images.length === 1) {
        selectImage(data.images[0])
      } else {
        searchResults.value = data.images
      }
    } else {
      showToast('查询失败')
    }
  } catch {
    showToast('网络错误')
  } finally {
    loading.value = false
  }
}

const selectImage = (item) => {
  imageUrl.value = `${API_BASE}${item.path}`
  searchResults.value = []
}

const onImageError = () => {
  showToast('图片加载失败')
  imageUrl.value = ''
}

const previewImage = () => {
  if (imageUrl.value) {
    showPreview.value = true
  }
}
</script>

<style scoped>
.app {
  min-height: 100vh;
  background: #f7f8fa;
}

.logout-text {
  color: #1989fa;
  font-size: 14px;
  cursor: pointer;
}

.main-content {
  padding: 12px 0;
}

.query-btn-wrap {
  padding: 16px;
}

.image-preview {
  padding: 12px;
}

.image-preview :deep(.van-image) {
  width: 100%;
  min-height: 200px;
}
</style>
