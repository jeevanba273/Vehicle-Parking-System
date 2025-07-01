<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="fw-bold text-dark">Registered Users</h2>
          <div class="d-flex align-items-center gap-3">
            <span class="badge bg-primary fs-6">Total Users: {{ users.length }}</span>
            <button @click="loadUsers" class="btn btn-outline-primary">
              <i class="bi bi-arrow-clockwise me-2"></i>Refresh
            </button>
          </div>
        </div>

        <!-- Search and Stats -->
        <div class="row g-4 mb-4">
          <div class="col-md-8">
            <div class="card">
              <div class="card-body">
                <div class="input-group">
                  <span class="input-group-text"><i class="bi bi-search"></i></span>
                  <input
                    v-model="searchQuery"
                    type="text"
                    class="form-control"
                    placeholder="Search users by name, email, or address..."
                  />
                </div>
              </div>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card bg-primary text-white">
              <div class="card-body text-center">
                <i class="bi bi-people display-4 mb-2"></i>
                <h3 class="fw-bold">{{ activeUsers }}</h3>
                <p class="mb-0">Active Users</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Users Table -->
        <div class="card shadow-sm">
          <div class="card-header bg-light">
            <h5 class="card-title mb-0">
              <i class="bi bi-table me-2"></i>User Directory
            </h5>
          </div>
          <div class="card-body p-0">
            <div class="table-responsive">
              <table class="table table-hover mb-0">
                <thead class="table-light">
                  <tr>
                    <th class="fw-bold">User</th>
                    <th class="fw-bold">Contact Information</th>
                    <th class="fw-bold">Booking Activity</th>
                    <th class="fw-bold">Joined Date</th>
                    <th class="fw-bold">Status</th>
                    <th class="fw-bold">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="user in filteredUsers"
                    :key="user.id"
                    class="animate-fade-in"
                  >
                    <td>
                      <div class="d-flex align-items-center">
                        <div class="avatar-circle me-3">
                          {{ getInitials(user.fullname) }}
                        </div>
                        <div>
                          <div class="fw-bold">{{ user.fullname }}</div>
                          <small class="text-muted">{{ user.email }}</small>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div>
                        <div class="text-sm">{{ user.address }}</div>
                        <small class="text-muted">PIN: {{ user.pin_code }}</small>
                      </div>
                    </td>
                    <td>
                      <div class="d-flex gap-3">
                        <div class="text-center">
                          <div class="fw-bold text-primary">{{ getUserBookingCount(user.id) }}</div>
                          <small class="text-muted">Total</small>
                        </div>
                        <div class="text-center">
                          <div class="fw-bold text-success">{{ getActiveBookingCount(user.id) }}</div>
                          <small class="text-muted">Active</small>
                        </div>
                      </div>
                    </td>
                    <td>
                      <div class="text-sm">{{ formatDate(user.created_at) }}</div>
                      <small class="text-muted">{{ getTimeAgo(user.created_at) }}</small>
                    </td>
                    <td>
                      <span class="badge bg-success">
                        <i class="bi bi-check-circle me-1"></i>Active
                      </span>
                    </td>
                    <td>
                      <div class="btn-group btn-group-sm">
                        <button class="btn btn-outline-primary" @click="viewUserDetails(user)">
                          <i class="bi bi-eye"></i>
                        </button>
                        <button class="btn btn-outline-info" @click="viewUserBookings(user)">
                          <i class="bi bi-calendar-check"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
        
        <div v-if="filteredUsers.length === 0" class="text-center py-5">
          <div class="text-muted">
            <i class="bi bi-person-x display-1"></i>
            <h4 class="mt-3">No users found</h4>
            <p>{{ users.length === 0 ? 'No users have registered yet' : 'Try adjusting your search criteria' }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- User Details Modal -->
    <div v-if="selectedUser" class="modal fade show d-block" style="background: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-person-circle me-2"></i>User Details
            </h5>
            <button @click="selectedUser = null" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <div class="row g-4">
              <div class="col-md-4 text-center">
                <div class="avatar-circle-large mx-auto mb-3">
                  {{ getInitials(selectedUser.fullname) }}
                </div>
                <h5 class="fw-bold">{{ selectedUser.fullname }}</h5>
                <p class="text-muted">{{ selectedUser.email }}</p>
              </div>
              <div class="col-md-8">
                <div class="row g-3">
                  <div class="col-12">
                    <label class="form-label fw-bold">Full Name</label>
                    <p class="form-control-plaintext">{{ selectedUser.fullname }}</p>
                  </div>
                  <div class="col-12">
                    <label class="form-label fw-bold">Email Address</label>
                    <p class="form-control-plaintext">{{ selectedUser.email }}</p>
                  </div>
                  <div class="col-12">
                    <label class="form-label fw-bold">Address</label>
                    <p class="form-control-plaintext">{{ selectedUser.address }}</p>
                  </div>
                  <div class="col-6">
                    <label class="form-label fw-bold">PIN Code</label>
                    <p class="form-control-plaintext">{{ selectedUser.pin_code }}</p>
                  </div>
                  <div class="col-6">
                    <label class="form-label fw-bold">Member Since</label>
                    <p class="form-control-plaintext">{{ formatDate(selectedUser.created_at) }}</p>
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
import { ref, computed, onMounted } from 'vue'
import { getApiUrl } from '../../config/api'
import type { User } from '../../stores/auth'

interface UserWithStats extends User {
  bookings_count: number
  active_bookings: number
}

const users = ref<UserWithStats[]>([])
const selectedUser = ref<UserWithStats | null>(null)
const searchQuery = ref('')
const loading = ref(false)

const activeUsers = computed(() => users.value.length)

const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  
  const query = searchQuery.value.toLowerCase()
  return users.value.filter(user =>
    user.fullname.toLowerCase().includes(query) ||
    user.email.toLowerCase().includes(query) ||
    user.address.toLowerCase().includes(query) ||
    user.pin_code.includes(query)
  )
})

onMounted(() => {
  loadUsers()
})

const loadUsers = async () => {
  loading.value = true
  try {
    const response = await fetch(getApiUrl('/api/users'))
    if (response.ok) {
      users.value = await response.json()
    }
  } catch (error) {
    console.error('Error loading users:', error)
  } finally {
    loading.value = false
  }
}

const getInitials = (name: string) => {
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const getUserBookingCount = (userId: string) => {
  const user = users.value.find(u => u.id === userId)
  return user?.bookings_count || 0
}

const getActiveBookingCount = (userId: string) => {
  const user = users.value.find(u => u.id === userId)
  return user?.active_bookings || 0
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getTimeAgo = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 1) return '1 day ago'
  if (diffDays < 30) return `${diffDays} days ago`
  if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`
  return `${Math.floor(diffDays / 365)} years ago`
}

const viewUserDetails = (user: UserWithStats) => {
  selectedUser.value = user
}

const viewUserBookings = (user: UserWithStats) => {
  // This would typically navigate to a bookings page for the user
  alert(`View bookings for ${user.fullname} - Feature coming soon!`)
}
</script>

<style scoped>
.avatar-circle {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 14px;
}

.avatar-circle-large {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 24px;
}

.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.table-hover tbody tr:hover {
  background-color: rgba(0, 123, 255, 0.05);
}

.btn-group-sm .btn {
  padding: 0.25rem 0.5rem;
}
</style>