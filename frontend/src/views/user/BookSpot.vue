<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="fw-bold text-dark">Book Parking Spot</h2>
          <button @click="loadParkingLots" class="btn btn-outline-primary">
            <i class="bi bi-arrow-clockwise me-2"></i>Refresh
          </button>
        </div>

        <!-- Search and Filter -->
        <div class="card mb-4 shadow-sm">
          <div class="card-body">
            <div class="row g-3">
              <div class="col-md-6">
                <input
                  v-model="searchQuery"
                  type="text"
                  class="form-control"
                  placeholder="Search parking lots..."
                />
              </div>
              <div class="col-md-3">
                <select v-model="priceFilter" class="form-select">
                  <option value="">All Prices</option>
                  <option value="low">Under $5/hour</option>
                  <option value="medium">$5-$10/hour</option>
                  <option value="high">Over $10/hour</option>
                </select>
              </div>
              <div class="col-md-3">
                <select v-model="availabilityFilter" class="form-select">
                  <option value="">All Lots</option>
                  <option value="available">Available Spots</option>
                  <option value="full">Full Lots</option>
                </select>
              </div>
            </div>
          </div>
        </div>

        <!-- Parking Lots Grid -->
        <div class="row g-4">
          <div
            v-for="lot in filteredLots"
            :key="lot.id"
            class="col-lg-4 col-md-6"
          >
            <div class="card h-100 shadow-sm card-hover">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-3">
                  <h5 class="card-title fw-bold">{{ lot.name }}</h5>
                  <span class="badge bg-primary">${{ lot.price_per_hour }}/hr</span>
                </div>
                
                <div class="mb-3">
                  <p class="text-muted mb-1">
                    <i class="bi bi-geo-alt me-2"></i>{{ lot.location }}
                  </p>
                  <p class="text-muted small mb-0">{{ lot.address }}</p>
                </div>
                
                <div class="row text-center mb-3">
                  <div class="col-6">
                    <div class="h4 fw-bold text-primary">{{ lot.total_spots }}</div>
                    <small class="text-muted">Total Spots</small>
                  </div>
                  <div class="col-6">
                    <div class="h4 fw-bold" :class="lot.available_spots > 0 ? 'text-success' : 'text-danger'">
                      {{ lot.available_spots }}
                    </div>
                    <small class="text-muted">Available</small>
                  </div>
                </div>
                
                <div class="progress mb-3" style="height: 8px;">
                  <div
                    class="progress-bar"
                    :class="getOccupancyColor(lot)"
                    :style="{ width: getOccupancyPercentage(lot) + '%' }"
                  ></div>
                </div>
                
                <button
                  @click="viewParkingGrid(lot)"
                  class="btn btn-primary w-100 btn-hover"
                  :disabled="lot.available_spots === 0"
                >
                  <i class="bi bi-grid-3x3-gap me-2"></i>
                  {{ lot.available_spots > 0 ? 'View & Book Spots' : 'Fully Occupied' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="filteredLots.length === 0" class="text-center py-5">
          <div class="text-muted">
            <i class="bi bi-search display-1"></i>
            <h4 class="mt-3">No parking lots found</h4>
            <p>Try adjusting your search criteria</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Parking Grid Modal -->
    <div v-if="selectedLot" class="modal fade show d-block" style="background: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ selectedLot.name }} - Select Parking Spot</h5>
            <button @click="selectedLot = null" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <ParkingGrid :lot="selectedLot" :show-booking-form="true" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import ParkingGrid from '../../components/ParkingGrid.vue'
import { getApiUrl } from '../../config/api'
import type { ParkingLot } from '../../stores/parking'

const parkingLots = ref<ParkingLot[]>([])
const selectedLot = ref<ParkingLot | null>(null)
const searchQuery = ref('')
const priceFilter = ref('')
const availabilityFilter = ref('')
const loading = ref(false)

const filteredLots = computed(() => {
  let filtered = parkingLots.value

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(lot =>
      lot.name.toLowerCase().includes(query) ||
      lot.location.toLowerCase().includes(query) ||
      lot.address.toLowerCase().includes(query)
    )
  }

  // Price filter
  if (priceFilter.value) {
    filtered = filtered.filter(lot => {
      switch (priceFilter.value) {
        case 'low': return lot.price_per_hour < 5
        case 'medium': return lot.price_per_hour >= 5 && lot.price_per_hour <= 10
        case 'high': return lot.price_per_hour > 10
        default: return true
      }
    })
  }

  // Availability filter
  if (availabilityFilter.value) {
    filtered = filtered.filter(lot => {
      switch (availabilityFilter.value) {
        case 'available': return lot.available_spots > 0
        case 'full': return lot.available_spots === 0
        default: return true
      }
    })
  }

  return filtered
})

onMounted(() => {
  loadParkingLots()
})

const loadParkingLots = async () => {
  loading.value = true
  try {
    const response = await fetch(getApiUrl('/api/parking-lots'))
    if (response.ok) {
      parkingLots.value = await response.json()
    }
  } catch (error) {
    console.error('Error loading parking lots:', error)
  } finally {
    loading.value = false
  }
}

const viewParkingGrid = (lot: ParkingLot) => {
  selectedLot.value = lot
}

const getOccupancyPercentage = (lot: ParkingLot) => {
  return ((lot.total_spots - lot.available_spots) / lot.total_spots) * 100
}

const getOccupancyColor = (lot: ParkingLot) => {
  const percentage = getOccupancyPercentage(lot)
  if (percentage < 50) return 'bg-success'
  if (percentage < 80) return 'bg-warning'
  return 'bg-danger'
}
</script>

<style scoped>
.card-hover {
  transition: all 0.3s ease;
}

.card-hover:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
}

.btn-hover {
  transition: all 0.3s ease;
}

.btn-hover:hover {
  transform: translateY(-2px);
}

.modal.show {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>