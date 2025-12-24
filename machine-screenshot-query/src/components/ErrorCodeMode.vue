<template>
  <div>
    <van-cell-group inset title="Query">
      <van-field v-model="selectedBrandText" is-link readonly label="Brand"
        placeholder="Select brand" @click="showBrandPicker = true" />
      <van-field v-model="selectedModelText" is-link readonly label="Model"
        placeholder="Select model" @click="showModelPicker = true" :disabled="!selectedBrand" />
      <van-field v-model="inputCode" label="Code" placeholder="e.g. 005-120"
        clearable @keyup.enter="queryImage" />
    </van-cell-group>

    <div class="query-btn-wrap">
      <van-button type="primary" block round :loading="loading" @click="queryImage">Search</van-button>
    </div>

    <van-cell-group inset title="Results" v-if="searchResults.length > 0">
      <van-cell v-for="item in searchResults" :key="item.path" :title="item.name"
        is-link @click="selectImage(item)" />
    </van-cell-group>

    <van-cell-group inset title="Preview" v-if="imageUrl">
      <div class="image-preview">
        <van-image :src="imageUrl" fit="contain" @click="showPreview = true" @error="onImageError" />
      </div>
    </van-cell-group>

    <!-- Brand Picker -->
    <van-popup v-model:show="showBrandPicker" position="bottom" round>
      <van-picker :columns="brandOptions" @confirm="onBrandConfirm" @cancel="showBrandPicker = false" title="Select Brand" />
    </van-popup>

    <!-- Model Picker -->
    <van-popup v-model:show="showModelPicker" position="bottom" round>
      <van-picker :columns="modelOptions" @confirm="onModelConfirm" @cancel="showModelPicker = false" title="Select Model" />
    </van-popup>

    <!-- Image Preview -->
    <van-image-preview v-model:show="showPreview" :images="[imageUrl]" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { showToast } from 'vant'

const props = defineProps({ apiBase: { type: String, default: '' } })

const brandListRaw = ref([])
const modelListRaw = ref([])
const searchResults = ref([])
const selectedBrand = ref('')
const selectedBrandText = ref('')
const selectedModel = ref('')
const selectedModelText = ref('')
const inputCode = ref('')
const imageUrl = ref('')
const loading = ref(false)
const showBrandPicker = ref(false)
const showModelPicker = ref(false)
const showPreview = ref(false)

const brandOptions = computed(() => brandListRaw.value.map(b => ({ text: b, value: b })))
const modelOptions = computed(() => modelListRaw.value.map(m => ({ text: m, value: m })))

onMounted(() => fetchBrands())

const fetchBrands = async () => {
  try {
    const res = await fetch(`${props.apiBase}/api/screenshots/brands/?mode=Error Code`, { credentials: 'include' })
    if (res.ok) brandListRaw.value = (await res.json()).brands
  } catch { showToast('Failed to load brands') }
}

const onBrandConfirm = async ({ selectedOptions }) => {
  const brand = selectedOptions[0].value
  selectedBrand.value = brand
  selectedBrandText.value = brand
  showBrandPicker.value = false
  selectedModel.value = ''
  selectedModelText.value = ''
  searchResults.value = []
  imageUrl.value = ''

  try {
    const res = await fetch(`${props.apiBase}/api/screenshots/models/?mode=Error Code&brand=${encodeURIComponent(brand)}`, { credentials: 'include' })
    if (res.ok) modelListRaw.value = (await res.json()).models
  } catch { showToast('Failed to load models') }
}

const onModelConfirm = ({ selectedOptions }) => {
  selectedModel.value = selectedOptions[0].value
  selectedModelText.value = selectedOptions[0].text
  searchResults.value = []
  imageUrl.value = ''
  showModelPicker.value = false
}

const queryImage = async () => {
  if (!selectedBrand.value) return showToast('Please select a brand')
  if (!selectedModel.value) return showToast('Please select a model')
  if (!inputCode.value.trim()) return showToast('Please enter code')

  loading.value = true
  searchResults.value = []
  imageUrl.value = ''

  try {
    const url = `${props.apiBase}/api/screenshots/search/?mode=Error Code&brand=${encodeURIComponent(selectedBrand.value)}&model=${encodeURIComponent(selectedModel.value)}&keyword=${encodeURIComponent(inputCode.value.trim())}`
    const res = await fetch(url, { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      if (data.images.length === 0) showToast('No matching screenshot found')
      else if (data.images.length === 1) selectImage(data.images[0])
      else searchResults.value = data.images
    } else showToast('Query failed')
  } catch { showToast('Network error') }
  finally { loading.value = false }
}

const selectImage = (item) => {
  imageUrl.value = `${props.apiBase}${item.path}`
  searchResults.value = []
}

const onImageError = () => {
  showToast('Failed to load image')
  imageUrl.value = ''
}
</script>

<style scoped>
.query-btn-wrap { padding: 16px; }
.image-preview { padding: 12px; }
.image-preview :deep(.van-image) { width: 100%; min-height: 200px; }
</style>
