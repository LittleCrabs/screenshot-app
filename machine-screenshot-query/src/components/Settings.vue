<template>
  <van-popup v-model:show="show" position="right" :style="{ width: '100%', height: '100%' }">
    <div class="settings-page">
      <van-nav-bar title="Settings" left-arrow @click-left="close" />

      <div class="settings-content">
        <van-cell-group inset title="Account Settings">
          <van-cell title="Change Password" is-link @click="showChangePassword = true">
            <template #icon><van-icon name="lock" class="cell-icon" /></template>
          </van-cell>
          <van-cell title="Update Phone Number" is-link @click="showUpdatePhone = true" :value="phone">
            <template #icon><van-icon name="phone-o" class="cell-icon" /></template>
          </van-cell>
          <van-cell title="My Uploads" is-link @click="showMyUploads = true">
            <template #icon><van-icon name="video-o" class="cell-icon" /></template>
            <template #value><span class="upload-count">{{ uploadCount }} videos</span></template>
          </van-cell>
        </van-cell-group>
      </div>

      <!-- Change Password Popup -->
      <van-popup v-model:show="showChangePassword" position="bottom" round :style="{ height: 'auto' }">
        <div class="password-popup">
          <div class="popup-header">
            <span class="popup-title">Change Password</span>
            <van-icon name="cross" @click="showChangePassword = false" />
          </div>
          
          <div class="password-form">
            <div class="form-item">
              <div class="form-label">Old Password *</div>
              <input v-model="passwordForm.oldPassword" type="password" placeholder="Enter old password" class="form-input" />
            </div>
            <div class="form-item">
              <div class="form-label">New Password *</div>
              <input v-model="passwordForm.newPassword" type="password" placeholder="Enter new password (min 6 chars)" class="form-input" />
            </div>
            <div class="form-item">
              <div class="form-label">Confirm Password *</div>
              <input v-model="passwordForm.confirmPassword" type="password" placeholder="Confirm new password" class="form-input" />
            </div>
          </div>

          <div class="popup-actions">
            <van-button block type="primary" @click="submitPassword">Update Password</van-button>
          </div>
        </div>
      </van-popup>

      <!-- Update Phone Popup -->
      <van-popup v-model:show="showUpdatePhone" position="bottom" round :style="{ height: 'auto' }">
        <div class="phone-popup">
          <div class="phone-header">
            <span class="phone-title">Update Phone Number</span>
            <van-icon name="cross" @click="showUpdatePhone = false" />
          </div>
          
          <div class="phone-current" v-if="phone">
            <div class="current-label">Current Phone Number</div>
            <div class="current-value">
              <span>{{ phone }}</span>
              <van-tag type="success" size="large">Verified</van-tag>
            </div>
          </div>

          <div class="phone-form">
            <div class="form-label">New Phone Number *</div>
            <div class="phone-input-group">
              <div class="country-code" @click="showCountryPicker = true">
                <span>{{ selectedCountry.code }}</span>
                <van-icon name="arrow-down" size="12" />
              </div>
              <input v-model="phoneForm.number" type="tel" placeholder="8765-4321" class="phone-input" />
            </div>
          </div>

          <div class="phone-actions">
            <van-button block type="primary" @click="submitPhone">Update</van-button>
          </div>
        </div>
      </van-popup>

      <!-- Country Code Picker -->
      <van-popup v-model:show="showCountryPicker" position="bottom" round>
        <van-picker :columns="countryOptions" @confirm="onCountryConfirm" @cancel="showCountryPicker = false" title="Select Country" />
      </van-popup>

      <!-- My Uploads Dialog -->
      <van-popup v-model:show="showMyUploads" position="bottom" :style="{ height: '70%' }" round>
        <div class="my-uploads">
          <van-nav-bar title="My Uploads" left-arrow @click-left="showMyUploads = false" />
          <div class="uploads-content">
            <van-empty v-if="uploadList.length === 0" description="No uploads yet" />
            <div v-else class="uploads-list">
              <van-cell-group inset>
                <van-cell v-for="item in uploadList" :key="item.id">
                  <template #title>
                    <div class="upload-item-title">{{ item.title }}</div>
                  </template>
                  <template #label>
                    <div class="upload-item-info">
                      <span class="brand-tag">{{ item.brand }}</span>
                      <span class="model-text">{{ item.model }}</span>
                    </div>
                    <div class="upload-item-time">{{ item.created_at }}</div>
                  </template>
                </van-cell>
              </van-cell-group>
            </div>
          </div>
        </div>
      </van-popup>
    </div>
  </van-popup>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { showToast } from 'vant'

const props = defineProps({ apiBase: { type: String, default: '' } })

const show = ref(false)
const showChangePassword = ref(false)
const showUpdatePhone = ref(false)
const showCountryPicker = ref(false)
const showMyUploads = ref(false)
const phone = ref('')
const uploadCount = ref(0)
const uploadList = ref([])

const passwordForm = ref({ oldPassword: '', newPassword: '', confirmPassword: '' })
const phoneForm = ref({ number: '' })

