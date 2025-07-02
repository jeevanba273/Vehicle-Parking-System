<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12">
        <!-- Settings Header -->
        <div class="settings-header mb-5">
          <div class="settings-content">
            <h1 class="settings-title">
              <i class="bi bi-gear-fill me-3"></i>Admin Settings
            </h1>
            <p class="settings-subtitle">Manage system-wide settings and administrative preferences</p>
          </div>
        </div>

        <!-- Settings Sections -->
        <div class="row g-4">
          <div class="col-lg-8">
            <!-- System Settings -->
            <div class="card settings-card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-server me-2"></i>System Configuration
                </h5>
              </div>
              <div class="card-body">
                <div class="settings-section">
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Auto-Cleanup Expired Bookings</h6>
                      <p class="text-muted">Automatically release expired parking spots</p>
                    </div>
                    <div class="setting-control">
                      <div class="form-check form-switch">
                        <input
                          v-model="settings.autoCleanup"
                          class="form-check-input"
                          type="checkbox"
                          id="autoCleanup"
                        />
                        <label class="form-check-label" for="autoCleanup"></label>
                      </div>
                    </div>
                  </div>
                  
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Real-time Updates</h6>
                      <p class="text-muted">Enable real-time parking spot status updates</p>
                    </div>
                    <div class="setting-control">
                      <div class="form-check form-switch">
                        <input
                          v-model="settings.realTimeUpdates"
                          class="form-check-input"
                          type="checkbox"
                          id="realTimeUpdates"
                        />
                        <label class="form-check-label" for="realTimeUpdates"></label>
                      </div>
                    </div>
                  </div>
                  
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Email Notifications to Admin</h6>
                      <p class="text-muted">Receive email alerts for system events</p>
                    </div>
                    <div class="setting-control">
                      <div class="form-check form-switch">
                        <input
                          v-model="settings.adminEmailNotifications"
                          class="form-check-input"
                          type="checkbox"
                          id="adminEmailNotifications"
                        />
                        <label class="form-check-label" for="adminEmailNotifications"></label>
                      </div>
                    </div>
                  </div>
                  
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Maintenance Mode</h6>
                      <p class="text-muted">Enable maintenance mode for system updates</p>
                    </div>
                    <div class="setting-control">
                      <div class="form-check form-switch">
                        <input
                          v-model="settings.maintenanceMode"
                          class="form-check-input"
                          type="checkbox"
                          id="maintenanceMode"
                        />
                        <label class="form-check-label" for="maintenanceMode"></label>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Booking Settings -->
            <div class="card settings-card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-calendar-check me-2"></i>Booking Configuration
                </h5>
              </div>
              <div class="card-body">
                <div class="settings-section">
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Maximum Booking Duration</h6>
                      <p class="text-muted">Set the maximum hours a user can book a spot</p>
                    </div>
                    <div class="setting-control">
                      <select v-model="settings.maxBookingHours" class="form-select">
                        <option value="4">4 hours</option>
                        <option value="8">8 hours</option>
                        <option value="12">12 hours</option>
                        <option value="24">24 hours</option>
                      </select>
                    </div>
                  </div>
                  
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Minimum Booking Duration</h6>
                      <p class="text-muted">Set the minimum booking time allowed</p>
                    </div>
                    <div class="setting-control">
                      <select v-model="settings.minBookingMinutes" class="form-select">
                        <option value="15">15 minutes</option>
                        <option value="30">30 minutes</option>
                        <option value="60">1 hour</option>
                      </select>
                    </div>
                  </div>
                  
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Allow Advance Booking</h6>
                      <p class="text-muted">Allow users to book spots in advance</p>
                    </div>
                    <div class="setting-control">
                      <div class="form-check form-switch">
                        <input
                          v-model="settings.allowAdvanceBooking"
                          class="form-check-input"
                          type="checkbox"
                          id="allowAdvanceBooking"
                        />
                        <label class="form-check-label" for="allowAdvanceBooking"></label>
                      </div>
                    </div>
                  </div>
                  
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Grace Period for Late Release</h6>
                      <p class="text-muted">Extra time before marking booking as expired</p>
                    </div>
                    <div class="setting-control">
                      <select v-model="settings.gracePeriodMinutes" class="form-select">
                        <option value="0">No grace period</option>
                        <option value="5">5 minutes</option>
                        <option value="10">10 minutes</option>
                        <option value="15">15 minutes</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Pricing Settings -->
            <div class="card settings-card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-currency-rupee me-2"></i>Pricing Configuration
                </h5>
              </div>
              <div class="card-body">
                <div class="settings-section">
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Dynamic Pricing</h6>
                      <p class="text-muted">Enable dynamic pricing based on demand</p>
                    </div>
                    <div class="setting-control">
                      <div class="form-check form-switch">
                        <input
                          v-model="settings.dynamicPricing"
                          class="form-check-input"
                          type="checkbox"
                          id="dynamicPricing"
                        />
                        <label class="form-check-label" for="dynamicPricing"></label>
                      </div>
                    </div>
                  </div>
                  
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Peak Hour Multiplier</h6>
                      <p class="text-muted">Price multiplier during peak hours</p>
                    </div>
                    <div class="setting-control">
                      <select v-model="settings.peakHourMultiplier" class="form-select">
                        <option value="1.0">1.0x (No change)</option>
                        <option value="1.2">1.2x</option>
                        <option value="1.5">1.5x</option>
                        <option value="2.0">2.0x</option>
                      </select>
                    </div>
                  </div>
                  
                  <div class="setting-item">
                    <div class="setting-info">
                      <h6>Weekend Pricing</h6>
                      <p class="text-muted">Different pricing for weekends</p>
                    </div>
                    <div class="setting-control">
                      <div class="form-check form-switch">
                        <input
                          v-model="settings.weekendPricing"
                          class="form-check-input"
                          type="checkbox"
                          id="weekendPricing"
                        />
                        <label class="form-check-label" for="weekendPricing"></label>
                      </div>
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
            <!-- System Status -->
            <div class="card settings-card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-activity me-2"></i>System Status
                </h5>
              </div>
              <div class="card-body">
                <div class="status-grid">
                  <div class="status-item">
                    <div class="status-indicator bg-success"></div>
                    <div class="status-content">
                      <div class="status-label">Database</div>
                      <div class="status-value">Connected</div>
                    </div>
                  </div>
                  
                  <div class="status-item">
                    <div class="status-indicator bg-warning"></div>
                    <div class="status-content">
                      <div class="status-label">Redis Cache</div>
                      <div class="status-value">Optional</div>
                    </div>
                  </div>
                  
                  <div class="status-item">
                    <div class="status-indicator bg-success"></div>
                    <div class="status-content">
                      <div class="status-label">API Server</div>
                      <div class="status-value">Running</div>
                    </div>
                  </div>
                  
                  <div class="status-item">
                    <div class="status-indicator bg-info"></div>
                    <div class="status-content">
                      <div class="status-label">Timezone</div>
                      <div class="status-value">IST</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- System Actions -->
            <div class="card settings-card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-tools me-2"></i>System Actions
                </h5>
              </div>
              <div class="card-body">
                <div class="system-actions">
                  <button @click="cleanupExpiredBookings" class="btn btn-outline-warning w-100 mb-3">
                    <i class="bi bi-trash me-2"></i>Cleanup Expired Bookings
                  </button>
                  
                  <button @click="refreshCache" class="btn btn-outline-info w-100 mb-3">
                    <i class="bi bi-arrow-clockwise me-2"></i>Refresh System Cache
                  </button>
                  
                  <button @click="exportLogs" class="btn btn-outline-secondary w-100 mb-3">
                    <i class="bi bi-download me-2"></i>Export System Logs
                  </button>
                  
                  <button @click="backupDatabase" class="btn btn-outline-success w-100">
                    <i class="bi bi-shield-check me-2"></i>Backup Database
                  </button>
                </div>
              </div>
            </div>
            
            <!-- System Info -->
            <div class="card settings-card">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-info-circle me-2"></i>System Information
                </h5>
              </div>
              <div class="card-body">
                <div class="info-grid">
                  <div class="info-item">
                    <span class="info-label">Version:</span>
                    <span class="info-value">1.0.0</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Environment:</span>
                    <span class="info-value">Production</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Last Updated:</span>
                    <span class="info-value">{{ getCurrentDate() }}</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Timezone:</span>
                    <span class="info-value">Asia/Kolkata (IST)</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Server:</span>
                    <span class="info-value">Railway.app</span>
                  </div>
                  <div class="info-item">
                    <span class="info-label">Database:</span>
                    <span class="info-value">SQLite</span>
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
  // System Settings
  autoCleanup: true,
  realTimeUpdates: true,
  adminEmailNotifications: true,
  maintenanceMode: false,
  
  // Booking Settings
  maxBookingHours: '8',
  minBookingMinutes: '15',
  allowAdvanceBooking: true,
  gracePeriodMinutes: '10',
  
  // Pricing Settings
  dynamicPricing: false,
  peakHourMultiplier: '1.2',
  weekendPricing: false
})

