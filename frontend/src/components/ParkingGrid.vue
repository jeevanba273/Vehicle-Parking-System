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
        <form @submit.prevent="bookSpot" class="row g-3">
          <div class="col-md-6">
            <label class="form-label">Vehicle Number</label>
            <input
              v-model="bookingForm.vehicleNumber"
              type="text"
              class="form-control"
              required
              placeholder="Enter vehicle number"
            />
          </div>
          <div class="col-md-6">
            <label class="form-label">Hours</label>
            <select v-model="bookingForm.hours" class="form-select" required>
              <option value="1">1 Hour</option>
              <option value="2">2 Hours</option>
              <option value="4">4 Hours</option>
              <option value="8">8 Hours</option>
              <option value="24">24 Hours</option>
            </select>
          </div>
          <div class="col-12">
            <p class="mb-2">
              <strong>Total Cost: ${{ (lot.price_per_hour * bookingForm.hours).toFixed(2) }}</strong>
            </p>
            <button type="submit" class="btn btn-primary me-2" :disabled="booking">
              <span v-if="booking" class="spinner-border spinner-border-sm me-2"></span>
              {{ booking ? 'Booking...' : 'Book Spot' }}
            </button>
            <button type="button" @click="cancelBooking" class="btn btn-secondary">Cancel</button>
          </div>
        </form>
      </div>
      
      <div v-else-if="selectedSpot.status === 'occupied' && canRelease" class="mt-3">
        <p><strong>Vehicle:</strong> {{ selectedSpot.vehicle_number }}</p>
        <p><strong>Booked At:</strong> {{ formatDateTime(selectedSpot.booked_at || '') }}</p>
        <p><strong>Release Time:</strong> {{ formatDateTime(selectedSpot.release_time || '') }}</p>
        <button @click="releaseSpot" class="btn btn-warning" :disabled="releasing">
          <span v-if="releasing" class="spinner-border spinner-border-sm me-2"></span>
          {{ releasing ? 'Releasing...' : 'Release Spot' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
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
  hours: 1
})

const canRelease = computed(() => {
  return selectedSpot.value?.occupied_by === authStore.currentUser?.id
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

const bookSpot = async () => {
  if (!selectedSpot.value || !authStore.currentUser) return
  
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
        hours: bookingForm.hours
      })
    })
    
    const result = await response.json()
    
    if (result.success) {
      await loadSpots()
      selectedSpot.value = null
      bookingForm.vehicleNumber = ''
      bookingForm.hours = 1
      alert('Spot booked successfully!')
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
    const activeBooking = bookings.find((b: any) => b.spot_id === selectedSpot.value?.id && b.status === 'active')
    
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
  bookingForm.vehicleNumber = ''
  bookingForm.hours = 1
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
</style>