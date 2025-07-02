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
                  <span class="badge bg-warning text-dark">
                    <i class="bi bi-shield-check me-1"></i>Administrator
                  </span>
                  <span class="badge bg-info">
                    <i class="bi bi-geo-alt me-1"></i>Bangalore Parking Authority
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
                  <i class="bi bi-person-circle me-2"></i>Administrator Information
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
                      <small class="form-text text-muted">Admin email cannot be changed</small>
                    </div>
                    
                    <div class="col-12">
                      <label class="form-label">Office Address</label>
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
                      <label class="form-label">Admin Since</label>
                      <input
                        :value="formatAdminSince()"
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
            <!-- System Stats -->
            <div class="card profile-card mb-4">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-graph-up me-2"></i>System Overview
                </h5>
              </div>
              <div class="card-body">
                <div class="stats-grid">
                  <div class="stat-item">
                    <div class="stat-icon bg-primary">
                      <i class="bi bi-building"></i>
                    </div>
                    <div class="stat-content">
                      <div class="stat-number">{{ systemStats.totalLots }}</div>
                      <div class="stat-label">Parking Lots</div>
                    </div>
                  </div>
                  
                  <div class="stat-item">
                    <div class="stat-icon bg-success">
                      <i class="bi bi-people"></i>
                    </div>
                    <div class="stat-content">
                      <div class="stat-number">{{ systemStats.totalUsers }}</div>
                      <div class="stat-label">Registered Users</div>
                    </div>
                  </div>
                  
                  <div class="stat-item">
                    <div class="stat-icon bg-warning">
                      <i class="bi bi-calendar-check"></i>
                    </div>
                    <div class="stat-content">
                      <div class="stat-number">{{ systemStats.totalBookings }}</div>
                      <div class="stat-label">Total Bookings</div>
                    </div>
                  </div>
                  
                  <div class="stat-item">
                    <div class="stat-icon bg-info">
                      <i class="bi bi-currency-rupee"></i>
                    </div>
                    <div class="stat-content">
                      <div class="stat-number">₹{{ systemStats.totalRevenue.toFixed(0) }}</div>
                      <div class="stat-label">Total Revenue</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Admin Actions -->
            <div class="card profile-card">
              <div class="card-header">
                <h5 class="card-title mb-0">
                  <i class="bi bi-lightning me-2"></i>Admin Actions
                </h5>
              </div>
              <div class="card-body">
                <div class="admin-actions">
                  <router-link to="/admin/parking-lots" class="btn btn-primary w-100 mb-3">
                    <i class="bi bi-building me-2"></i>Manage Parking Lots
                  </router-link>
                  
                  <router-link to="/admin/users" class="btn btn-outline-success w-100 mb-3">
                    <i class="bi bi-people me-2"></i>View All Users
                  </router-link>
                  
                  <router-link to="/admin/analytics" class="btn btn-outline-info w-100 mb-3">
                    <i class="bi bi-graph-up me-2"></i>View Analytics
                  </router-link>
                  
                  <button @click="exportSystemData" class="btn btn-outline-warning w-100">
                    <i class="bi bi-download me-2"></i>Export System Data
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
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'
import { getApiUrl } from '../../config/api'

const authStore = useAuthStore()

const updating = ref(false)
const systemStats = reactive({
  totalLots: 0,
  totalUsers: 0,
  totalBookings: 0,
  totalRevenue: 0
})

const profileForm = reactive({
  fullname: '',
  email: '',
  address: '',
  pin_code: ''
})

onMounted(() => {
  loadProfile()
  loadSystemStats()
})

const loadProfile = () => {
  if (authStore.currentUser) {
    profileForm.fullname = authStore.currentUser.fullname
    profileForm.email = authStore.currentUser.email
    profileForm.address = authStore.currentUser.address
    profileForm.pin_code = authStore.currentUser.pin_code
  }
}

const loadSystemStats = async () => {
  try {
    // Load analytics data
    const analyticsResponse = await fetch(getApiUrl('/api/analytics'))
    if (analyticsResponse.ok) {
      const analytics = await analyticsResponse.json()
      systemStats.totalLots = analytics.total_lots || 0
      systemStats.totalBookings = analytics.total_bookings || 0
      systemStats.totalRevenue = analytics.total_revenue || 0
    }
    
    // Load users count
    const usersResponse = await fetch(getApiUrl('/api/users'))
    if (usersResponse.ok) {
      const users = await usersResponse.json()
      systemStats.totalUsers = users.length || 0
    }
  } catch (error) {
    console.error('Error loading system stats:', error)
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
    
    alert('Admin profile updated successfully!')
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

const formatAdminSince = () => {
  if (!authStore.currentUser?.created_at) return 'N/A'
  
  const date = new Date(authStore.currentUser.created_at)
  return date.toLocaleDateString('en-IN', {
    timeZone: 'Asia/Kolkata',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const exportSystemData = async () => {
  try {
    // Gather all system data
    const [analyticsRes, usersRes, lotsRes] = await Promise.all([
      fetch(getApiUrl('/api/analytics')),
      fetch(getApiUrl('/api/users')),
      fetch(getApiUrl('/api/parking-lots'))
    ])
    
    const analytics = analyticsRes.ok ? await analyticsRes.json() : {}
    const users = usersRes.ok ? await usersRes.json() : []
    const lots = lotsRes.ok ? await lotsRes.json() : []
    
    const systemData = {
      exportInfo: {
        exportedBy: authStore.currentUser?.fullname,
        exportDate: new Date().toISOString(),
        timezone: 'Asia/Kolkata (IST)'
      },
      analytics,
      users: users.map((user: any) => ({
        id: user.id,
        fullname: user.fullname,
        email: user.email,
        created_at: user.created_at,
        bookings_count: user.bookings_count,
        active_bookings: user.active_bookings
      })),
      parkingLots: lots,
      summary: {
        totalLots: lots.length,
        totalUsers: users.length,
        totalRevenue: analytics.total_revenue || 0,
        totalBookings: analytics.total_bookings || 0
      }
    }
    
    const dataStr = JSON.stringify(systemData, null, 2)
    const dataBlob = new Blob([dataStr], { type: 'application/json' })
    const url = URL.createObjectURL(dataBlob)
    
    const link = document.createElement('a')
    link.href = url
    link.download = `bangalore-parking-system-data-${Date.now()}.json`
    link.click()
    
    URL.revokeObjectURL(url)
    alert('System data exported successfully!')
  } catch (error) {
    console.error('Error exporting system data:', error)
    alert('Failed to export system data')
  }
}
</script>

<style scoped>
.profile-header {
  background: linear-gradient(135deg, #0d6efd 0%, #6610f2 100%);
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
  border-color: #0d6efd;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
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

.admin-actions {
  display: flex;
  flex-direction: column;
}

.admin-actions .btn {
  border-radius: 10px;
  font-weight: 600;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
  text-decoration: none;
}

.admin-actions .btn:hover {
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