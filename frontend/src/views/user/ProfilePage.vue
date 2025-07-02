<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12">
        <!-- Profile Header -->
        <div class="profile-header mb-5">
          <div class="profile-content">
            <div class="d-flex align-items-center mb-4">
              <div class="profile-avatar me-4">
                {{ getInitials(authStore.currentUser?.fullname || '') }}
              </div>
              <div>
                <h1 class="profile-title">{{ authStore.currentUser?.fullname }}</h1>
                <p class="profile-subtitle">{{ authStore.currentUser?.email }}</p>
                <div class="profile-badges">
                  <span class="badge bg-success">
                    <i class="bi bi-check-circle me-1"></i>Verified User
                  </span>
                  <span class="badge bg-info">
                    <i class="bi bi-geo-alt me-1"></i>Bangalore
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Profile Information -->
        <div class="row g-4">
          <div class="col-lg-8">
            <div class="card profile-card">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-person-circle me-2"></i>Personal Information
                </h5>
              </div>
              <div class="card-body">
                <form @submit.prevent="updateProfile" class="profile-form">
                  <div class="row g-3">
                    <div class="col-md-6">
                      <label class="form-label">Full Name</label>
                      <input
                        v-model="profileForm.fullname"
                        type="text"
                        class="form-control"
                        required
                      />
                    </div>
                    
                    <div class="col-md-6">
                      <label class="form-label">Email Address</label>
                      <input
                        v-model="profileForm.email"
                        type="email"
                        class="form-control"
                        readonly
                        disabled
                      />
                      <small class="form-text text-muted">Email cannot be changed</small>
                    </div>
                    
                    <div class="col-12">
                      <label class="form-label">Address in Bangalore</label>
                      <textarea
                        v-model="profileForm.address"
                        class="form-control"
                        rows="3"
                        required
                      ></textarea>
                    </div>
                    
                    <div class="col-md-6">
                      <label class="form-label">PIN Code</label>
                      <input
                        v-model="profileForm.pin_code"
                        type="text"
                        class="form-control"
                        pattern="[0-9]{6}"
                        maxlength="6"
                        required
                      />
                    </div>
                    
                    <div class="col-md-6">
                      <label class="form-label">Member Since</label>
                      <input
                        :value="formatMemberSince()"
                        type="text"
                        class="form-control"
                        readonly
                        disabled
                      />
                    </div>
                  </div>
                  
                  <div class="form-actions mt-4">
                    <button
                      type="submit"
                      class="btn btn-primary"
                      :disabled="updating"
                    >
                      <span v-if="updating" class="spinner-border spinner-border-sm me-2"></span>
                      <i v-else class="bi bi-check-circle me-2"></i>
                      {{ updating ? 'Updating...' : 'Update Profile' }}
                    </button>
                    <button
                      type="button"
                      @click="resetForm"
                      class="btn btn-outline-secondary"
                    >
                      <i class="bi bi-arrow-clockwise me-2"></i>Reset
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
          
          <div class="col-lg-4">
            <!-- Account Stats -->
            <div class="card profile-card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-graph-up me-2"></i>Account Statistics
                </h5>
              </div>
              <div class="card-body">
                <div class="stats-grid">
                  <div class="stat-item">
                    <div class="stat-icon bg-primary">
                      <i class="bi bi-calendar-check"></i>
                    </div>
                    <div class="stat-content">
                      <div class="stat-number">{{ totalBookings }}</div>
                      <div class="stat-label">Total Bookings</div>
                    </div>
                  </div>
                  
                  <div class="stat-item">
                    <div class="stat-icon bg-success">
                      <i class="bi bi-clock-history"></i>
                    </div>
                    <div class="stat-content">
                      <div class="stat-number">{{ activeBookings }}</div>
                      <div class="stat-label">Active Bookings</div>
                    </div>
                  </div>
                  
                  <div class="stat-item">
                    <div class="stat-icon bg-warning">
                      <i class="bi bi-currency-rupee"></i>
                    </div>
                    <div class="stat-content">
                      <div class="stat-number">₹{{ totalSpent.toFixed(0) }}</div>
                      <div class="stat-label">Total Spent</div>
                    </div>
                  </div>
                  
                  <div class="stat-item">
                    <div class="stat-icon bg-info">
                      <i class="bi bi-star"></i>
                    </div>
                    <div class="stat-content">
                      <div class="stat-number">{{ membershipLevel }}</div>
                      <div class="stat-label">Membership</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Quick Actions -->
            <div class="card profile-card">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-lightning me-2"></i>Quick Actions
                </h5>
              </div>
              <div class="card-body">
                <div class="quick-actions">
                  <router-link to="/user/book-spot" class="btn btn-success w-100 mb-3">
                    <i class="bi bi-plus-circle me-2"></i>Book New Spot
                  </router-link>
                  
                  <router-link to="/user/history" class="btn btn-outline-primary w-100 mb-3">
                    <i class="bi bi-clock-history me-2"></i>View Booking History
                  </router-link>
                  
                  <button @click="downloadData" class="btn btn-outline-info w-100">
                    <i class="bi bi-download me-2"></i>Download My Data
                  </button>
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
import { ref, reactive, onMounted, computed } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { getApiUrl } from '../../config/api'