const countryOptions = [
  { text: 'Singapore (+65)', value: '+65' },
  { text: 'China (+86)', value: '+86' },
  { text: 'Hong Kong (+852)', value: '+852' },
  { text: 'Taiwan (+886)', value: '+886' },
  { text: 'Malaysia (+60)', value: '+60' },
  { text: 'Japan (+81)', value: '+81' },
  { text: 'USA (+1)', value: '+1' },
]
const selectedCountry = ref({ code: '+65', name: 'Singapore' })

const open = () => {
  show.value = true
  fetchPhone()
  fetchUploadCount()
}

const close = () => {
  show.value = false
}

const fetchPhone = async () => {
  try {
    const res = await fetch(`${props.apiBase}/api/users/phone/`, { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      phone.value = data.phone || ''
    }
  } catch {}
}

const onCountryConfirm = ({ selectedOptions }) => {
  selectedCountry.value = { code: selectedOptions[0].value, name: selectedOptions[0].text }
  showCountryPicker.value = false
}

const submitPhone = async () => {
  if (!phoneForm.value.number.trim()) {
    showToast('Please enter phone number')
    return
  }

  const fullPhone = `${selectedCountry.value.code} ${phoneForm.value.number}`
  
  try {
    const res = await fetch(`${props.apiBase}/api/users/phone/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ phone: fullPhone })
    })
    const data = await res.json()
    if (res.ok) {
      showToast('Phone number updated')
      phone.value = data.phone
      phoneForm.value.number = ''
      showUpdatePhone.value = false
    } else {
      showToast(data.error || 'Failed to update phone')
    }
  } catch {
    showToast('Network error')
  }
}

const fetchUploadCount = async () => {
  try {
    const res = await fetch(`${props.apiBase}/api/screenshots/my-uploads/`, { credentials: 'include' })
    if (res.ok) {
      const data = await res.json()
      uploadCount.value = data.count
      uploadList.value = data.uploads || []
    }
  } catch {}
}

const submitPassword = async () => {
  const { oldPassword, newPassword, confirmPassword } = passwordForm.value
  if (!oldPassword || !newPassword) {
    showToast('Please fill all fields')
    return
  }
  if (newPassword.length < 6) {
    showToast('Password must be at least 6 characters')
    return
  }
  if (newPassword !== confirmPassword) {
    showToast('Passwords do not match')
    return
  }

  try {
    const res = await fetch(`${props.apiBase}/api/users/change-password/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ old_password: oldPassword, new_password: newPassword })
    })
    const data = await res.json()
    if (res.ok) {
      showToast('Password changed successfully')
      passwordForm.value = { oldPassword: '', newPassword: '', confirmPassword: '' }
      showChangePassword.value = false
    } else {
      showToast(data.error || 'Failed to change password')
    }
  } catch {
    showToast('Network error')
  }
}

defineExpose({ open })
</script>

<style scoped>
.settings-page { height: 100%; background: #f7f8fa; display: flex; flex-direction: column; }
.settings-content { flex: 1; padding: 16px 0; }
.cell-icon { margin-right: 8px; font-size: 18px; color: #1989fa; }
.upload-count { color: #1989fa; }
.my-uploads { height: 100%; display: flex; flex-direction: column; }
.uploads-content { flex: 1; overflow-y: auto; }
.uploads-list { padding: 12px 0; }
.upload-item-title { font-weight: 500; margin-bottom: 4px; }
.upload-item-info { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; }
.brand-tag { background: #e8f4ff; color: #1989fa; padding: 2px 8px; border-radius: 4px; font-size: 12px; }
.model-text { color: #666; font-size: 12px; }
.upload-item-time { color: #999; font-size: 12px; }

.phone-popup, .password-popup { padding: 20px; }
.phone-header, .popup-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.phone-title, .popup-title { font-size: 16px; font-weight: 600; }
.phone-current { background: #f7f8fa; padding: 12px; border-radius: 8px; margin-bottom: 20px; }
.current-label { font-size: 12px; color: #999; margin-bottom: 8px; }
.current-value { display: flex;justify-content:space-between; align-items: center; gap: 8px; font-size: 16px; font-weight: 500; }
.phone-form { margin-bottom: 20px; }
.form-label { font-size: 14px; color: #333; margin-bottom: 8px; }
.phone-input-group { display: flex; border: 1px solid #ddd; border-radius: 6px; overflow: hidden; }
.country-code { display: flex; align-items: center; gap: 4px; padding: 12px; background: #f7f8fa; border-right: 1px solid #ddd; cursor: pointer; font-weight: 500; }
.phone-input { flex: 1; border: none; padding: 12px; font-size: 16px; outline: none; }
.phone-actions, .popup-actions { margin-top: 20px; }

.password-form { margin-bottom: 20px; }
.form-item { margin-bottom: 16px; }
.form-input { width: 100%; border: 1px solid #ddd; border-radius: 6px; padding: 12px; font-size: 16px; outline: none; box-sizing: border-box; }
.form-input:focus { border-color: #1989fa; }
</style>
