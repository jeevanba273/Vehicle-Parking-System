<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="fw-bold text-dark">Booking History</h2>
          <button @click="loadBookings" class="btn btn-outline-primary">
            <i class="bi bi-arrow-clockwise me-2"></i>Refresh
          </button>
        </div>

        <!-- Summary Cards -->
        <div class="row g-4 mb-4">
          <div class="col-md-3">
            <div class="card bg-primary text-white">
              <div class="card-body text-center">
                <i class="bi bi-calendar-check display-4 mb-2"></i>
                <h3 class="fw-bold">{{ totalBookings }}</h3>
                <p class="mb-0">Total Bookings</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card bg-success text-white">
              <div class="card-body text-center">
                <i class="bi bi-clock-history display-4 mb-2"></i>
                <h3 class="fw-bold">{{ activeBookings }}</h3>
                <p class="mb-0">Active Bookings</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card bg-info text-white">
              <div class="card-body text-center">
                <i class="bi bi-check-circle display-4 mb-2"></i>
                <h3 class="fw-bold">{{ completedBookings }}</h3>
                <p class="mb-0">Completed</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="card bg-warning text-white">
              <div class="card-body text-center">
                <i class="bi bi-currency-dollar display-4 mb-2"></i>
                <h3 class="fw-bold">${{ totalSpent.toFixed(2) }}</h3>
                <p class="mb-0">Total Spent</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Filter -->
        <div class="card mb-4 shadow-sm">
          <div class="card-body">
            <div class="row g-3">
              <div class="col-md-4">
                <select v-model="statusFilter" class="form-select">
                  <option value="">All Bookings</option>
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                </select>
              </div>
              <div class="col-md-4">
                <input
                  v-model="searchQuery"
                  type="text"
                  class="form-control"
                  placeholder="Search by lot name or vehicle..."
                />
              </div>
              <div class="col-md-4">
                <select v-model="sortBy" class="form-select">
                  <option value="newest">Newest First</option>
                  <option value="oldest">Oldest First</option>
                  <option value="cost-high">Highest Cost</option>
                  <option value="cost-low">Lowest Cost</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Bookings List -->
        <div class="row g-4">
          <div
            v-for="booking in filteredBookings"
            :key="booking.id"
            class="col-lg-6"
          >
            <div class="card shadow-sm card-hover">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-3">
                  <h5 class="card-title fw-bold">{{ booking.lot_name }}</h5>
                  <span
                    class="badge"
                    :class="booking.status === 'active' ? 'bg-success' : 'bg-secondary'"
                  >
                    {{ booking.status }}
                  </span>
                </div>
                
                <div class="row g-3 mb-3">
                  <div class="col-6">
                    <small class="text-muted">Spot Number</small>
                    <div class="fw-bold">{{ booking.spot_number }}</div>
                  </div>
                  <div class="col-6">
                    <small class="text-muted">Vehicle</small>
                    <div class="fw-bold">{{ booking.vehicle_number }}</div>
                  </div>
                  <div class="col-6">
                    <small class="text-muted">Start Time</small>
                    <div class="fw-bold">{{ formatDateTime(booking.start_time) }}</div>
                  </div>
                  <div class="col-6">
                    <small class="text-muted">End Time</small>
                    <div class="fw-bold">
                      {{ booking.end_time ? formatDateTime(booking.end_time) : 'Active' }}
                    </div>
                  </div>
                </div>
                
                <div class="d-flex justify-content-between align-items-center">
                  <div>
                    <small class="text-muted">Total Cost</small>
                    <div class="h5 fw-bold text-primary mb-0">${{ booking.total_cost.toFixed(2) }}</div>
                  </div>
                  
                  <div v-if="booking.status === 'active'">
                    <button
                      @click="releaseBooking(booking)"
                      class="btn btn-warning btn-sm"
                      :disabled="releasing === booking.id"
                    >
                      <span v-if="releasing === booking.id" class="spinner-border spinner-border-sm me-2"></span>
                      {{ releasing === booking.id ? 'Releasing...' : 'Release Spot' }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-if="filteredBookings.length === 0" class="text-center py-5">
          <div class="text-muted">
            <i class="bi bi-calendar-x display-1"></i>
            <h4 class="mt-3">No bookings found</h4>
            <p>{{ bookings.length === 0 ? 'You haven\'t made any bookings yet' : 'Try adjusting your filters' }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth'

interface Booking {
  id: string
  lot_name: string
  spot_number: string
  vehicle_number: string
  start_time: string
  end_time: string | null
  total_cost: number
  status: 'active' | 'completed'
}

const authStore = useAuthStore()

const bookings = ref<Booking[]>([])
const statusFilter = ref('')
const searchQuery = ref('')
const sortBy = ref('newest')
const releasing = ref<string | null>(null)
const loading = ref(false)

const totalBookings = computed(() => bookings.value.length)
const activeBookings = computed(() => bookings.value.filter(b => b.status === 'active').length)
const completedBookings = computed(() => bookings.value.filter(b => b.status === 'completed').length)
const totalSpent = computed(() => bookings.value.reduce((sum, b) => sum + b.total_cost, 0))

const filteredBookings = computed(() => {
  let filtered = [...bookings.value]

  // Status filter
  if (statusFilter.value) {
    filtered = filtered.filter(booking => booking.status === statusFilter.value)
  }

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(booking =>
      booking.lot_name.toLowerCase().includes(query) ||
      booking.vehicle_number.toLowerCase().includes(query) ||
      booking.spot_number.toLowerCase().includes(query)
    )
  }

  // Sort
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'newest':
        return new Date(b.start_time).getTime() - new Date(a.start_time).getTime()
      case 'oldest':
        return new Date(a.start_time).getTime() - new Date(b.start_time).getTime()
      case 'cost-high':
        return b.total_cost - a.total_cost
      case 'cost-low':
        return a.total_cost - b.total_cost
      default:
        return 0
    }
  })

  return filtered
})

onMounted(() => {
  loadBookings()
})

const loadBookings = async () => {
  if (!authStore.currentUser) return
  
  loading.value = true
  try {
    const response = await fetch(`http://localhost:5000/api/users/${authStore.currentUser.id}/bookings`)
    if (response.ok) {
      bookings.value = await response.json()
    }
  } catch (error) {
    console.error('Error loading bookings:', error)
  } finally {
    loading.value = false
  }
}

const releaseBooking = async (booking: Booking) => {
  releasing.value = booking.id
  
  try {
    const response = await fetch(`http://localhost:5000/api/bookings/${booking.id}/release`, {
      method: 'POST'
    })
    
    const result = await response.json()
    
    if (result.success) {
      await loadBookings()
      alert('Spot released successfully!')
    } else {
      alert(result.message || 'Failed to release spot')
    }
  } catch (error) {
    console.error('Error releasing booking:', error)
    alert('Error releasing spot')
  } finally {
    releasing.value = null
  }
}

const formatDateTime = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}
</script>

<style scoped>
.card-hover {
  transition: all 0.3s ease;
}

.card-hover:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
}
</style>