<template>
  <div class="component-check">
    <div class="header">
      <h1>{{ title }}</h1>
    </div>
    <div class="controls">
      <div class="search-box">
        <input v-model="searchTerm" type="text" placeholder="Search component..." @keypress.enter="search">
        <button class="btn btn-primary" @click="search">Search</button>
      </div>
    </div>
    <div class="stats">
      <span>Total: <strong>{{ data.length }}</strong></span>
      <span>Showing: <strong>{{ filteredData.length }}</strong></span>
    </div>
    <div class="card-list">
      <div v-if="filteredData.length === 0" class="empty">No results found</div>
      <div v-for="item in filteredData" :key="item.name" class="card">
        <div class="card-header">
          <span class="card-name">{{ item.name }}</span>
          <span class="card-module">{{ item.module }}</span>
        </div>
        <div class="card-body">
          <div class="card-desc">{{ item.desc }}</div>
          <div class="card-meta">
            <span v-if="item.cyclic" class="meta-item cyclic">Cyclic</span>
            <span v-if="item.timeout && item.timeout !== '-'" class="meta-item">Timeout: {{ item.timeout }}</span>
            <span v-if="item.level && item.level !== '-'" class="meta-item level">Level: {{ item.level }}</span>
            <span v-if="item.prohibited && item.prohibited !== '-'" class="meta-item prohibited">Prohibited: {{ item.prohibited }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  title: { type: String, default: 'Output Component Check List' },
  data: { type: Array, default: () => [] }
})

const searchTerm = ref('')

const filteredData = computed(() => {
  if (!searchTerm.value.trim()) return props.data
  const term = searchTerm.value.toLowerCase()
  return props.data.filter(item =>
    item.name.toLowerCase().includes(term) ||
    item.desc.toLowerCase().includes(term) ||
    item.module.toLowerCase().includes(term)
  )
})

const search = () => {
  // 触发 computed 重新计算
}
</script>

<style scoped>
.component-check { background: #f7f8fa; min-height: 100%; }
.header { background: #1989fa; color: white; padding: 12px 16px; text-align: center; }
.header h1 { font-size: 16px; font-weight: 500; margin: 0; }
.controls { padding: 12px; background: #fff; border-bottom: 1px solid #eee; }
.search-box { display: flex; gap: 8px; }
.search-box input { flex: 1; padding: 10px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; outline: none; }
.search-box input:focus { border-color: #1989fa; }
.btn { padding: 10px 16px; border: none; border-radius: 6px; font-size: 13px; cursor: pointer; }
.btn-primary { background: #1989fa; color: white; }
.stats { padding: 8px 12px; background: #f7f8fa; font-size: 12px; color: #666; display: flex; justify-content: space-between; }
.card-list { padding: 8px; }
.card { background: #fff; border-radius: 8px; margin-bottom: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.card-header { padding: 10px 12px; background: #f7f8fa; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
.card-name { font-weight: 600; color: #1989fa; font-size: 15px; }
.card-module { font-size: 11px; background: #e8f4ff; color: #1989fa; padding: 2px 8px; border-radius: 10px; }
.card-body { padding: 10px 12px; }
.card-desc { color: #333; line-height: 1.5; margin-bottom: 8px; font-size: 13px; white-space: pre-line; }
.card-meta { display: flex; flex-wrap: wrap; gap: 8px; font-size: 11px; }
.meta-item { background: #f5f5f5; padding: 4px 8px; border-radius: 4px; color: #666; }
.meta-item.cyclic { background: #d4edda; color: #155724; }
.meta-item.prohibited { background: #fff3cd; color: #856404; }
.meta-item.level { background: #e8f4ff; color: #1989fa; }
.empty { text-align: center; padding: 40px; color: #999; }
</style>
