<template>
  <div class="parking-grid-container">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h4 class="mb-0">{{ lot.name }} - Parking Grid</h4>
      <div class="d-flex gap-3">
        <div class="d-flex align-items-center">
          <div class="parking-spot available me-2" style="width: 20px; height: 20px;"></div>
          <small>Available</small>
        </div>
        <div class="d-flex align-items-center">
          <div class="parking-spot occupied me-2" style="width: 20px; height: 20px;"></div>
          <small>Occupied</small>
        </div>
        <div class="d-flex align-items-center">
          <div class="parking-spot reserved me-2" style="width: 20px; height: 20px;"></div>
          <small>Reserved</small>
        </div>
      </div>
    </div>
    
    <div class="parking-grid">
      <div
        v-for="spot in spots"
        :key="spot.id"
        :class="['parking-spot', spot.status]"
        :title="`Spot ${spot.spot_number} - ${spot.status}`"
        @click="selectSpot(spot)"
      >
        {{ spot.spot_number }}
      </div>
    </div>
    
    <div v-if="selectedSpot" class="mt-4 p-3 border rounded bg-light">
      <h6>Selected Spot: {{ selectedSpot.spot_number }}</h6>
      <p class="mb-2">Status: <span :class="`badge bg-${getStatusColor(selectedSpot.status)}`">{{ selectedSpot.status }}</span></p>
      
      <div v-if="selectedSpot.status === 'available' && showBookingForm" class="mt-3">
        <form @submit.prevent="bookSpot" class="booking-form">
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label fw-medium">Vehicle Number</label>
              <input
                v-model="bookingForm.vehicleNumber"
                type="text"
                class="form-control booking-input"
                required
                placeholder="Enter vehicle number"
              />
            </div>
            <div class="col-md-6">
              <label class="form-label fw-medium">Parking Duration</label>
              <div class="time-input-container">
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
                <div class="mt-2">
                  <small class="text-muted">
                    Total Duration: {{ formatDuration(bookingForm.totalHours) }}
                    <span v-if="bookingForm.totalHours < 0.25" class="text-warning">
                      (Minimum 15 minutes)
                    </span>
                  </small>
                </div>
                <div class="mt-1">
                  <div class="btn-group btn-group-sm" role="group">
                    <button type="button" class="btn btn-outline-secondary" @click="setQuickTime(0.25)">15min</button>
                    <button type="button" class="btn btn-outline-secondary" @click="setQuickTime(0.5)">30min</button>
                    <button type="button" class="btn btn-outline-secondary" @click="setQuickTime(1)">1hr</button>
                    <button type="button" class="btn btn-outline-secondary" @click="setQuickTime(2)">2hrs</button>
                    <button type="button" class="btn btn-outline-secondary" @click="setQuickTime(4)">4hrs</button>
                    <button type="button" class="btn btn-outline-secondary" @click="setQuickTime(8)">8hrs</button>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-12">
              <div class="cost-summary p-3 bg-white rounded border">
                <div class="row">
                  <div class="col-6">
                    <small class="text-muted">Rate per hour:</small>
                    <div class="fw-bold">${{ lot.price_per_hour.toFixed(2) }}</div>
                  </div>
                  <div class="col-6">
                    <small class="text-muted">Duration:</small>
                    <div class="fw-bold">{{ formatDuration(bookingForm.totalHours) }}</div>
                  </div>
                </div>
                <hr class="my-2">
                <div class="d-flex justify-content-between align-items-center">
                  <span class="fw-bold">Total Cost:</span>
                  <span class="h5 fw-bold text-primary mb-0">${{ calculateTotalCost().toFixed(2) }}</span>
                </div>
              </div>
            </div>
            <div class="col-12">
              <button 
                type="submit" 
                class="btn btn-primary me-2 booking-submit-btn" 
                :disabled="booking || bookingForm.totalHours < 0.25"
              >
                <span v-if="booking" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else class="bi bi-check-circle me-2"></i>
                {{ booking ? 'Booking...' : 'Book Spot' }}
              </button>
              <button type="button" @click="cancelBooking" class="btn btn-secondary">
                <i class="bi bi-x-circle me-2"></i>Cancel
              </button>
            </div>
          </div>
        </form>
      </div>
      
      <div v-else-if="selectedSpot.status === 'occupied'" class="mt-3">
        <div class="occupied-info p-3 bg-white rounded border">
          <div class="row g-2">
            <div class="col-md-6">
              <small class="text-muted">Vehicle:</small>
              <div class="fw-bold">{{ selectedSpot.vehicle_number }}</div>
            </div>
            <div class="col-md-6">
              <small class="text-muted">Booked At:</small>
              <div class="fw-bold">{{ formatDateTime(selectedSpot.booked_at || '') }}</div>
            </div>
            <div class="col-md-6">
              <small class="text-muted">Release Time:</small>
              <div class="fw-bold">{{ formatDateTime(selectedSpot.release_time || '') }}</div>
            </div>
            <div class="col-md-6">
              <small class="text-muted">Time Remaining:</small>
              <div class="fw-bold" :class="getTimeRemainingColor(selectedSpot.release_time || '')">
                {{ getTimeRemaining(selectedSpot.release_time || '') }}
              </div>
            </div>
            
            <!-- Show user details for admin -->
            <div v-if="isAdmin && selectedSpot.user_details" class="col-12 mt-3">
              <div class="user-details-card p-3 bg-info bg-opacity-10 rounded border border-info">
                <h6 class="text-info mb-2">
                  <i class="bi bi-person-circle me-2"></i>User Details
                </h6>
                <div class="row g-2">
                  <div class="col-md-6">
                    <small class="text-muted">Name:</small>
                    <div class="fw-bold">{{ selectedSpot.user_details.fullname }}</div>
                  </div>
                  <div class="col-md-6">
                    <small class="text-muted">Email:</small>
                    <div class="fw-bold">{{ selectedSpot.user_details.email }}</div>
                  </div>
                  <div class="col-md-6">
                    <small class="text-muted">Address:</small>
                    <div class="fw-bold">{{ selectedSpot.user_details.address }}</div>
                  </div>
                  <div class="col-md-6">
                    <small class="text-muted">PIN Code:</small>
                    <div class="fw-bold">{{ selectedSpot.user_details.pin_code }}</div>
                  </div>
                </div>
                
                <!-- Show booking details -->
                <div v-if="selectedSpot.booking_details" class="mt-3 pt-3 border-top border-info">
                  <h6 class="text-info mb-2">
                    <i class="bi bi-calendar-check me-2"></i>Booking Details
                  </h6>
                  <div class="row g-2">
                    <div class="col-md-6">
                      <small class="text-muted">Duration:</small>
                      <div class="fw-bold">{{ formatDuration(selectedSpot.booking_details.duration_hours) }}</div>
                    </div>
                    <div class="col-md-6">
                      <small class="text-muted">Total Cost:</small>
                      <div class="fw-bold text-success">${{ selectedSpot.booking_details.total_cost.toFixed(2) }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Release button for user's own booking -->
        <div v-if="canRelease" class="mt-3">
          <button @click="releaseSpot" class="btn btn-warning" :disabled="releasing">
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
    alert('Minimum booking duration is 15 minutes')
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
      alert(`Spot booked successfully for ${formatDuration(bookingForm.totalHours)}!`)
    } else {
      alert(result.message || 'Failed to book spot')
    }
  } catch (error) {
    console.error('Error booking spot:', error)
    alert('Error booking spot')
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
        alert('Spot released successfully!')
      } else {
        alert(result.message || 'Failed to release spot')
      }
    } else {
      alert('No active booking found for this spot')
    }
  } catch (error) {
    console.error('Error releasing spot:', error)
    alert('Error releasing spot')
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

const getStatusColor = (status: string) => {
  switch (status) {
    case 'available': return 'success'
    case 'occupied': return 'danger'
    case 'reserved': return 'warning'
    default: return 'secondary'
  }
}

const formatDateTime = (dateString: string) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleString()
}

