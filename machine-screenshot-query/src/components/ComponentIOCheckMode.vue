<template>
  <div>
    <van-cell-group inset title="Query">
      <van-field v-model="selectedBrandText" is-link readonly label="Brand"
        placeholder="Select brand" @click="showBrandPicker = true" />
      <van-field v-model="selectedFileText" is-link readonly label="File"
        placeholder="Select file" @click="showFilePicker = true" :disabled="!selectedBrand" />
    </van-cell-group>

    <ComponentCheck v-if="componentData.length > 0" :title="componentTitle" :data="componentData" />

    <!-- Brand Picker -->
    <van-popup v-model:show="showBrandPicker" position="bottom" round>
      <van-picker :columns="brandOptions" @confirm="onBrandConfirm" @cancel="showBrandPicker = false" title="Select Brand" />
    </van-popup>

    <!-- File Picker -->
    <van-popup v-model:show="showFilePicker" position="bottom" round>
      <van-picker :columns="fileOptions" @confirm="onFileConfirm" @cancel="showFilePicker = false" title="Select File" />
    </van-popup>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { showToast } from 'vant'
import ComponentCheck from './ComponentCheck.vue'

const props = defineProps({ apiBase: { type: String, default: '' } })

const brandListRaw = ref([])
const fileListRaw = ref([])
const componentData = ref([])
const componentTitle = ref('')
const selectedBrand = ref('')
const selectedBrandText = ref('')
const selectedFileText = ref('')
const showBrandPicker = ref(false)
const showFilePicker = ref(false)

const brandOptions = computed(() => brandListRaw.value.map(b => ({ text: b, value: b })))
const fileOptions = computed(() => fileListRaw.value.map(f => ({ text: f.name, value: f.filename })))

onMounted(() => fetchBrands())

const fetchBrands = async () => {
  try {
    const res = await fetch(`${props.apiBase}/api/screenshots/brands/?mode=Component IO Check`, { credentials: 'include' })
    if (res.ok) brandListRaw.value = (await res.json()).brands
  } catch { showToast('Failed to load brands') }
}

const onBrandConfirm = async ({ selectedOptions }) => {
  const brand = selectedOptions[0].value
  selectedBrand.value = brand
  selectedBrandText.value = brand
  showBrandPicker.value = false
  selectedFileText.value = ''
  componentData.value = []

  try {
    const res = await fetch(`${props.apiBase}/api/screenshots/components/?brand=${encodeURIComponent(brand)}`, { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      fileListRaw.value = data.files
      if (data.files.length === 0) showToast('No files found')
    }
  } catch { showToast('Failed to load files') }
}

const onFileConfirm = async ({ selectedOptions }) => {
  const file = selectedOptions[0]
  selectedFileText.value = file.text
  showFilePicker.value = false

  try {
    const res = await fetch(`${props.apiBase}/api/screenshots/component-data/?brand=${encodeURIComponent(selectedBrand.value)}&filename=${encodeURIComponent(file.value)}`, { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      componentTitle.value = data.title || file.text
      componentData.value = data.data || []
    } else showToast('Failed to load data')
  } catch { showToast('Network error') }
}
</script>