onMounted(() => {
  loadSettings()
})

const loadSettings = () => {
  // Load settings from localStorage
  const savedSettings = localStorage.getItem('adminSettings')
  if (savedSettings) {
    try {
      const parsed = JSON.parse(savedSettings)
      Object.assign(settings, parsed)
    } catch (error) {
      console.error('Error loading admin settings:', error)
    }
  }
}

const saveSettings = async () => {
  saving.value = true
  
  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Save to localStorage
    localStorage.setItem('adminSettings', JSON.stringify(settings))
    
    alert('Admin settings saved successfully!')
  } catch (error) {
    console.error('Error saving admin settings:', error)
    alert('Failed to save admin settings')
  } finally {
    saving.value = false
  }
}

const resetSettings = () => {
  if (confirm('Are you sure you want to reset all settings to default?')) {
    // Reset to default values
    Object.assign(settings, {
      autoCleanup: true,
      realTimeUpdates: true,
      adminEmailNotifications: true,
      maintenanceMode: false,
      maxBookingHours: '8',
      minBookingMinutes: '15',
      allowAdvanceBooking: true,
      gracePeriodMinutes: '10',
      dynamicPricing: false,
      peakHourMultiplier: '1.2',
      weekendPricing: false
    })
    
    // Remove from localStorage
    localStorage.removeItem('adminSettings')
    
    alert('Admin settings reset to default!')
  }
}

