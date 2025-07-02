<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12">
        <!-- Settings Header -->
        <div class="settings-header mb-5">
          <div class="settings-content">
            <h1 class="settings-title">
              <i class="bi bi-gear-fill me-3"></i>Settings
            </h1>
            <p class="settings-subtitle">Manage your account preferences and application settings</p>
          </div>
        </div>

        <!-- Settings Sections -->
        <div class="row g-4">
          <div class="col-lg-8">
            <!-- Notification Settings -->
            <div class="card settings-card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-bell me-2"></i>Notification Preferences
                </h5>
              </div>
              <div class="card-body">
                <div class="settings-section">
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Email Notifications</h6>
                      <p class="text-muted">Receive booking confirmations and updates via email</p>
                    </div>
                    <div class="setting-control">
                      <div class="form-check form-switch">
                        <input
                          v-model="settings.emailNotifications"
                          class="form-check-input"
                          type="checkbox"
                          id="emailNotifications"
                        />
                        <label class="form-check-label" for="emailNotifications"></label>
                      </div>
                    </div>
                  </div>
                  
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>SMS Notifications</h6>
                      <p class="text-muted">Get SMS alerts for booking reminders and updates</p>
                    </div>
                    <div class="setting-control">
                      <div class="form-check form-switch">
                        <input
                          v-model="settings.smsNotifications"
                          class="form-check-input"
                          type="checkbox"
                          id="smsNotifications"
                        />
                        <label class="form-check-label" for="smsNotifications"></label>
                      </div>
                    </div>
                  </div>
                  
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Push Notifications</h6>
                      <p class="text-muted">Receive real-time notifications in your browser</p>
                    </div>
                    <div class="setting-control">
                      <div class="form-check form-switch">
                        <input
                          v-model="settings.pushNotifications"
                          class="form-check-input"
                          type="checkbox"
                          id="pushNotifications"
                        />
                        <label class="form-check-label" for="pushNotifications"></label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Privacy Settings -->
            <div class="card settings-card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-shield-lock me-2"></i>Privacy & Security
                </h5>
              </div>
              <div class="card-body">
                <div class="settings-section">
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Profile Visibility</h6>
                      <p class="text-muted">Control who can see your profile information</p>
                    </div>
                    <div class="setting-control">
                      <select v-model="settings.profileVisibility" class="form-select">
                        <option value="private">Private</option>
                        <option value="public">Public</option>
                        <option value="friends">Friends Only</option>
                      </select>
                    </div>
                  </div>
                  
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Data Sharing</h6>
                      <p class="text-muted">Allow anonymous usage data to improve our services</p>
                    </div>
                    <div class="setting-control">
                      <div class="form-check form-switch">
                        <input
                          v-model="settings.dataSharing"
                          class="form-check-input"
                          type="checkbox"
                          id="dataSharing"
                        />
                        <label class="form-check-label" for="dataSharing"></label>
                      </div>
                    </div>
                  </div>
                  
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Two-Factor Authentication</h6>
                      <p class="text-muted">Add an extra layer of security to your account</p>
                    </div>
                    <div class="setting-control">
                      <button class="btn btn-outline-primary btn-sm">
                        <i class="bi bi-shield-plus me-2"></i>Enable 2FA
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- App Preferences -->
            <div class="card settings-card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-sliders me-2"></i>App Preferences
                </h5>
              </div>
              <div class="card-body">
                <div class="settings-section">
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Theme</h6>
                      <p class="text-muted">Choose your preferred app theme</p>
                    </div>
                    <div class="setting-control">
                      <select v-model="settings.theme" class="form-select">
                        <option value="light">Light</option>
                        <option value="dark">Dark</option>
                        <option value="auto">Auto (System)</option>
                      </select>
                    </div>
                  </div>
                  
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Language</h6>
                      <p class="text-muted">Select your preferred language</p>
                    </div>
                    <div class="setting-control">
                      <select v-model="settings.language" class="form-select">
                        <option value="en">English</option>
                        <option value="hi">हिंदी (Hindi)</option>
                        <option value="kn">ಕನ್ನಡ (Kannada)</option>
                        <option value="ta">தமிழ் (Tamil)</option>
                      </select>
                    </div>
                  </div>
                  
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Auto-Refresh</h6>
                      <p class="text-muted">Automatically refresh parking availability</p>
                    </div>
                    <div class="setting-control">
                      <div class="form-check form-switch">
                        <input
                          v-model="settings.autoRefresh"
                          class="form-check-input"
                          type="checkbox"
                          id="autoRefresh"
                        />
                        <label class="form-check-label" for="autoRefresh"></label>
                      </div>
                    </div>
                  </div>
                  
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Default Booking Duration</h6>
                      <p class="text-muted">Set your preferred default parking duration</p>
                    </div>
                    <div class="setting-control">
                      <select v-model="settings.defaultDuration" class="form-select">
                        <option value="0.5">30 minutes</option>
                        <option value="1">1 hour</option>
                        <option value="2">2 hours</option>
                        <option value="4">4 hours</option>
                        <option value="8">8 hours</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Save Settings -->
            <div class="settings-actions">
              <button
                @click="saveSettings"
                class="btn btn-primary btn-lg"
                :disabled="saving"
              >
                <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else class="bi bi-check-circle me-2"></i>
                {{ saving ? 'Saving...' : 'Save Settings' }}
              </button>
              <button
                @click="resetSettings"
                class="btn btn-outline-secondary btn-lg"
              >
                <i class="bi bi-arrow-clockwise me-2"></i>Reset to Default
              </button>
            </div>
          </div>
          
          <div class="col-lg-4">
            <!-- Account Actions -->
            <div class="card settings-card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-person-gear me-2"></i>Account Actions
                </h5>
              </div>
              <div class="card-body">
                <div class="account-actions">
                  <button @click="changePassword" class="btn btn-outline-warning w-100 mb-3">
                    <i class="bi bi-key me-2"></i>Change Password
                  </button>
                  
                  <button @click="exportData" class="btn btn-outline-info w-100 mb-3">
                    <i class="bi bi-download me-2"></i>Export My Data
                  </button>
                  
                  <button @click="deactivateAccount" class="btn btn-outline-danger w-100">
                    <i class="bi bi-person-x me-2"></i>Deactivate Account
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Help & Support -->
            <div class="card settings-card">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-question-circle me-2"></i>Help & Support
                </h5>
              </div>
              <div class="card-body">
                <div class="help-links">
                  <a href="#" class="help-link">
                    <i class="bi bi-book me-2"></i>User Guide
                  </a>
                  
                  <a href="#" class="help-link">
                    <i class="bi bi-chat-dots me-2"></i>Contact Support
                  </a>
                  
                  <a href="#" class="help-link">
                    <i class="bi bi-bug me-2"></i>Report a Bug
                  </a>
                  
                  <a href="#" class="help-link">
                    <i class="bi bi-star me-2"></i>Rate Our App
                  </a>
                </div>
                
                <div class="app-info mt-4">
                  <h6>App Information</h6>
                  <div class="info-grid">
                    <div class="info-item">
                      <span class="info-label">Version:</span>
                      <span class="info-value">1.0.0</span>
                    </div>
                    <div class="info-item">
                      <span class="info-label">Last Updated:</span>
                      <span class="info-value">{{ getCurrentDate() }}</span>
                    </div>
                    <div class="info-item">
                      <span class="info-label">Timezone:</span>
                      <span class="info-value">IST (Asia/Kolkata)</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'

