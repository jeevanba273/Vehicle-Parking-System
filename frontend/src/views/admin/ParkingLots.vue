<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="fw-bold text-dark">Parking Lots Management</h2>
          <button
            @click="showAddModal = true"
            class="btn btn-primary btn-lg"
          >
            <i class="bi bi-plus-circle me-2"></i>Add Parking Lot
          </button>
        </div>

        <!-- Search and Filter -->
        <div class="card mb-4 shadow-sm">
          <div class="card-body">
            <div class="row g-3">
              <div class="col-md-6">
                <div class="input-group">
                  <span class="input-group-text"><i class="bi bi-search"></i></span>
                  <input
                    v-model="searchQuery"
                    type="text"
                    class="form-control"
                    placeholder="Search parking lots..."
                  />
                </div>
              </div>
              <div class="col-md-3">
                <select v-model="locationFilter" class="form-select">
                  <option value="">All Locations</option>
                  <option value="City Center">City Center</option>
                  <option value="West District">West District</option>
                  <option value="Financial Center">Financial Center</option>
                </select>
              </div>
              <div class="col-md-3">
                <button @click="loadParkingLots" class="btn btn-outline-primary w-100">
                  <i class="bi bi-arrow-clockwise me-2"></i>Refresh
                </button>
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
                  <div class="dropdown">
                    <button class="btn btn-outline-secondary btn-sm" data-bs-toggle="dropdown">
                      <i class="bi bi-three-dots-vertical"></i>
                    </button>
                    <ul class="dropdown-menu">
                      <li><a class="dropdown-item" @click="editLot(lot)" href="#"><i class="bi bi-pencil me-2"></i>Edit</a></li>
                      <li><a class="dropdown-item" @click="viewSpots(lot)" href="#"><i class="bi bi-grid-3x3-gap me-2"></i>View Grid</a></li>
                      <li><hr class="dropdown-divider"></li>
                      <li><a class="dropdown-item text-danger" @click="deleteLot(lot.id)" href="#"><i class="bi bi-trash me-2"></i>Delete</a></li>
                    </ul>
                  </div>
                </div>
                
                <div class="mb-3">
                  <p class="text-muted mb-1">
                    <i class="bi bi-geo-alt me-2"></i>{{ lot.location }}
                  </p>
                  <p class="text-muted small mb-2">{{ lot.address }}</p>
                  <p class="text-primary fw-bold mb-0">
                    <i class="bi bi-currency-dollar me-1"></i>${{ lot.price_per_hour }}/hour
                  </p>
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
                
                <div class="progress mb-3" style="height: 10px;">
                  <div
                    class="progress-bar"
                    :class="getOccupancyColor(lot)"
                    :style="{ width: getOccupancyPercentage(lot) + '%' }"
                  ></div>
                </div>
                
                <button
                  @click="viewSpots(lot)"
                  class="btn btn-outline-primary w-100"
                >
                  <i class="bi bi-grid-3x3-gap me-2"></i>View Parking Grid
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-if="filteredLots.length === 0" class="text-center py-5">
          <div class="text-muted">
            <i class="bi bi-building display-1"></i>
            <h4 class="mt-3">No parking lots found</h4>
            <p>Try adjusting your search criteria or add a new parking lot</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div v-if="showAddModal || editingLot" class="modal fade show d-block" style="background: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-building me-2"></i>
              {{ editingLot ? 'Edit Parking Lot' : 'Add New Parking Lot' }}
            </h5>
            <button @click="closeModal" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveLot">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label fw-medium">Name</label>
                  <input
                    v-model="lotForm.name"
                    type="text"
                    class="form-control"
                    required
                    placeholder="Enter parking lot name"
                  />
                </div>
                
                <div class="col-md-6">
                  <label class="form-label fw-medium">Location</label>
                  <input
                    v-model="lotForm.location"
                    type="text"
                    class="form-control"
                    required
                    placeholder="Enter location"
                  />
                </div>
                
                <div class="col-12">
                  <label class="form-label fw-medium">Address</label>
                  <textarea
                    v-model="lotForm.address"
                    class="form-control"
                    rows="3"
                    required
                    placeholder="Enter full address"
                  ></textarea>
                </div>
                
                <div class="col-md-6">
                  <label class="form-label fw-medium">Total Spots</label>
                  <input
                    v-model.number="lotForm.total_spots"
                    type="number"
                    class="form-control"
                    min="1"
                    max="500"
                    required
                  />
                </div>
                
                <div class="col-md-6">
                  <label class="form-label fw-medium">Price per Hour ($)</label>
                  <input
                    v-model.number="lotForm.price_per_hour"
                    type="number"
                    class="form-control"
                    min="0"
                    step="0.01"
                    required
                  />
                </div>
              </div>
              
              <div class="d-flex gap-3 mt-4">
                <button type="submit" class="btn btn-primary flex-fill" :disabled="saving">
                  <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="bi bi-check-circle me-2"></i>
                  {{ saving ? 'Saving...' : (editingLot ? 'Update' : 'Add') }} Lot
                </button>
                <button
                  type="button"
                  @click="closeModal"
                  class="btn btn-secondary flex-fill"
                >
                  <i class="bi bi-x-circle me-2"></i>Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Parking Grid Modal -->
    <div v-if="selectedLot" class="modal fade show d-block" style="background: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-grid-3x3-gap me-2"></i>{{ selectedLot.name }} - Parking Grid
            </h5>
            <button @click="selectedLot = null" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <ParkingGrid :lot="selectedLot" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, reactive, onMounted } from 'vue'