const getTimeRemaining = (releaseTime: string) => {
  if (!releaseTime) return 'N/A'
  
  const now = new Date()
  const release = new Date(releaseTime)
  const diff = release.getTime() - now.getTime()
  
  if (diff <= 0) return 'Expired'
  
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60))
  
  if (hours > 0) {
    return `${hours}h ${minutes}m`
  } else {
    return `${minutes}m`
  }
}

const getTimeRemainingColor = (releaseTime: string) => {
  if (!releaseTime) return 'text-muted'
  
  const now = new Date()
  const release = new Date(releaseTime)
  const diff = release.getTime() - now.getTime()
  const minutes = diff / (1000 * 60)
  
  if (minutes <= 0) return 'text-danger'
  if (minutes <= 30) return 'text-warning'
  return 'text-success'
}
</script>

<style scoped>
.parking-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(50px, 1fr));
  gap: 8px;
  max-width: 600px;
  margin: 0 auto;
}

.parking-spot {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
  color: white;
  border: 2px solid transparent;
}

.parking-spot.available {
  background-color: var(--bs-success);
}

.parking-spot.occupied {
  background-color: var(--bs-danger);
}

.parking-spot.reserved {
  background-color: var(--bs-warning);
  color: var(--bs-dark);
}

.parking-spot:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
  border-color: var(--bs-primary);
}

