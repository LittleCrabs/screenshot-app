<template>
  <div>
    <van-cell-group inset title="Query">
      <van-field v-model="selectedBrandText" is-link readonly label="Brand"
        placeholder="Select brand" @click="showBrandPicker = true" />
      <van-field v-model="videoKeyword" label="Keyword" placeholder="Search video..."
        clearable @keyup.enter="searchVideos" :disabled="!selectedBrand" />
    </van-cell-group>

    <div class="btn-group">
      <van-button type="primary" round :loading="loading" @click="searchVideos" :disabled="!selectedBrand">Search</van-button>
      <van-button type="success" round icon="plus" @click="$refs.uploadRef.open()">Upload Video</van-button>
    </div>

    <van-cell-group inset title="Videos" v-if="videoList.length > 0">
      <van-cell v-for="item in videoList" :key="item.path" :title="item.name"
        is-link @click="playVideo(item)" />
    </van-cell-group>

    <van-cell-group inset title="Player" v-if="videoUrl">
      <div class="video-player">
        <video :src="videoUrl" controls width="100%"></video>
      </div>
    </van-cell-group>

    <!-- Brand Picker -->
    <van-popup v-model:show="showBrandPicker" position="bottom" round>
      <van-picker :columns="brandOptions" @confirm="onBrandConfirm" @cancel="showBrandPicker = false" title="Select Brand" />
    </van-popup>

    <!-- Video Upload -->
    <VideoUpload ref="uploadRef" :api-base="apiBase" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { showToast } from 'vant'
import VideoUpload from './VideoUpload.vue'

const props = defineProps({ apiBase: { type: String, default: '' } })

const uploadRef = ref(null)
const brandListRaw = ref([])
const videoList = ref([])
const videoUrl = ref('')
const videoKeyword = ref('')
const selectedBrand = ref('')
const selectedBrandText = ref('')
const loading = ref(false)
const showBrandPicker = ref(false)

const brandOptions = computed(() => brandListRaw.value.filter(b => b !== 'Pending Video').map(b => ({ text: b, value: b })))

onMounted(() => fetchBrands())

const fetchBrands = async () => {
  try {
    const res = await fetch(`${props.apiBase}/api/screenshots/brands/?mode=Video Tutorial`, { credentials: 'include' })
    if (res.ok) brandListRaw.value = (await res.json()).brands
  } catch { showToast('Failed to load brands') }
}

const onBrandConfirm = ({ selectedOptions }) => {
  selectedBrand.value = selectedOptions[0].value
  selectedBrandText.value = selectedOptions[0].text
  showBrandPicker.value = false
  videoList.value = []
  videoUrl.value = ''
}

const searchVideos = async () => {
  if (!selectedBrand.value) return showToast('Please select a brand')

  loading.value = true
  videoList.value = []
  videoUrl.value = ''

  try {
    const res = await fetch(`${props.apiBase}/api/screenshots/videos/?brand=${encodeURIComponent(selectedBrand.value)}&keyword=${encodeURIComponent(videoKeyword.value.trim())}`, { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      videoList.value = data.videos
      if (data.videos.length === 0) showToast('No matching videos found')
    } else showToast('Query failed')
  } catch { showToast('Network error') }
  finally { loading.value = false }
}

const playVideo = (item) => {
  videoUrl.value = `${props.apiBase}${item.path}`
}
</script>

<style scoped>
.btn-group { padding: 16px; display: flex; gap: 12px; }
.btn-group .van-button { flex: 1; }
.video-player { padding: 12px; }
.video-player video { border-radius: 8px; }
</style>