import { useParkingStore } from '../../stores/parking'
import ParkingGrid from '../../components/ParkingGrid.vue'
import type { ParkingLot } from '../../stores/parking'

const parkingStore = useParkingStore()

const searchQuery = ref('')
const locationFilter = ref('')
const showAddModal = ref(false)
const editingLot = ref<ParkingLot | null>(null)
const selectedLot = ref<ParkingLot | null>(null)
const saving = ref(false)

const lotForm = reactive({
  name: '',
  location: '',
  address: '',
  total_spots: 10,
  price_per_hour: 5
})

const filteredLots = computed(() => {
  let filtered = parkingStore.parkingLots

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(lot =>
      lot.name.toLowerCase().includes(query) ||
      lot.location.toLowerCase().includes(query) ||
      lot.address.toLowerCase().includes(query)
    )
  }

  if (locationFilter.value) {
    filtered = filtered.filter(lot => lot.location === locationFilter.value)
  }

  return filtered
})

onMounted(() => {
  loadParkingLots()
})

const loadParkingLots = async () => {
  await parkingStore.fetchParkingLots()
}

const editLot = (lot: ParkingLot) => {
  editingLot.value = lot
  Object.assign(lotForm, {
    name: lot.name,
    location: lot.location,
    address: lot.address,
    total_spots: lot.total_spots,
    price_per_hour: lot.price_per_hour
  })
}

const deleteLot = async (id: string) => {
  if (confirm('Are you sure you want to delete this parking lot? This action cannot be undone.')) {
    const success = await parkingStore.deleteParkingLot(id)
    if (success) {
      alert('Parking lot deleted successfully!')
    } else {
      alert('Failed to delete parking lot')
    }
  }
}

const viewSpots = (lot: ParkingLot) => {
  selectedLot.value = lot
}

const saveLot = async () => {
  saving.value = true
  
  try {
    let success = false
    
    if (editingLot.value) {
      success = await parkingStore.updateParkingLot(editingLot.value.id, lotForm)
    } else {
      success = await parkingStore.createParkingLot(lotForm)
    }
    
    if (success) {
      closeModal()
      alert(`Parking lot ${editingLot.value ? 'updated' : 'created'} successfully!`)
    } else {
      alert(`Failed to ${editingLot.value ? 'update' : 'create'} parking lot`)
    }
  } finally {
    saving.value = false
  }
}

const closeModal = () => {
  showAddModal.value = false
  editingLot.value = null
  Object.assign(lotForm, {
    name: '',
    location: '',
    address: '',
    total_spots: 10,
    price_per_hour: 5
  })
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

.modal.show {
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>