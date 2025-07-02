<template>
  <div class="parking-grid-container">
    <div class="grid-header mb-4">
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h4 class="grid-title mb-1">{{ lot.name }} - Parking Grid</h4>
          <p class="grid-subtitle text-muted">Real-time spot management and booking (Current IST: {{ getCurrentISTTime() }})</p>
        </div>
        <div class="grid-stats">
          <div class="stat-item">
            <span class="stat-number text-success">{{ availableCount }}</span>
            <span class="stat-label">Available</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-number text-danger">{{ occupiedCount }}</span>
            <span class="stat-label">Occupied</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Legend -->
    <div class="legend-section mb-4">
      <div class="legend-items">
        <div class="legend-item">
          <div class="legend-spot available"></div>
          <span>Available</span>
        </div>
        <div class="legend-item">
          <div class="legend-spot occupied"></div>
          <span>Occupied</span>
        </div>
        <div class="legend-item">
          <div class="legend-spot reserved"></div>
          <span>Reserved</span>
        </div>
        <div class="legend-item">
          <div class="legend-spot selected"></div>
          <span>Selected</span>
        </div>
      </div>
    </div>
    
    <!-- Parking Grid -->
    <div class="parking-grid-wrapper">
      <div class="parking-grid">
        <div
          v-for="spot in spots"
          :key="spot.id"
          :class="['parking-spot', spot.status, { 'selected': selectedSpot?.id === spot.id }]"
          :title="`Spot ${spot.spot_number} - ${spot.status}`"
          @click="selectSpot(spot)"
        >
          <div class="spot-number">{{ spot.spot_number }}</div>
          <div v-if="spot.status === 'occupied'" class="spot-timer">
            <i class="bi bi-clock"></i>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Spot Details Panel -->
    <div v-if="selectedSpot" class="spot-details-panel">
      <div class="panel-header">
        <h6 class="panel-title">
          <i class="bi bi-info-circle me-2"></i>
          Spot {{ selectedSpot.spot_number }} Details
        </h6>
        <div class="panel-status">
          <span :class="`badge status-${selectedSpot.status}`">
            {{ selectedSpot.status.toUpperCase() }}
          </span>
        </div>
      </div>
      
      <!-- Available Spot - Booking Form -->
      <div v-if="selectedSpot.status === 'available' && showBookingForm" class="booking-section">
        <form @submit.prevent="bookSpot" class="booking-form">
          <div class="form-header">
            <h6><i class="bi bi-plus-circle me-2"></i>Book This Spot</h6>
          </div>
          
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label">Vehicle Number</label>
              <div class="input-group">
                <span class="input-group-text"><i class="bi bi-car-front"></i></span>
                <input
                  v-model="bookingForm.vehicleNumber"
                  type="text"
                  class="form-control booking-input"
                  required
                  placeholder="KA-01-AB-1234"
                />
              </div>
            </div>
            
            <div class="col-md-6">
              <label class="form-label">Parking Duration</label>
              <div class="duration-controls">
                <div class="row g-2">
                  <div class="col-6">
                    <div class="input-group">
                      <input
                        v-model.number="bookingForm.hours"
                        type="number"
                        class="form-control booking-input text-center"
                        min="0"
                        max="23"
                        placeholder="0"
                        @input="updateTotalTime"
                      />
                      <span class="input-group-text">hrs</span>
                    </div>
                  </div>
                  <div class="col-6">
                    <div class="input-group">
                      <input
                        v-model.number="bookingForm.minutes"
                        type="number"
                        class="form-control booking-input text-center"
                        min="0"
                        max="59"
                        step="15"
                        placeholder="0"
                        @input="updateTotalTime"
                      />
                      <span class="input-group-text">min</span>
                    </div>
                  </div>
                </div>
                
                <!-- Quick Duration Buttons -->
                <div class="quick-duration-buttons mt-2">
                  <button type="button" class="btn btn-outline-primary btn-sm" @click="setQuickTime(0.25)">15min</button>
                  <button type="button" class="btn btn-outline-primary btn-sm" @click="setQuickTime(0.5)">30min</button>
                  <button type="button" class="btn btn-outline-primary btn-sm" @click="setQuickTime(1)">1hr</button>
                  <button type="button" class="btn btn-outline-primary btn-sm" @click="setQuickTime(2)">2hrs</button>
                  <button type="button" class="btn btn-outline-primary btn-sm" @click="setQuickTime(4)">4hrs</button>
                  <button type="button" class="btn btn-outline-primary btn-sm" @click="setQuickTime(8)">8hrs</button>
                </div>
                
                <div class="duration-display mt-2">
                  <small class="text-muted">
                    Total Duration: <strong>{{ formatDuration(bookingForm.totalHours) }}</strong>
                    <span v-if="bookingForm.totalHours < 0.25" class="text-warning ms-2">
                      (Minimum 15 minutes required)
                    </span>
                  </small>
                </div>
              </div>
            </div>
            
            <!-- Cost Summary -->
            <div class="col-12">
              <div class="cost-summary">
                <div class="cost-header">
                  <h6><i class="bi bi-calculator me-2"></i>Cost Breakdown</h6>
                </div>
                <div class="cost-details">
                  <div class="cost-row">
                    <span>Hourly Rate:</span>
                    <span class="cost-value">₹{{ lot.price_per_hour.toFixed(2) }}/hour</span>
                  </div>
                  <div class="cost-row">
                    <span>Duration:</span>
                    <span class="cost-value">{{ formatDuration(Math.max(0.25, bookingForm.totalHours)) }}</span>
                  </div>
                  <div class="cost-row total-row">
                    <span>Total Cost:</span>
                    <span class="total-cost">₹{{ calculateTotalCost().toFixed(2) }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Action Buttons -->
            <div class="col-12">
              <div class="booking-actions">
                <button 
                  type="submit" 
                  class="btn btn-success btn-lg booking-submit-btn" 
                  :disabled="booking || bookingForm.totalHours < 0.25"
                >
                  <span v-if="booking" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="bi bi-check-circle me-2"></i>
                  {{ booking ? 'Booking...' : 'Confirm Booking' }}
                </button>
                <button type="button" @click="cancelBooking" class="btn btn-outline-secondary btn-lg">
                  <i class="bi bi-x-circle me-2"></i>Cancel
                </button>
              </div>
            </div>
          </div>
        </form>
      </div>
      
      <!-- Occupied Spot Details -->
      <div v-else-if="selectedSpot.status === 'occupied'" class="occupied-details">
        <div class="occupied-info">
          <div class="info-grid">
            <div class="info-item">
              <label>Vehicle Number</label>
              <div class="info-value">{{ selectedSpot.vehicle_number }}</div>
            </div>
            <div class="info-item">
              <label>Booked At (IST)</label>
              <div class="info-value">{{ parseISTDateTime(selectedSpot.booked_at || '') }}</div>
            </div>
            <div class="info-item">
              <label>Release Time (IST)</label>
              <div class="info-value">{{ parseISTDateTime(selectedSpot.release_time || '') }}</div>
            </div>
            <div class="info-item">
              <label>Time Remaining</label>
              <div class="info-value" :class="getTimeRemainingColor(selectedSpot.release_time || '')">
                {{ getTimeRemaining(selectedSpot.release_time || '') }}
              </div>
            </div>
          </div>
          
          <!-- User Details for Admin -->
          <div v-if="isAdmin && selectedSpot.user_details" class="user-details-section">
            <div class="section-header">
              <h6><i class="bi bi-person-circle me-2"></i>User Information</h6>
            </div>
            <div class="user-info-grid">
              <div class="user-info-item">
                <label>Name</label>
                <div class="user-info-value">{{ selectedSpot.user_details.fullname }}</div>
              </div>
              <div class="user-info-item">
                <label>Email</label>
                <div class="user-info-value">{{ selectedSpot.user_details.email }}</div>
              </div>
              <div class="user-info-item">
                <label>Address</label>
                <div class="user-info-value">{{ selectedSpot.user_details.address }}</div>
              </div>
              <div class="user-info-item">
                <label>PIN Code</label>
                <div class="user-info-value">{{ selectedSpot.user_details.pin_code }}</div>
              </div>
            </div>
            
            <!-- Booking Details -->
            <div v-if="selectedSpot.booking_details" class="booking-details-section">
              <div class="section-header">
                <h6><i class="bi bi-calendar-check me-2"></i>Booking Information</h6>
              </div>
              <div class="booking-info-grid">
                <div class="booking-info-item">
                  <label>Duration</label>
                  <div class="booking-info-value">{{ formatDuration(selectedSpot.booking_details.duration_hours) }}</div>
                </div>
                <div class="booking-info-item">
                  <label>Total Cost</label>
                  <div class="booking-info-value cost-highlight">₹{{ selectedSpot.booking_details.total_cost.toFixed(2) }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Release Button for User's Own Booking -->
        <div v-if="canRelease" class="release-section">
          <button @click="releaseSpot" class="btn btn-warning btn-lg release-btn" :disabled="releasing">
            <span v-if="releasing" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="bi bi-unlock me-2"></i>
            {{ releasing ? 'Releasing...' : 'Release Spot' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive, watch } from 'vue'
import { useAuthStore } from '../stores/auth'
import { getApiUrl } from '../config/api'
import type { ParkingLot, ParkingSpot } from '../stores/parking'

const props = defineProps<{
  lot: ParkingLot
  showBookingForm?: boolean
}>()

const authStore = useAuthStore()

const spots = ref<ParkingSpot[]>([])
const selectedSpot = ref<ParkingSpot | null>(null)
const booking = ref(false)
const releasing = ref(false)

const bookingForm = reactive({
  vehicleNumber: '',
  hours: 1,
  minutes: 0,
  totalHours: 1
})

const isAdmin = computed(() => authStore.isAdmin)
const availableCount = computed(() => spots.value.filter(s => s.status === 'available').length)
const occupiedCount = computed(() => spots.value.filter(s => s.status === 'occupied').length)

const canRelease = computed(() => {
  return selectedSpot.value?.occupied_by === authStore.currentUser?.id
})

// Watch for changes in hours and minutes to update total
watch([() => bookingForm.hours, () => bookingForm.minutes], () => {
  updateTotalTime()
})

onMounted(async () => {
  await loadSpots()
})

const loadSpots = async () => {
  try {
    const response = await fetch(getApiUrl(`/api/parking-lots/${props.lot.id}/spots`))
    if (response.ok) {
      spots.value = await response.json()
    }
  } catch (error) {
    console.error('Error loading spots:', error)
  }
}

const selectSpot = (spot: ParkingSpot) => {
  selectedSpot.value = spot
}

const updateTotalTime = () => {
  const hours = Number(bookingForm.hours) || 0
  const minutes = Number(bookingForm.minutes) || 0
  bookingForm.totalHours = hours + (minutes / 60)
}

const setQuickTime = (hours: number) => {
  bookingForm.totalHours = hours
  bookingForm.hours = Math.floor(hours)
  bookingForm.minutes = Math.round((hours - Math.floor(hours)) * 60)
}

const formatDuration = (totalHours: number) => {
  if (totalHours < 1) {
    return `${Math.round(totalHours * 60)} minutes`
  } else if (totalHours === 1) {
    return '1 hour'
  } else {
    const hours = Math.floor(totalHours)
    const minutes = Math.round((totalHours - hours) * 60)
    if (minutes === 0) {
      return `${hours} hours`
    } else {
      return `${hours}h ${minutes}m`
    }
  }
}

const calculateTotalCost = () => {
  const minHours = Math.max(0.25, bookingForm.totalHours) // Minimum 15 minutes
  return props.lot.price_per_hour * minHours
}

const bookSpot = async () => {
  if (!selectedSpot.value || !authStore.currentUser) return
  
  if (bookingForm.totalHours < 0.25) {
    showNotification('Minimum booking duration is 15 minutes', 'warning')
    return
  }
  
  booking.value = true
  
  try {
    const response = await fetch(getApiUrl('/api/bookings'), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: authStore.currentUser.id,
        lot_id: props.lot.id,
        spot_id: selectedSpot.value.id,
        vehicle_number: bookingForm.vehicleNumber,
        hours: Math.max(0.25, bookingForm.totalHours) // Send the actual duration
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      await loadSpots()
      selectedSpot.value = null
      resetForm()
      showNotification(`Spot booked successfully for ${formatDuration(Math.max(0.25, bookingForm.totalHours))}! All times are in IST.`, 'success')
    } else {
      showNotification(result.message || 'Failed to book spot', 'error')
    }
  } catch (error) {
    console.error('Error booking spot:', error)
    showNotification('Error booking spot', 'error')
  } finally {
    booking.value = false
  }
}

const releaseSpot = async () => {
  if (!selectedSpot.value) return
  
  releasing.value = true
  
  try {
    // Find the booking for this spot
    const bookingsResponse = await fetch(getApiUrl(`/api/users/${authStore.currentUser?.id}/bookings`))
    const bookings = await bookingsResponse.json()
    const activeBooking = bookings.find((b: any) => 
      b.spot_number === selectedSpot.value?.spot_number && 
      b.status === 'active' &&
      b.lot_name === props.lot.name
    )
    
    if (activeBooking) {
      const response = await fetch(getApiUrl(`/api/bookings/${activeBooking.id}/release`), {
        method: 'POST'
      })
      
      const result = await response.json()
      
      if (result.success) {
        await loadSpots()
        selectedSpot.value = null
        showNotification('Spot released successfully!', 'success')
      } else {
        showNotification(result.message || 'Failed to release spot', 'error')
      }
    } else {
      showNotification('No active booking found for this spot', 'warning')
    }
  } catch (error) {
    console.error('Error releasing spot:', error)
    showNotification('Error releasing spot', 'error')
  } finally {
    releasing.value = false
  }
}

const cancelBooking = () => {
  selectedSpot.value = null
  resetForm()
}

const resetForm = () => {
  bookingForm.vehicleNumber = ''
  bookingForm.hours = 1
  bookingForm.minutes = 0
  bookingForm.totalHours = 1
}

const getCurrentISTTime = () => {
  const now = new Date()
  return now.toLocaleTimeString('en-IN', {
    timeZone: 'Asia/Kolkata',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true
  })
}

const parseISTDateTime = (dateString: string) => {
  if (!dateString || dateString === 'N/A' || dateString === 'None') return 'N/A'
  
  try {
    // If the string already contains 'IST', just return it as is
    if (dateString.includes('IST')) {
      return dateString
    }
    
    // Try to parse as regular date and convert to IST format
    const date = new Date(dateString)
    if (isNaN(date.getTime())) {
      return 'Invalid Date'
    }
    
    return date.toLocaleString('en-IN', {
      timeZone: 'Asia/Kolkata',
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    }) + ' IST'
  } catch (error) {
    console.error('Error parsing date:', error)
    return dateString
  }
}

const getTimeRemaining = (releaseTime: string) => {
  if (!releaseTime || releaseTime === 'N/A' || releaseTime === 'None') return 'N/A'
  
  try {
    let releaseDate: Date
    
    // Parse IST format from backend - CRITICAL FIX
    if (releaseTime.includes('IST')) {
      // Parse the IST formatted string properly
      const cleanTime = releaseTime.replace(' IST', '')
      // Convert DD/MM/YYYY, HH:MM:SS AM/PM format to proper date
      const parts = cleanTime.split(', ')
      if (parts.length === 2) {
        const datePart = parts[0] // DD/MM/YYYY
        const timePart = parts[1] // HH:MM:SS AM/PM
        
        const [day, month, year] = datePart.split('/')
        const dateStr = `${month}/${day}/${year} ${timePart}`
        releaseDate = new Date(dateStr)
      } else {
        releaseDate = new Date(cleanTime)
      }
    } else {
      releaseDate = new Date(releaseTime)
    }
    
    if (isNaN(releaseDate.getTime())) {
      console.error('Invalid release date:', releaseTime)
      return 'Invalid Date'
    }
    
    // Get current IST time properly
    const now = new Date()
    const istOffset = 5.5 * 60 * 60 * 1000 // IST is UTC+5:30
    const utcTime = now.getTime() + (now.getTimezoneOffset() * 60000)
    const istTime = new Date(utcTime + istOffset)
    
    const diff = releaseDate.getTime() - istTime.getTime()
    
    if (diff <= 0) return 'Expired'
    
    const hours = Math.floor(diff / (1000 * 60 * 60))
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
    
    if (hours > 0) {
      return `${hours}h ${minutes}m`
    } else {
      return `${minutes}m`
    }
  } catch (error) {
    console.error('Error calculating time remaining:', error, 'for time:', releaseTime)
    return 'Error'
  }
}

const getTimeRemainingColor = (releaseTime: string) => {
  if (!releaseTime || releaseTime === 'N/A' || releaseTime === 'None') return 'text-muted'
  
  try {
    let releaseDate: Date
    
    if (releaseTime.includes('IST')) {
      const cleanTime = releaseTime.replace(' IST', '')
      const parts = cleanTime.split(', ')
      if (parts.length === 2) {
        const datePart = parts[0]
        const timePart = parts[1]
        const [day, month, year] = datePart.split('/')
        const dateStr = `${month}/${day}/${year} ${timePart}`
        releaseDate = new Date(dateStr)
      } else {
        releaseDate = new Date(cleanTime)
      }
    } else {
      releaseDate = new Date(releaseTime)
    }
    
    if (isNaN(releaseDate.getTime())) {
      return 'text-muted'
    }
    
    const now = new Date()
    const istOffset = 5.5 * 60 * 60 * 1000
    const utcTime = now.getTime() + (now.getTimezoneOffset() * 60000)
    const istTime = new Date(utcTime + istOffset)
    
    const diff = releaseDate.getTime() - istTime.getTime()
    const minutes = diff / (1000 * 60)
    
    if (minutes <= 0) return 'text-danger'
    if (minutes <= 30) return 'text-warning'
    return 'text-success'
  } catch (error) {
    return 'text-muted'
  }
}

const showNotification = (message: string, type: 'success' | 'error' | 'warning' | 'info') => {
  // Enhanced notification system - will be replaced with toast notifications
  console.log(`${type.toUpperCase()}: ${message}`)
  alert(message)
}
</script>

<style scoped>
.parking-grid-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

/* Grid Header */
.grid-header {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid #dee2e6;
}

.grid-title {
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 0.25rem;
}

.grid-subtitle {
  margin-bottom: 0;
  font-size: 0.9rem;
}

.grid-stats {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: white;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.stat-item {
  text-align: center;
}

.stat-number {
  display: block;
  font-size: 1.5rem;
  font-weight: 800;
  line-height: 1;
}

.stat-label {
  font-size: 0.8rem;
  color: #6c757d;
  font-weight: 500;
}

.stat-divider {
  width: 1px;
  height: 30px;
  background: #dee2e6;
}

/* Legend */
.legend-section {
  background: white;
  border-radius: 12px;
  padding: 1rem 1.5rem;
  border: 1px solid #e9ecef;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.legend-items {
  display: flex;
  gap: 2rem;
  justify-content: center;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: #495057;
}

.legend-spot {
  width: 20px;
  height: 20px;
  border-radius: 6px;
  border: 2px solid transparent;
}

.legend-spot.available {
  background: #28a745;
}

.legend-spot.occupied {
  background: #dc3545;
}

.legend-spot.reserved {
  background: #ffc107;
}

.legend-spot.selected {
  background: #007bff;
  border-color: #0056b3;
}

/* Parking Grid */
.parking-grid-wrapper {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid #e9ecef;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  margin-bottom: 2rem;
}

.parking-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
  gap: 12px;
  max-width: 800px;
  margin: 0 auto;
}

.parking-spot {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: white;
  border: 3px solid transparent;
  position: relative;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.parking-spot.available {
  background: linear-gradient(135deg, #28a745, #20c997);
}

.parking-spot.occupied {
  background: linear-gradient(135deg, #dc3545, #c82333);
}

.parking-spot.reserved {
  background: linear-gradient(135deg, #ffc107, #e0a800);
  color: #212529;
}

.parking-spot.selected {
  border-color: #007bff;
  transform: scale(1.1);
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.3);
  z-index: 10;
}

.parking-spot:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(0,0,0,0.2);
}

.spot-number {
  font-size: 0.8rem;
  font-weight: 700;
}

.spot-timer {
  font-size: 0.6rem;
  margin-top: 2px;
}

/* Spot Details Panel */
.spot-details-panel {
  background: white;
  border-radius: 16px;
  border: 1px solid #e9ecef;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  overflow: hidden;
}

.panel-header {
  background: linear-gradient(135deg, #495057, #6c757d);
  color: white;
  padding: 1rem 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.panel-title {
  margin: 0;
  font-weight: 600;
}

.panel-status .badge {
  font-size: 0.75rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
}

.status-available {
  background: #28a745;
}

.status-occupied {
  background: #dc3545;
}

.status-reserved {
  background: #ffc107;
  color: #212529;
}

/* Booking Section */
.booking-section {
  padding: 2rem;
}

.form-header {
  margin-bottom: 1.5rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #e9ecef;
}

.form-header h6 {
  color: #495057;
  font-weight: 600;
  margin: 0;
}

.booking-input {
  border: 2px solid #e9ecef;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.booking-input:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.duration-controls {
  position: relative;
}

.quick-duration-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.quick-duration-buttons .btn {
  padding: 0.25rem 0.75rem;
  font-size: 0.8rem;
  border-radius: 20px;
}

.duration-display {
  text-align: center;
}

.cost-summary {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  padding: 1.5rem;
  border: 2px solid #dee2e6;
}

.cost-header h6 {
  color: #495057;
  font-weight: 600;
  margin-bottom: 1rem;
}

.cost-details {
  space-y: 0.5rem;
}

.cost-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.cost-row.total-row {
  border-top: 2px solid #dee2e6;
  margin-top: 0.5rem;
  padding-top: 1rem;
  font-weight: 600;
}

.cost-value {
  font-weight: 500;
  color: #495057;
}

.total-cost {
  font-size: 1.2rem;
  font-weight: 700;
  color: #28a745;
}

.booking-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
}

.booking-submit-btn {
  background: linear-gradient(135deg, #28a745, #20c997);
  border: none;
  color: white;
  font-weight: 600;
  padding: 0.75rem 2rem;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.booking-submit-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #218838, #1e7e34);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4);
}

.booking-submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Occupied Details */
.occupied-details {
  padding: 2rem;
}

.occupied-info {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.info-item label {
  font-size: 0.8rem;
  color: #6c757d;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
  margin-top: 0.25rem;
}

.user-details-section,
.booking-details-section {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border-radius: 12px;
  padding: 1.5rem;
  margin-top: 1.5rem;
  border: 1px solid #2196f3;
}

.section-header h6 {
  color: #1976d2;
  font-weight: 600;
  margin-bottom: 1rem;
}

.user-info-grid,
.booking-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
}

.user-info-item,
.booking-info-item {
  background: rgba(255,255,255,0.7);
  padding: 1rem;
  border-radius: 8px;
}

.user-info-item label,
.booking-info-item label {
  font-size: 0.75rem;
  color: #1976d2;
  font-weight: 600;
  text-transform: uppercase;
}

.user-info-value,
.booking-info-value {
  font-size: 0.9rem;
  font-weight: 600;
  color: #2d3748;
  margin-top: 0.25rem;
}

.cost-highlight {
  color: #28a745 !important;
  font-size: 1.1rem !important;
}

.release-section {
  text-align: center;
  padding-top: 1rem;
  border-top: 2px solid #dee2e6;
}

.release-btn {
  background: linear-gradient(135deg, #ffc107, #e0a800);
  border: none;
  color: #212529;
  font-weight: 600;
  padding: 0.75rem 2rem;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.release-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #e0a800, #d39e00);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(255, 193, 7, 0.4);
}

/* Responsive Design */
@media (max-width: 768px) {
  .parking-grid-container {
    padding: 0.5rem;
  }
  
  .grid-header {
    padding: 1rem;
  }
  
  .grid-stats {
    flex-direction: column;
    gap: 0.5rem;
    padding: 1rem;
  }
  
  .stat-divider {
    width: 30px;
    height: 1px;
  }
  
  .legend-items {
    gap: 1rem;
  }
  
  .parking-grid {
    grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
    gap: 8px;
  }
  
  .parking-spot {
    width: 50px;
    height: 50px;
    font-size: 0.8rem;
  }
  
  .spot-details-panel {
    margin-top: 1rem;
  }
  
  .booking-section,
  .occupied-details {
    padding: 1rem;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  
  .user-info-grid,
  .booking-info-grid {
    grid-template-columns: 1fr;
  }
  
  .booking-actions {
    flex-direction: column;
  }
  
  .quick-duration-buttons {
    justify-content: center;
  }
}

@media (max-width: 576px) {
  .grid-header {
    text-align: center;
  }
  
  .grid-stats {
    flex-direction: row;
    justify-content: center;
  }
  
  .parking-grid {
    grid-template-columns: repeat(auto-fill, minmax(45px, 1fr));
    gap: 6px;
  }
  
  .parking-spot {
    width: 45px;
    height: 45px;
    font-size: 0.7rem;
  }
  
  .cost-summary {
    padding: 1rem;
  }
  
  .booking-submit-btn,
  .release-btn {
    width: 100%;
  }
}
</style>