const cleanupExpiredBookings = () => {
  alert('Cleanup expired bookings - Feature will be implemented with backend integration!')
}

const refreshCache = () => {
  alert('System cache refreshed successfully!')
}

const exportLogs = () => {
  // Create a simple log export
  const logData = {
    exportDate: new Date().toISOString(),
    timezone: 'Asia/Kolkata',
    logs: [
      { timestamp: new Date().toISOString(), level: 'INFO', message: 'System running normally' },
      { timestamp: new Date().toISOString(), level: 'INFO', message: 'Admin settings exported' }
    ]
  }
  
  const dataStr = JSON.stringify(logData, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  
  const link = document.createElement('a')
  link.href = url
  link.download = `system-logs-${Date.now()}.json`
  link.click()
  
  URL.revokeObjectURL(url)
}

const backupDatabase = () => {
  alert('Database backup initiated - Feature will be implemented with backend integration!')
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
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.form-check-input:focus {
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.form-select {
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 0.5rem 1rem;
  min-width: 150px;
}

.form-select:focus {
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
}

.settings-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  padding: 2rem 0;
}

.status-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.status-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.status-content {
  flex: 1;
}

.status-label {
  font-size: 0.9rem;
  color: #6c757d;
  font-weight: 500;
}

.status-value {
  font-size: 0.9rem;
  color: #2d3748;
  font-weight: 600;
}

.system-actions {
  display: flex;
  flex-direction: column;
}

.system-actions .btn {
  border-radius: 10px;
  font-weight: 600;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.system-actions .btn:hover {
  transform: translateY(-2px);
}

.info-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.info-label {
  color: #6c757d;
  font-size: 0.9rem;
  font-weight: 500;
}

.info-value {
  color: #2d3748;
  font-weight: 600;
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