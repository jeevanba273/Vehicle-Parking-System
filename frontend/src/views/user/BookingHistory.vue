<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12">
        <!-- Enhanced Header -->
        <div class="page-header mb-4">
          <div class="row align-items-center">
            <div class="col-md-8">
              <h2 class="fw-bold text-dark mb-2">
                <i class="bi bi-clock-history me-2 text-primary"></i>Booking History
              </h2>
              <p class="text-muted mb-0">Track your parking reservations and activity</p>
            </div>
            <div class="col-md-4 text-md-end">
              <button @click="loadBookings" class="btn btn-outline-primary refresh-btn">
                <i class="bi bi-arrow-clockwise me-2"></i>Refresh
              </button>
            </div>
          </div>
        </div>

        <!-- Enhanced Summary Cards -->
        <div class="summary-cards mb-4">
          <div class="row g-4">
            <div class="col-md-3">
              <div class="summary-card total-bookings">
                <div class="card-icon">
                  <i class="bi bi-calendar-check"></i>
                </div>
                <div class="card-content">
                  <div class="card-number">{{ totalBookings }}</div>
                  <div class="card-label">Total Bookings</div>
                  <div class="card-trend">
                    <i class="bi bi-arrow-up text-success"></i>
                    <span>+12% this month</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="summary-card active-bookings">
                <div class="card-icon">
                  <i class="bi bi-clock-history"></i>
                </div>
                <div class="card-content">
                  <div class="card-number">{{ activeBookings }}</div>
                  <div class="card-label">Active Bookings</div>
                  <div class="card-trend">
                    <i class="bi bi-circle-fill text-success pulse"></i>
                    <span>Live now</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="summary-card completed-bookings">
                <div class="card-icon">
                  <i class="bi bi-check-circle"></i>
                </div>
                <div class="card-content">
                  <div class="card-number">{{ completedBookings }}</div>
                  <div class="card-label">Completed</div>
                  <div class="card-trend">
                    <i class="bi bi-award text-warning"></i>
                    <span>{{ Math.round((completedBookings / totalBookings) * 100) }}% success</span>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="summary-card total-spent">
                <div class="card-icon">
                  <i class="bi bi-currency-dollar"></i>
                </div>
                <div class="card-content">
                  <div class="card-number">${{ totalSpent.toFixed(2) }}</div>
                  <div class="card-label">Total Spent</div>
                  <div class="card-trend">
                    <i class="bi bi-graph-up text-info"></i>
                    <span>Avg ${{ (totalSpent / Math.max(totalBookings, 1)).toFixed(2) }}/booking</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Enhanced Filter Bar -->
        <div class="filter-bar mb-4">
          <div class="row g-3">
            <div class="col-md-3">
              <select v-model="statusFilter" class="form-select filter-select">
                <option value="">All Bookings</option>
                <option value="active">Active Only</option>
                <option value="completed">Completed Only</option>
              </select>
            </div>
            <div class="col-md-3">
              <select v-model="timeFilter" class="form-select filter-select">
                <option value="">All Time</option>
                <option value="today">Today</option>
                <option value="week">This Week</option>
                <option value="month">This Month</option>
                <option value="quarter">Last 3 Months</option>
              </select>
            </div>
            <div class="col-md-3">
              <input
                v-model="searchQuery"
                type="text"
                class="form-control search-input"
                placeholder="Search by lot name or vehicle..."
              />
            </div>
            <div class="col-md-3">
              <select v-model="sortBy" class="form-select filter-select">
                <option value="newest">Newest First</option>
                <option value="oldest">Oldest First</option>
                <option value="cost-high">Highest Cost</option>
                <option value="cost-low">Lowest Cost</option>
                <option value="duration">Longest Duration</option>
              </select>
            </div>
          </div>
        </div>

        <!-- Enhanced Bookings List -->
        <div class="bookings-container">
          <div
            v-for="booking in filteredBookings"
            :key="booking.id"
            class="booking-card"
            :class="{ 'active-booking': booking.status === 'active' }"
          >
            <!-- Card Header -->
            <div class="booking-header">
              <div class="d-flex justify-content-between align-items-start">
                <div class="booking-info">
                  <h5 class="booking-title">{{ booking.lot_name }}</h5>
                  <div class="booking-meta">
                    <span class="spot-info">
                      <i class="bi bi-geo-alt me-1"></i>Spot {{ booking.spot_number }}
                    </span>
                    <span class="vehicle-info">
                      <i class="bi bi-car-front me-1"></i>{{ booking.vehicle_number }}
                    </span>
                  </div>
                </div>
                <div class="booking-status">
                  <span
                    class="status-badge"
                    :class="booking.status === 'active' ? 'status-active' : 'status-completed'"
                  >
                    <i :class="booking.status === 'active' ? 'bi bi-clock' : 'bi bi-check-circle'"></i>
                    {{ booking.status === 'active' ? 'Active' : 'Completed' }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Card Body -->
            <div class="booking-body">
              <div class="row g-3">
                <!-- Time Information -->
                <div class="col-md-6">
                  <div class="info-section">
                    <h6 class="info-title">
                      <i class="bi bi-clock me-2"></i>Timing Details
                    </h6>
                    <div class="info-grid">
                      <div class="info-item">
                        <span class="info-label">Start Time:</span>
                        <span class="info-value">{{ formatDateTime(booking.start_time) }}</span>
                      </div>
                      <div class="info-item">
                        <span class="info-label">End Time:</span>
                        <span class="info-value">
                          {{ booking.end_time ? formatDateTime(booking.end_time) : 'Active' }}
                        </span>
                      </div>
                      <div class="info-item">
                        <span class="info-label">Duration:</span>
                        <span class="info-value">{{ formatDuration(booking.duration_hours) }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Cost Information -->
                <div class="col-md-6">
                  <div class="info-section">
                    <h6 class="info-title">
                      <i class="bi bi-currency-dollar me-2"></i>Cost Breakdown
                    </h6>
                    <div class="cost-breakdown">
                      <div class="cost-item">
                        <span class="cost-label">Duration:</span>
                        <span class="cost-value">{{ formatDuration(booking.duration_hours) }}</span>
                      </div>
                      <div class="cost-item">
                        <span class="cost-label">Rate:</span>
                        <span class="cost-value">${{ (booking.total_cost / booking.duration_hours).toFixed(2) }}/hr</span>
                      </div>
                      <div class="cost-item total-cost">
                        <span class="cost-label">Total:</span>
                        <span class="cost-value">${{ booking.total_cost.toFixed(2) }}</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Active Booking Controls -->
                <div v-if="booking.status === 'active'" class="col-12">
                  <div class="active-controls">
                    <div class="row align-items-center">
                      <div class="col-md-8">
                        <div class="time-remaining">
                          <i class="bi bi-hourglass-split me-2"></i>
                          <span class="remaining-text">Time Remaining: </span>
                          <span class="remaining-value">{{ getTimeRemaining(booking) }}</span>
                        </div>
                      </div>
                      <div class="col-md-4 text-md-end">
                        <button
                          @click="releaseBooking(booking)"
                          class="btn btn-warning release-btn"
                          :disabled="releasing === booking.id"
                        >
                          <span v-if="releasing === booking.id" class="spinner-border spinner-border-sm me-2"></span>
                          <i v-else class="bi bi-unlock me-2"></i>
                          {{ releasing === booking.id ? 'Releasing...' : 'Release Spot' }}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Card Footer -->
            <div class="booking-footer">
              <div class="d-flex justify-content-between align-items-center">
                <div class="booking-id">
                  <small class="text-muted">Booking ID: #{{ booking.id.slice(-8) }}</small>
                </div>
                <div class="booking-actions">
                  <button class="btn btn-outline-primary btn-sm action-btn" @click="viewDetails(booking)">
                    <i class="bi bi-eye me-1"></i>Details
                  </button>
                  <button class="btn btn-outline-secondary btn-sm action-btn" @click="downloadReceipt(booking)">
                    <i class="bi bi-download me-1"></i>Receipt
                  </button>
                  <button v-if="booking.status === 'completed'" class="btn btn-outline-success btn-sm action-btn" @click="rebookSpot(booking)">
                    <i class="bi bi-arrow-repeat me-1"></i>Rebook
                  </button>
                </div>
              </div>
            </div>

            <!-- Active Booking Indicator -->
            <div v-if="booking.status === 'active'" class="active-indicator">
              <div class="pulse-ring"></div>
              <div class="pulse-dot"></div>
            </div>
          </div>
        </div>

        <!-- Enhanced Empty State -->
        <div v-if="filteredBookings.length === 0" class="empty-state">
          <div class="empty-illustration">
            <i class="bi bi-calendar-x"></i>
          </div>
          <h4>{{ bookings.length === 0 ? 'No bookings yet' : 'No bookings found' }}</h4>
          <p>
            {{ bookings.length === 0 
              ? 'Start by booking your first parking spot' 
              : 'Try adjusting your filters to see more results' 
            }}
          </p>
          <div class="empty-actions">
            <button v-if="bookings.length === 0" @click="$router.push('/user/book-spot')" class="btn btn-primary">
              <i class="bi bi-plus-circle me-2"></i>Book Your First Spot
            </button>
            <button v-else @click="clearFilters" class="btn btn-outline-primary">
              <i class="bi bi-funnel me-2"></i>Clear Filters
            </button>
          </div>
        </div>

        <!-- Pagination -->
        <div v-if="filteredBookings.length > 0" class="pagination-container">
          <nav aria-label="Booking history pagination">
            <ul class="pagination justify-content-center">
              <li class="page-item">
                <a class="page-link" href="#" aria-label="Previous">
                  <span aria-hidden="true">&laquo;</span>
                </a>
              </li>
              <li class="page-item active"><a class="page-link" href="#">1</a></li>
              <li class="page-item"><a class="page-link" href="#">2</a></li>
              <li class="page-item"><a class="page-link" href="#">3</a></li>
              <li class="page-item">
                <a class="page-link" href="#" aria-label="Next">
                  <span aria-hidden="true">&raquo;</span>
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'
import { getApiUrl } from '../../config/api'

interface Booking {
  id: string
  lot_name: string
  spot_number: string
  vehicle_number: string
  start_time: string
  end_time: string | null
  duration_hours: number
  total_cost: number
  status: 'active' | 'completed'
}

const router = useRouter()
const authStore = useAuthStore()

const bookings = ref<Booking[]>([])
const statusFilter = ref('')
const timeFilter = ref('')
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

  // Time filter
  if (timeFilter.value) {
    const now = new Date()
    const startTime = new Date(filtered[0]?.start_time || now)
    
    filtered = filtered.filter(booking => {
      const bookingDate = new Date(booking.start_time)
      switch (timeFilter.value) {
        case 'today':
          return bookingDate.toDateString() === now.toDateString()
        case 'week':
          const weekAgo = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
          return bookingDate >= weekAgo
        case 'month':
          const monthAgo = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000)
          return bookingDate >= monthAgo
        case 'quarter':
          const quarterAgo = new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000)
          return bookingDate >= quarterAgo
        default:
          return true
      }
    })
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
      case 'duration':
        return b.duration_hours - a.duration_hours
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
    const response = await fetch(getApiUrl(`/api/users/${authStore.currentUser.id}/bookings`))
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
    const response = await fetch(getApiUrl(`/api/bookings/${booking.id}/release`), {
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

const clearFilters = () => {
  statusFilter.value = ''
  timeFilter.value = ''
  searchQuery.value = ''
  sortBy.value = 'newest'
}

const viewDetails = (booking: Booking) => {
  alert(`Viewing details for booking #${booking.id.slice(-8)} - Feature coming soon!`)
}

const downloadReceipt = (booking: Booking) => {
  alert(`Downloading receipt for booking #${booking.id.slice(-8)} - Feature coming soon!`)
}

const rebookSpot = (booking: Booking) => {
  alert(`Rebooking spot at ${booking.lot_name} - Feature coming soon!`)
}

const formatDateTime = (dateString: string) => {
  return new Date(dateString).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatDuration = (hours: number) => {
  if (hours < 1) {
    return `${Math.round(hours * 60)} minutes`
  } else if (hours === 1) {
    return '1 hour'
  } else {
    const wholeHours = Math.floor(hours)
    const minutes = Math.round((hours - wholeHours) * 60)
    if (minutes === 0) {
      return `${wholeHours} hours`
    } else {
      return `${wholeHours}h ${minutes}m`
    }
  }
}

const getTimeRemaining = (booking: Booking) => {
  if (!booking.end_time) return 'N/A'
  
  const now = new Date()
  const end = new Date(booking.end_time)
  const diff = end.getTime() - now.getTime()
  
  if (diff <= 0) return 'Expired'
  
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  
  if (hours > 0) {
    return `${hours}h ${minutes}m`
  } else {
    return `${minutes}m`
  }
}
</script>

<style scoped>
/* Page Header */
.page-header {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid #dee2e6;
}

.refresh-btn {
  border-radius: 12px !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
}

.refresh-btn:hover {
  transform: rotate(180deg) !important;
}

/* Summary Cards */
.summary-cards {
  margin-bottom: 2rem;
}

.summary-card {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.summary-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

.summary-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #0d6efd, #6f42c1);
}

.total-bookings::before {
  background: linear-gradient(90deg, #0d6efd, #0b5ed7);
}

.active-bookings::before {
  background: linear-gradient(90deg, #198754, #20c997);
}

.completed-bookings::before {
  background: linear-gradient(90deg, #17a2b8, #20c997);
}

.total-spent::before {
  background: linear-gradient(90deg, #ffc107, #fd7e14);
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 16px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.75rem;
  color: #0d6efd;
  margin-bottom: 1rem;
}

.card-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2d3748;
  line-height: 1;
  margin-bottom: 0.5rem;
}

.card-label {
  color: #6c757d;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 0.75rem;
}

.card-trend {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
  color: #6c757d;
}

.pulse {
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

/* Filter Bar */
.filter-bar {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  border: 1px solid #e9ecef;
}

.filter-select, .search-input {
  border: 2px solid #e9ecef !important;
  border-radius: 12px !important;
  background: #f8f9fa !important;
  transition: all 0.3s ease !important;
}

.filter-select:focus, .search-input:focus {
  border-color: #0d6efd !important;
  background: white !important;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25) !important;
}

/* Bookings Container */
.bookings-container {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.booking-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.booking-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.12);
}

.booking-card.active-booking {
  border-color: #198754;
  background: linear-gradient(135deg, #f8fff9 0%, #e8f5e8 100%);
}

.booking-header {
  padding: 1.5rem 1.5rem 0;
}

.booking-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.booking-meta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.spot-info, .vehicle-info {
  color: #6c757d;
  font-size: 0.9rem;
  font-weight: 600;
  display: flex;
  align-items: center;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-active {
  background: #d4edda;
  color: #155724;
}

.status-completed {
  background: #cce7ff;
  color: #004085;
}

.booking-body {
  padding: 1.5rem;
}

.info-section {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #e9ecef;
  height: 100%;
}

.info-title {
  color: #2d3748;
  font-weight: 600;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.info-grid {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.info-item {
  display: flex;
  justify-content: between;
  align-items: center;
}

.info-label {
  color: #6c757d;
  font-size: 0.9rem;
  min-width: 80px;
}

.info-value {
  color: #2d3748;
  font-weight: 600;
  font-size: 0.9rem;
  margin-left: auto;
}

.cost-breakdown {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.cost-item {
  display: flex;
  justify-content: between;
  align-items: center;
  padding: 0.5rem 0;
}

.cost-item.total-cost {
  border-top: 2px solid #dee2e6;
  padding-top: 1rem;
  margin-top: 0.5rem;
}

.cost-label {
  color: #6c757d;
  font-size: 0.9rem;
}

.cost-value {
  color: #2d3748;
  font-weight: 600;
  margin-left: auto;
}

.total-cost .cost-value {
  color: #198754;
  font-size: 1.1rem;
  font-weight: 700;
}

.active-controls {
  background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #c3e6cb;
}

.time-remaining {
  display: flex;
  align-items: center;
  color: #155724;
  font-weight: 600;
}

.remaining-text {
  margin-right: 0.5rem;
}

.remaining-value {
  font-size: 1.1rem;
  font-weight: 700;
}

.release-btn {
  background: linear-gradient(135deg, #ffc107 0%, #fd7e14 100%) !important;
  border: none !important;
  color: #000 !important;
  font-weight: 600 !important;
  border-radius: 12px !important;
  transition: all 0.3s ease !important;
}

.release-btn:hover:not(:disabled) {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 25px rgba(255, 193, 7, 0.3) !important;
}

.booking-footer {
  padding: 1.5rem;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.booking-id {
  font-family: 'Courier New', monospace;
}

.booking-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  border-radius: 8px !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
}

.action-btn:hover {
  transform: translateY(-1px) !important;
}

/* Active Booking Indicator */
.active-indicator {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 20px;
  height: 20px;
}

.pulse-ring {
  position: absolute;
  width: 20px;
  height: 20px;
  border: 2px solid #198754;
  border-radius: 50%;
  animation: pulse-ring 2s infinite;
}

.pulse-dot {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 8px;
  height: 8px;
  background: #198754;
  border-radius: 50%;
}

@keyframes pulse-ring {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  100% {
    transform: scale(2);
    opacity: 0;
  }
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #6c757d;
}

.empty-illustration {
  font-size: 5rem;
  margin-bottom: 2rem;
  color: #dee2e6;
}

.empty-actions {
  margin-top: 2rem;
}

/* Pagination */
.pagination-container {
  margin-top: 3rem;
  padding-top: 2rem;
  border-top: 1px solid #e9ecef;
}

.pagination .page-link {
  border-radius: 8px !important;
  margin: 0 0.25rem !important;
  border: 1px solid #dee2e6 !important;
  color: #6c757d !important;
  font-weight: 600 !important;
}

.pagination .page-item.active .page-link {
  background: linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%) !important;
  border-color: #0d6efd !important;
}

.pagination .page-link:hover {
  background: #f8f9fa !important;
  border-color: #0d6efd !important;
  color: #0d6efd !important;
}

/* Responsive Design */
@media (max-width: 768px) {
  .summary-card {
    padding: 1.5rem;
  }
  
  .card-number {
    font-size: 2rem;
  }
  
  .booking-meta {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .booking-actions {
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .action-btn {
    width: 100%;
  }
  
  .active-controls .row {
    flex-direction: column;
    gap: 1rem;
  }
  
  .active-controls .col-md-4 {
    text-align: left !important;
  }
}
</style>