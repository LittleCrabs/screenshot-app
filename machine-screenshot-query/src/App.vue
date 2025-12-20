<template>
  <div class="app">
    <Login v-if="!isLoggedIn" @login-success="onLoginSuccess" />

    <div v-else>
      <!-- Top Navigation -->
      <van-nav-bar title="Edoc Query" fixed placeholder>
        <template #right>
          <span class="logout-text" @click="handleLogout">Logout</span>
        </template>
      </van-nav-bar>

      <div class="main-content">
        <!-- Mode Switch -->
        <van-cell-group inset title="Mode">
          <van-radio-group v-model="queryMode" direction="horizontal" class="mode-radio">
            <van-radio name="errorCode">Error Code</van-radio>
            <van-radio name="ioCheck">Component IO Check</van-radio>
          </van-radio-group>
        </van-cell-group>

        <!-- Error Code Mode -->
        <template v-if="queryMode === 'errorCode'">
          <van-cell-group inset title="Query">
            <van-field
              v-model="selectedBrandText"
              is-link
              readonly
              label="Brand"
              placeholder="Select brand (required)"
              @click="showBrandPicker = true"
            />
            <van-field
              v-model="selectedModelText"
              is-link
              readonly
              label="Model"
              placeholder="Select model (required)"
              @click="showModelPicker = true"
              :disabled="!selectedBrand"
            />
            <van-field
              v-model="inputCode"
              label="Code"
              placeholder="e.g. 005-120"
              clearable
              @keyup.enter="queryImage"
            />
          </van-cell-group>

          <div class="query-btn-wrap">
            <van-button type="primary" block round :loading="loading" @click="queryImage">
              Search
            </van-button>
          </div>

          <!-- Search Results -->
          <van-cell-group inset title="Results" v-if="searchResults.length > 0">
            <van-cell
              v-for="item in searchResults"
              :key="item.path"
              :title="item.name"
              is-link
              @click="selectImage(item)"
            />
          </van-cell-group>

          <!-- Image Preview -->
          <van-cell-group inset title="Preview" v-if="imageUrl">
            <div class="image-preview">
              <van-image
                :src="imageUrl"
                fit="contain"
                @click="previewImage"
                @error="onImageError"
              />
            </div>
          </van-cell-group>
        </template>

        <!-- Component IO Check Mode -->
        <template v-if="queryMode === 'ioCheck'">
          <van-cell-group inset title="Query">
            <van-field
              v-model="selectedBrandText"
              is-link
              readonly
              label="Brand"
              placeholder="Select brand (required)"
              @click="showBrandPicker = true"
            />
            <van-field
              v-model="selectedFileText"
              is-link
              readonly
              label="File"
              placeholder="Select file (required)"
              @click="showFilePicker = true"
              :disabled="!selectedBrand"
            />
          </van-cell-group>

          <!-- HTML Content -->
          <van-cell-group inset title="Content" v-if="htmlContent">
            <div class="html-content" v-html="htmlContent"></div>
          </van-cell-group>
        </template>
      </div>

      <!-- Brand Picker -->
      <van-popup v-model:show="showBrandPicker" position="bottom" round>
        <van-picker
          :columns="brandList"
          :columns-field-names="{ text: 'text', value: 'text' }"
          @confirm="onBrandConfirm"
          @cancel="showBrandPicker = false"
          title="Select Brand"
        />
      </van-popup>

      <!-- Model Picker -->
      <van-popup v-model:show="showModelPicker" position="bottom" round>
        <van-picker
          :columns="modelList"
          :columns-field-names="{ text: 'text', value: 'text' }"
          @confirm="onModelConfirm"
          @cancel="showModelPicker = false"
          title="Select Model"
        />
      </van-popup>

      <!-- File Picker -->
      <van-popup v-model:show="showFilePicker" position="bottom" round>
        <van-picker
          :columns="fileList"
          :columns-field-names="{ text: 'text', value: 'text' }"
          @confirm="onFileConfirm"
          @cancel="showFilePicker = false"
          title="Select File"
        />
      </van-popup>

      <!-- Image Preview -->
      <van-image-preview v-model:show="showPreview" :images="[imageUrl]" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { showToast, showDialog } from 'vant'
import Login from './components/Login.vue'

const API_BASE = import.meta.env.VITE_API_BASE || ''

// Login state
const isLoggedIn = ref(false)
const user = ref(null)

// Query mode
const queryMode = ref('errorCode')

// Data
const brandListRaw = ref([])
const modelListRaw = ref([])
const searchResults = ref([])
const htmlFiles = ref([])
const htmlContent = ref('')
const selectedHtmlFile = ref('')
const selectedFileText = ref('')

const selectedBrand = ref('')
const selectedBrandText = ref('')
const selectedModel = ref('')
const selectedModelText = ref('')
const inputCode = ref('')
const imageUrl = ref('')
const loading = ref(false)

// Popup control
const showBrandPicker = ref(false)
const showModelPicker = ref(false)
const showFilePicker = ref(false)
const showPreview = ref(false)

// Picker data format
const brandList = computed(() => brandListRaw.value.map((b) => ({ text: b })))
const modelList = computed(() => modelListRaw.value.map((m) => ({ text: m })))
const fileList = computed(() => htmlFiles.value.map((f) => ({ text: f.name, filename: f.filename })))

// Watch mode change to reset data
watch(queryMode, () => {
  selectedBrand.value = ''
  selectedBrandText.value = ''
  selectedModel.value = ''
  selectedModelText.value = ''
  modelListRaw.value = []
  searchResults.value = []
  imageUrl.value = ''
  htmlFiles.value = []
  htmlContent.value = ''
  selectedHtmlFile.value = ''
  selectedFileText.value = ''
  inputCode.value = ''
})