.parking-grid-container {
  max-width: 800px;
  margin: 0 auto;
}

.booking-form {
  position: relative;
  z-index: 10;
}

.booking-input {
  background: #f8f9fa !important;
  border: 2px solid #e9ecef !important;
  border-radius: 8px !important;
  padding: 0.5rem 0.75rem !important;
  font-size: 0.9rem !important;
  transition: all 0.3s ease !important;
  cursor: text !important;
  pointer-events: auto !important;
  position: relative !important;
  z-index: 11 !important;
}

.booking-input:focus {
  background: #ffffff !important;
  border-color: #0d6efd !important;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25) !important;
  outline: none !important;
}

.booking-submit-btn {
  cursor: pointer !important;
  pointer-events: auto !important;
  user-select: none !important;
  position: relative !important;
  z-index: 15 !important;
  background: linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%) !important;
  border: none !important;
  color: white !important;
  font-weight: 600 !important;
  padding: 0.75rem 1.5rem !important;
  border-radius: 8px !important;
  transition: all 0.3s ease !important;
}

.booking-submit-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #0b5ed7 0%, #0a58ca 100%) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 20px rgba(13, 110, 253, 0.4) !important;
}

.booking-submit-btn:disabled {
  opacity: 0.6 !important;
  cursor: not-allowed !important;
  pointer-events: none !important;
}

.time-input-container {
  position: relative;
  z-index: 10;
}

.cost-summary {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
  border: 2px solid #dee2e6 !important;
}

.occupied-info {
  background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%) !important;
  border: 2px solid #ffc107 !important;
}

.user-details-card {
  background: linear-gradient(135deg, #e7f3ff 0%, #cce7ff 100%) !important;
  border: 2px solid #0dcaf0 !important;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.btn-group-sm .btn {
  padding: 0.25rem 0.5rem !important;
  font-size: 0.75rem !important;
  cursor: pointer !important;
  pointer-events: auto !important;
  user-select: none !important;
  position: relative !important;
  z-index: 12 !important;
}

.input-group-text {
  background: #e9ecef !important;
  border: 2px solid #e9ecef !important;
  color: #6c757d !important;
  font-size: 0.8rem !important;
  font-weight: 600 !important;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .parking-spot {
    width: 40px;
    height: 40px;
    font-size: 10px;
  }
  
  .parking-grid {
    grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
    gap: 6px;
  }
  
  .btn-group-sm .btn {
    padding: 0.2rem 0.4rem !important;
    font-size: 0.7rem !important;
  }
}
</style>