const saving = ref(false)

const settings = reactive({
  // Notifications
  emailNotifications: true,
  smsNotifications: false,
  pushNotifications: true,
  
  // Privacy
  profileVisibility: 'private',
  dataSharing: false,
  
  // App Preferences
  theme: 'light',
  language: 'en',
  autoRefresh: true,
  defaultDuration: '1'
})

onMounted(() => {
  loadSettings()
})

const loadSettings = () => {
  // Load settings from localStorage
  const savedSettings = localStorage.getItem('userSettings')
  if (savedSettings) {
    try {
      const parsed = JSON.parse(savedSettings)
      Object.assign(settings, parsed)
    } catch (error) {
      console.error('Error loading settings:', error)
    }
  }
}

const saveSettings = async () => {
  saving.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Save to localStorage
    localStorage.setItem('userSettings', JSON.stringify(settings))
    
    alert('Settings saved successfully!')
  } catch (error) {
    console.error('Error saving settings:', error)
    alert('Failed to save settings')
  } finally {
    saving.value = false
  }
}

const resetSettings = () => {
  if (confirm('Are you sure you want to reset all settings to default?')) {
    // Reset to default values
    Object.assign(settings, {
      emailNotifications: true,
      smsNotifications: false,
      pushNotifications: true,
      profileVisibility: 'private',
      dataSharing: false,
      theme: 'light',
      language: 'en',
      autoRefresh: true,
      defaultDuration: '1'
    })
    
    // Remove from localStorage
    localStorage.removeItem('userSettings')
    
    alert('Settings reset to default!')
  }
}

