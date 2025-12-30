<template>
  <van-popup v-model:show="show" position="right" :style="{ width: '100%', height: '100%' }">
    <div class="upload-page">
      <van-nav-bar title="Upload Video" left-arrow @click-left="close" />

      <!-- 上传成功页面 -->
      <div v-if="uploadSuccess" class="success-page">
        <van-icon name="checked" size="80" color="#07c160" />
        <h2>Upload Successful!</h2>
        <p>Your video has been submitted for review.</p>
        <div class="success-info">
          <p><strong>Brand:</strong> {{ form.brand }}</p>
          <p><strong>Model:</strong> {{ form.model }}</p>
          <p><strong>Title:</strong> {{ form.title }}</p>
        </div>
        <div class="success-actions">
          <van-button type="primary" block @click="resetForm">Upload Another Video</van-button>
          <van-button block @click="close" style="margin-top: 12px">Back</van-button>
        </div>
      </div>

      <!-- 上传表单 -->
      <div v-else class="upload-form">
        <van-cell-group inset>
          <van-field v-model="form.brandText" is-link readonly label="Brand" placeholder="Select brand"
            @click="showBrandPicker = true" :rules="[{ required: true }]" />
          <van-field v-model="form.model" label="Model" placeholder="e.g. AP7775" clearable
            :rules="[{ required: true }]" />
          <van-field v-model="form.title" label="Video Title" placeholder="e.g. How to replace IBT" clearable
            :rules="[{ required: true }]" />
        </van-cell-group>

        <van-cell-group inset title="Upload File" style="margin-top: 16px">
          <div class="file-upload-area">
            <input type="file" ref="fileInput" accept="video/*" @change="onFileSelect" style="display: none" />
            <div v-if="!form.file" class="upload-placeholder" @click="$refs.fileInput.click()">
              <van-icon name="video-o" size="48" color="#999" />
              <p>Click to select video file</p>
              <p class="hint">Supported: MP4, WebM, MOV, AVI, MKV</p>
            </div>
            <div v-else class="file-selected">
              <van-icon name="video" size="32" color="#1989fa" />
              <div class="file-info">
                <p class="file-name">{{ form.file.name }}</p>
                <p class="file-size">{{ formatSize(form.file.size) }}</p>
              </div>
              <van-icon name="cross" size="20" color="#999" @click="form.file = null" />
            </div>
          </div>
        </van-cell-group>

        <!-- 上传进度 -->
        <div v-if="uploading" class="upload-progress">
          <p>Upload Progress:</p>
          <van-progress :percentage="progress" stroke-width="8" />
          <p class="progress-hint">Uploading... Please don't close this page.</p>
        </div>

        <div class="submit-btn">
          <van-button type="primary" block round :loading="uploading" :disabled="!canSubmit" @click="submit">
            {{ uploading ? 'Uploading...' : 'Upload Video' }}
          </van-button>
        </div>
      </div>

      <!-- Brand Picker -->
      <van-popup v-model:show="showBrandPicker" position="bottom" round>
        <van-picker :columns="brandOptions" @confirm="onBrandConfirm" @cancel="showBrandPicker = false" title="Select Brand" />
      </van-popup>
    </div>
  </van-popup>
</template>

<script setup>
import { ref, computed } from 'vue'
import { showToast } from 'vant'

const props = defineProps({ apiBase: { type: String, default: '' } })
const emit = defineEmits(['close'])

const show = ref(false)
const showBrandPicker = ref(false)
const uploading = ref(false)
const progress = ref(0)
const uploadSuccess = ref(false)
const fileInput = ref(null)

const form = ref({
  brand: '',
  brandText: '',
  model: '',
  title: '',
  file: null
})

const brandOptions = [
  { text: 'FUJI XEROX', value: 'FUJI XEROX' },
  { text: 'FUJI FILM', value: 'FUJI FILM' },
  { text: 'Canon', value: 'Canon' }
]

const canSubmit = computed(() => {
  return form.value.brand && form.value.model.trim() && form.value.title.trim() && form.value.file
})

const open = () => {
  show.value = true
  uploadSuccess.value = false
}

const close = () => {
  show.value = false
  emit('close')
}

const resetForm = () => {
  form.value = { brand: '', brandText: '', model: '', title: '', file: null }
  progress.value = 0
  uploadSuccess.value = false
}

const onBrandConfirm = ({ selectedOptions }) => {
  form.value.brand = selectedOptions[0].value
  form.value.brandText = selectedOptions[0].text
  showBrandPicker.value = false
}

const onFileSelect = (e) => {
  const file = e.target.files[0]
  if (file) {
    const ext = file.name.split('.').pop().toLowerCase()
    if (!['mp4', 'webm', 'mov', 'avi', 'mkv'].includes(ext)) {
      showToast('Invalid video format')
      return
    }
    form.value.file = file
  }
}

const formatSize = (bytes) => {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  if (bytes < 1024 * 1024 * 1024) return (bytes / 1024 / 1024).toFixed(1) + ' MB'
  return (bytes / 1024 / 1024 / 1024).toFixed(1) + ' GB'
}

const submit = async () => {
  if (!canSubmit.value) return

  uploading.value = true
  progress.value = 0

  const formData = new FormData()
  formData.append('brand', form.value.brand)
  formData.append('model', form.value.model)
  formData.append('title', form.value.title)
  formData.append('video', form.value.file)

  try {
    const xhr = new XMLHttpRequest()
    xhr.open('POST', `${props.apiBase}/api/screenshots/upload-video/`)
    xhr.withCredentials = true

    xhr.upload.onprogress = (e) => {
      if (e.lengthComputable) {
        progress.value = Math.round((e.loaded / e.total) * 100)
      }
    }

    xhr.onload = () => {
      uploading.value = false
      if (xhr.status === 200) {
        uploadSuccess.value = true
      } else {
        const res = JSON.parse(xhr.responseText)
        showToast(res.error || 'Upload failed')
      }
    }

    xhr.onerror = () => {
      uploading.value = false
      showToast('Network error')
    }

    xhr.send(formData)
  } catch {
    uploading.value = false
    showToast('Upload failed')
  }
}

defineExpose({ open })
</script>

<style scoped>
.upload-page { height: 100%; background: #f7f8fa; display: flex; flex-direction: column; }
.upload-form { flex: 1; padding: 16px 0; overflow-y: auto; }
.file-upload-area { padding: 16px; }
.upload-placeholder { border: 2px dashed #ddd; border-radius: 8px; padding: 32px; text-align: center; cursor: pointer; }
.upload-placeholder p { margin: 8px 0 0; color: #666; }
.upload-placeholder .hint { font-size: 12px; color: #999; }
.file-selected { display: flex; align-items: center; gap: 12px; padding: 12px; background: #f0f9ff; border-radius: 8px; }
.file-info { flex: 1; }
.file-name { font-weight: 500; word-break: break-all; }
.file-size { font-size: 12px; color: #999; margin-top: 4px; }
.upload-progress { padding: 16px; margin: 16px; background: #fff; border-radius: 8px; }
.upload-progress p { margin-bottom: 12px; font-weight: 500; }
.progress-hint { margin-top: 12px; font-size: 12px; color: #999; text-align: center; }
.submit-btn { padding: 16px; }
.success-page { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 32px; text-align: center; }
.success-page h2 { margin: 16px 0 8px; color: #07c160; }
.success-page > p { color: #666; }
.success-info { margin: 24px 0; padding: 16px; background: #f7f8fa; border-radius: 8px; width: 100%; text-align: left; }
.success-info p { margin: 8px 0; }
.success-actions { width: 100%; margin-top: 24px; }
</style>