const authStore = useAuthStore()

const updating = ref(false)
const totalBookings = ref(0)
const activeBookings = ref(0)
const totalSpent = ref(0)

const profileForm = reactive({
  fullname: '',
  email: '',
  address: '',
  pin_code: ''
})

const membershipLevel = computed(() => {
  if (totalSpent.value >= 5000) return 'Gold'
  if (totalSpent.value >= 2000) return 'Silver'
  return 'Bronze'
})

onMounted(() => {
  loadProfile()
  loadStats()
})

const loadProfile = () => {
  if (authStore.currentUser) {
    profileForm.fullname = authStore.currentUser.fullname
    profileForm.email = authStore.currentUser.email
    profileForm.address = authStore.currentUser.address
    profileForm.pin_code = authStore.currentUser.pin_code
  }
}

const loadStats = async () => {
  if (!authStore.currentUser) return
  
  try {
    const response = await fetch(getApiUrl(`/api/users/${authStore.currentUser.id}/bookings`))
    if (response.ok) {
      const bookings = await response.json()
      totalBookings.value = bookings.length
      activeBookings.value = bookings.filter((b: any) => b.status === 'active').length
      totalSpent.value = bookings.reduce((sum: number, b: any) => sum + b.total_cost, 0)
    }
  } catch (error) {
    console.error('Error loading stats:', error)
  }
}

const updateProfile = async () => {
  updating.value = true
  
  try {
    // Simulate API call - in real app, this would update the backend
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Update local store
    if (authStore.currentUser) {
      authStore.currentUser.fullname = profileForm.fullname
      authStore.currentUser.address = profileForm.address
      authStore.currentUser.pin_code = profileForm.pin_code
      
      // Update localStorage
      localStorage.setItem('currentUser', JSON.stringify(authStore.currentUser))
    }
    
    alert('Profile updated successfully!')
  } catch (error) {
    console.error('Error updating profile:', error)
    alert('Failed to update profile')
  } finally {
    updating.value = false
  }
}

const resetForm = () => {
  loadProfile()
}

const getInitials = (name: string) => {
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const formatMemberSince = () => {
  if (!authStore.currentUser?.created_at) return 'N/A'
  
  const date = new Date(authStore.currentUser.created_at)
  return date.toLocaleDateString('en-IN', {
    timeZone: 'Asia/Kolkata',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const downloadData = () => {
  // Create a simple data export
  const userData = {
    profile: authStore.currentUser,
    stats: {
      totalBookings: totalBookings.value,
      activeBookings: activeBookings.value,
      totalSpent: totalSpent.value,
      membershipLevel: membershipLevel.value
    },
    exportDate: new Date().toISOString()
  }
  
  const dataStr = JSON.stringify(userData, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  
  const link = document.createElement('a')
  link.href = url
  link.download = `parkease-data-${Date.now()}.json`
  link.click()
  
  URL.revokeObjectURL(url)
}
</script>

<style scoped>
.profile-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  padding: 2rem;
  color: white;
  position: relative;
  overflow: hidden;
}

.profile-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
  opacity: 0.3;
}

.profile-content {
  position: relative;
  z-index: 2;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  backdrop-filter: blur(10px);
  border: 3px solid rgba(255,255,255,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 800;
  color: white;
}

.profile-title {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 0.25rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.profile-subtitle {
  font-size: 1.1rem;
  opacity: 0.9;
  margin-bottom: 1rem;
}

.profile-badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.profile-badges .badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.profile-card {
  border-radius: 16px;
  border: none;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
}

.profile-card:hover {
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

.profile-form {
  padding: 1rem 0;
}

.form-label {
  color: #495057;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.form-control {
  border: 2px solid #e9ecef;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.form-control:disabled {
  background-color: #f8f9fa;
  opacity: 0.8;
}

.form-text {
  color: #6c757d;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-start;
  padding-top: 1rem;
  border-top: 1px solid #dee2e6;
}

.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.stat-item:hover {
  background: #e9ecef;
  transform: translateY(-2px);
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.2rem;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 1.2rem;
  font-weight: 700;
  color: #2d3748;
  line-height: 1;
}

.stat-label {
  font-size: 0.8rem;
  color: #6c757d;
  font-weight: 500;
}

.quick-actions {
  display: flex;
  flex-direction: column;
}

.quick-actions .btn {
  border-radius: 10px;
  font-weight: 600;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
}

.quick-actions .btn:hover {
  transform: translateY(-2px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .profile-header {
    padding: 1.5rem;
  }
  
  .profile-title {
    font-size: 1.5rem;
  }
  
  .profile-avatar {
    width: 60px;
    height: 60px;
    font-size: 1.5rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
  
  .form-actions .btn {
    width: 100%;
  }
}

@media (max-width: 576px) {
  .profile-header .d-flex {
    flex-direction: column;
    text-align: center;
  }
  
  .profile-avatar {
    margin: 0 auto 1rem;
  }
  
  .card-header {
    padding: 1rem;
  }
  
  .card-body {
    padding: 1rem;
  }
}
</style>