const changePassword = () => {
  alert('Change Password feature - Coming soon!')
}

const exportData = () => {
  // Create a simple data export
  const userData = {
    settings: settings,
    exportDate: new Date().toISOString(),
    timezone: 'Asia/Kolkata'
  }
  
  const dataStr = JSON.stringify(userData, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  
  const link = document.createElement('a')
  link.href = url
  link.download = `parkease-settings-${Date.now()}.json`
  link.click()
  
  URL.revokeObjectURL(url)
}

const deactivateAccount = () => {
  if (confirm('Are you sure you want to deactivate your account? This action cannot be undone.')) {
    alert('Account deactivation feature - Coming soon!')
  }
}

const getCurrentDate = () => {
  return new Date().toLocaleDateString('en-IN', {
    timeZone: 'Asia/Kolkata',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.settings-header {
  background: linear-gradient(135deg, #6c757d 0%, #495057 100%);
  border-radius: 20px;
  padding: 2rem;
  color: white;
  position: relative;
  overflow: hidden;
}

.settings-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
  opacity: 0.3;
}

.settings-content {
  position: relative;
  z-index: 2;
}

.settings-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.settings-subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 0;
}

.settings-card {
  border-radius: 16px;
  border: none;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
}

.settings-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

.card-header {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
  border-radius: 16px 16px 0 0 !important;
  padding: 1.5rem;
}

.card-title {
  color: #495057;
  font-weight: 600;
}

.settings-section {
  padding: 1rem 0;
}

.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 0;
  border-bottom: 1px solid #f1f3f4;
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-info {
  flex: 1;
  margin-right: 2rem;
}

.setting-info h6 {
  color: #2d3748;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.setting-info p {
  color: #6c757d;
  margin-bottom: 0;
  font-size: 0.9rem;
}

.setting-control {
  flex-shrink: 0;
}

.form-check-input {
  width: 3rem;
  height: 1.5rem;
  border-radius: 1rem;
  background-color: #dee2e6;
  border: none;
  transition: all 0.3s ease;
}

.form-check-input:checked {
  background-color: #28a745;
  border-color: #28a745;
}

.form-check-input:focus {
  box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25);
}

.form-select {
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  min-width: 150px;
}

.form-select:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.settings-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  padding: 2rem 0;
}

.account-actions {
  display: flex;
  flex-direction: column;
}

.account-actions .btn {
  border-radius: 10px;
  font-weight: 600;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.account-actions .btn:hover {
  transform: translateY(-2px);
}

.help-links {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.help-link {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  text-decoration: none;
  color: #495057;
  font-weight: 500;
  transition: all 0.3s ease;
}

.help-link:hover {
  background: #e9ecef;
  color: #495057;
  transform: translateX(5px);
}

.app-info {
  padding-top: 1rem;
  border-top: 1px solid #dee2e6;
}

.app-info h6 {
  color: #495057;
  font-weight: 600;
  margin-bottom: 1rem;
}

.info-grid {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-label {
  color: #6c757d;
  font-size: 0.9rem;
}

.info-value {
  color: #2d3748;
  font-weight: 500;
  font-size: 0.9rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .settings-header {
    padding: 1.5rem;
  }
  
  .settings-title {
    font-size: 2rem;
  }
  
  .setting-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .setting-info {
    margin-right: 0;
  }
  
  .setting-control {
    width: 100%;
  }
  
  .form-select {
    width: 100%;
  }
  
  .settings-actions {
    flex-direction: column;
  }
  
  .settings-actions .btn {
    width: 100%;
  }
}

@media (max-width: 576px) {
  .card-header {
    padding: 1rem;
  }
  
  .card-body {
    padding: 1rem;
  }
  
  .setting-item {
    padding: 1rem 0;
  }
}
</style>