onMounted(() => {
  const savedUser = localStorage.getItem('user')
  if (savedUser) {
    user.value = JSON.parse(savedUser)
    isLoggedIn.value = true
    fetchBrands()
  }
})

const onLoginSuccess = (userData) => {
  user.value = userData
  isLoggedIn.value = true
  fetchBrands()
}

const handleLogout = async () => {
  try {
    await showDialog({
      title: 'Confirm logout?',
      showCancelButton: true,
      confirmButtonText: 'OK',
      cancelButtonText: 'Cancel',
    })
    await fetch(`${API_BASE}/api/users/logout/`, {
      method: 'POST',
      credentials: 'include',
    })
  } catch {
    return
  }
  localStorage.removeItem('user')
  isLoggedIn.value = false
  user.value = null
}

// Fetch brand list
const fetchBrands = async () => {
  try {
    const response = await fetch(`${API_BASE}/api/screenshots/brands/`, {
      credentials: 'include',
    })
    if (response.ok) {
      const data = await response.json()
      brandListRaw.value = data.brands
    } else if (response.status === 401 || response.status === 403) {
      handleLogout()
    }
  } catch {
    showToast('Failed to load brands')
  }
}

// Brand selection
const onBrandConfirm = async ({ selectedValues }) => {
  const brand = selectedValues[0]
  selectedBrand.value = brand
  selectedBrandText.value = brand
  showBrandPicker.value = false

  // Clear child selections
  selectedModel.value = ''
  selectedModelText.value = ''
  modelListRaw.value = []
  searchResults.value = []
  imageUrl.value = ''
  htmlFiles.value = []
  htmlContent.value = ''
  selectedHtmlFile.value = ''
  selectedFileText.value = ''

  if (queryMode.value === 'errorCode') {
    // Fetch model list
    try {
      const response = await fetch(
        `${API_BASE}/api/screenshots/models/?brand=${encodeURIComponent(brand)}`,
        { credentials: 'include' }
      )
      if (response.ok) {
        const data = await response.json()
        modelListRaw.value = data.models
      }
    } catch {
      showToast('Failed to load models')
    }
  } else {
    // Fetch HTML file list
    try {
      const response = await fetch(
        `${API_BASE}/api/screenshots/html-list/?brand=${encodeURIComponent(brand)}`,
        { credentials: 'include' }
      )
      if (response.ok) {
        const data = await response.json()
        htmlFiles.value = data.files
        if (data.files.length === 0) {
          showToast('No HTML files found')
        }
      }
    } catch {
      showToast('Failed to load files')
    }
  }
}

// Model selection
const onModelConfirm = async ({ selectedValues }) => {
  const model = selectedValues[0]
  selectedModel.value = model
  selectedModelText.value = model
  searchResults.value = []
  imageUrl.value = ''
  showModelPicker.value = false
}

// Load HTML content
const loadHtmlContent = async (filename) => {
  htmlContent.value = ''

  try {
    const response = await fetch(
      `${API_BASE}/api/screenshots/html-content/?brand=${encodeURIComponent(selectedBrand.value)}&filename=${encodeURIComponent(filename)}`,
      { credentials: 'include' }
    )
    if (response.ok) {
      const responseData = await response.json()
      htmlContent.value = responseData.content

      // 执行 HTML 中的脚本
      setTimeout(() => {
        const container = document.querySelector('.html-content')
        if (container) {
          const scripts = container.querySelectorAll('script:not([type])')
          scripts.forEach((oldScript) => {
            const newScript = document.createElement('script')
            newScript.textContent = oldScript.textContent
            oldScript.parentNode.replaceChild(newScript, oldScript)
          })
        }
      }, 100)
    } else {
      showToast('Failed to load content')
    }
  } catch {
    showToast('Network error')
  }
}

// File selection
const onFileConfirm = async ({ selectedOptions }) => {
  const file = selectedOptions[0]
  selectedHtmlFile.value = file.filename
  selectedFileText.value = file.text
  showFilePicker.value = false
  await loadHtmlContent(file.filename)
}

// Search screenshot
const queryImage = async () => {
  if (!selectedBrand.value) {
    showToast('Please select a brand')
    return
  }
  if (!selectedModel.value) {
    showToast('Please select a model')
    return
  }
  if (!inputCode.value.trim()) {
    showToast('Please enter screenshot code')
    return
  }

  loading.value = true
  searchResults.value = []
  imageUrl.value = ''

  try {
    const url = `${API_BASE}/api/screenshots/search/?brand=${encodeURIComponent(selectedBrand.value)}&model=${encodeURIComponent(selectedModel.value)}&keyword=${encodeURIComponent(inputCode.value.trim())}`

    const response = await fetch(url, { credentials: 'include' })
    if (response.ok) {
      const data = await response.json()
      if (data.images.length === 0) {
        showToast('No matching screenshot found')
      } else if (data.images.length === 1) {
        selectImage(data.images[0])
      } else {
        searchResults.value = data.images
      }
    } else {
      showToast('Query failed')
    }
  } catch {
    showToast('Network error')
  } finally {
    loading.value = false
  }
}

const selectImage = (item) => {
  imageUrl.value = `${API_BASE}${item.path}`
  searchResults.value = []
}

const onImageError = () => {
  showToast('Failed to load image')
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

.mode-radio {
  padding: 12px 16px;
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

.html-content {
  padding: 12px;
  overflow-x: auto;
}

.html-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}

.html-content :deep(td),
.html-content :deep(th) {
  border: 1px solid #ddd;
  padding: 6px;
}
</style>
