<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12">
        <!-- Enhanced Header with Quick Stats -->
        <div class="dashboard-header mb-4">
          <div class="row align-items-center">
            <div class="col-md-6">
              <h2 class="fw-bold text-dark mb-2">
                <i class="bi bi-building-gear me-2 text-primary"></i>Parking Lots Management
              </h2>
              <p class="text-muted mb-0">Manage and monitor all parking facilities</p>
            </div>
            <div class="col-md-6 text-md-end">
              <div class="d-flex gap-2 justify-content-md-end">
                <div class="quick-stat">
                  <div class="stat-value">{{ parkingStore.parkingLots.length }}</div>
                  <div class="stat-label">Total Lots</div>
                </div>
                <div class="quick-stat">
                  <div class="stat-value">{{ totalSpots }}</div>
                  <div class="stat-label">Total Spots</div>
                </div>
                <div class="quick-stat">
                  <div class="stat-value">{{ availableSpots }}</div>
                  <div class="stat-label">Available</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Enhanced Action Bar -->
        <div class="action-bar mb-4">
          <div class="row g-3">
            <div class="col-md-4">
              <div class="search-container">
                <i class="bi bi-search search-icon"></i>
                <input
                  v-model="searchQuery"
                  type="text"
                  class="form-control search-input"
                  placeholder="Search parking lots, locations..."
                />
                <button v-if="searchQuery" @click="searchQuery = ''" class="clear-search">
                  <i class="bi bi-x"></i>
                </button>
              </div>
            </div>
            <div class="col-md-3">
              <select v-model="locationFilter" class="form-select filter-select">
                <option value="">All Locations</option>
                <option value="City Center">City Center</option>
                <option value="West District">West District</option>
                <option value="Financial Center">Financial Center</option>
                <option value="Shopping District">Shopping District</option>
                <option value="Business Park">Business Park</option>
              </select>
            </div>
            <div class="col-md-3">
              <select v-model="sortBy" class="form-select filter-select">
                <option value="name">Sort by Name</option>
                <option value="availability">By Availability</option>
                <option value="price">By Price</option>
                <option value="size">By Size</option>
                <option value="newest">Newest First</option>
              </select>
            </div>
            <div class="col-md-2">
              <div class="d-flex gap-2">
                <button @click="loadParkingLots" class="btn btn-outline-primary refresh-btn">
                  <i class="bi bi-arrow-clockwise"></i>
                </button>
                <button @click="showAddModal = true" class="btn btn-primary add-btn">
                  <i class="bi bi-plus-lg me-1"></i>Add Lot
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Enhanced Parking Lots Grid -->
        <div class="parking-lots-grid">
          <div
            v-for="lot in filteredLots"
            :key="lot.id"
            class="parking-lot-card"
            :class="{ 'fully-occupied': lot.available_spots === 0 }"
          >
            <!-- Card Header -->
            <div class="card-header-custom">
              <div class="d-flex justify-content-between align-items-start">
                <div class="lot-info">
                  <h5 class="lot-name">{{ lot.name }}</h5>
                  <div class="lot-location">
                    <i class="bi bi-geo-alt me-1"></i>{{ lot.location }}
                  </div>
                </div>
                <div class="lot-actions">
                  <div class="dropdown">
                    <button class="btn btn-ghost btn-sm" data-bs-toggle="dropdown">
                      <i class="bi bi-three-dots-vertical"></i>
                    </button>
                    <ul class="dropdown-menu dropdown-menu-end">
                      <li><a class="dropdown-item" @click="editLot(lot)"><i class="bi bi-pencil me-2"></i>Edit Details</a></li>
                      <li><a class="dropdown-item" @click="viewSpots(lot)"><i class="bi bi-grid-3x3-gap me-2"></i>View Grid</a></li>
                      <li><a class="dropdown-item" @click="duplicateLot(lot)"><i class="bi bi-copy me-2"></i>Duplicate</a></li>
                      <li><hr class="dropdown-divider"></li>
                      <li><a class="dropdown-item text-danger" @click="deleteLot(lot.id)"><i class="bi bi-trash me-2"></i>Delete</a></li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>

            <!-- Card Body -->
            <div class="card-body-custom">
              <div class="lot-address mb-3">
                <i class="bi bi-building me-2 text-muted"></i>
                <span class="text-muted">{{ lot.address }}</span>
              </div>

              <!-- Stats Grid -->
              <div class="stats-grid mb-3">
                <div class="stat-item">
                  <div class="stat-icon bg-primary">
                    <i class="bi bi-grid-3x3-gap"></i>
                  </div>
                  <div class="stat-content">
                    <div class="stat-number">{{ lot.total_spots }}</div>
                    <div class="stat-text">Total Spots</div>
                  </div>
                </div>
                <div class="stat-item">
                  <div class="stat-icon" :class="lot.available_spots > 0 ? 'bg-success' : 'bg-danger'">
                    <i class="bi bi-car-front"></i>
                  </div>
                  <div class="stat-content">
                    <div class="stat-number">{{ lot.available_spots }}</div>
                    <div class="stat-text">Available</div>
                  </div>
                </div>
                <div class="stat-item">
                  <div class="stat-icon bg-warning">
                    <i class="bi bi-currency-dollar"></i>
                  </div>
                  <div class="stat-content">
                    <div class="stat-number">${{ lot.price_per_hour }}</div>
                    <div class="stat-text">Per Hour</div>
                  </div>
                </div>
              </div>

              <!-- Occupancy Progress -->
              <div class="occupancy-section mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="occupancy-label">Occupancy Rate</span>
                  <span class="occupancy-percentage">{{ getOccupancyPercentage(lot) }}%</span>
                </div>
                <div class="progress-container">
                  <div
                    class="progress-bar-custom"
                    :class="getOccupancyColor(lot)"
                    :style="{ width: getOccupancyPercentage(lot) + '%' }"
                  ></div>
                </div>
              </div>

              <!-- Revenue Estimate -->
              <div class="revenue-estimate mb-3">
                <div class="d-flex justify-content-between">
                  <span class="text-muted">Daily Revenue Potential:</span>
                  <span class="fw-bold text-success">${{ calculateDailyRevenue(lot) }}</span>
                </div>
              </div>
            </div>

            <!-- Card Footer -->
            <div class="card-footer-custom">
              <div class="d-flex gap-2">
                <button @click="viewSpots(lot)" class="btn btn-primary btn-sm flex-fill">
                  <i class="bi bi-grid-3x3-gap me-1"></i>View Grid
                </button>
                <button @click="editLot(lot)" class="btn btn-outline-secondary btn-sm">
                  <i class="bi bi-pencil"></i>
                </button>
                <button @click="generateReport(lot)" class="btn btn-outline-info btn-sm">
                  <i class="bi bi-file-earmark-text"></i>
                </button>
              </div>
            </div>

            <!-- Status Badge -->
            <div class="status-badge" :class="getStatusBadgeClass(lot)">
              {{ getStatusText(lot) }}
            </div>
          </div>

          <!-- Add New Lot Card -->
          <div class="add-lot-card" @click="showAddModal = true">
            <div class="add-lot-content">
              <div class="add-lot-icon">
                <i class="bi bi-plus-circle"></i>
              </div>
              <h6 class="add-lot-title">Add New Parking Lot</h6>
              <p class="add-lot-subtitle">Create a new parking facility</p>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="filteredLots.length === 0 && parkingStore.parkingLots.length > 0" class="empty-state">
          <div class="empty-icon">
            <i class="bi bi-search"></i>
          </div>
          <h4>No parking lots found</h4>
          <p>Try adjusting your search criteria or filters</p>
          <button @click="clearFilters" class="btn btn-outline-primary">Clear Filters</button>
        </div>

        <div v-if="parkingStore.parkingLots.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="bi bi-building"></i>
          </div>
          <h4>No parking lots yet</h4>
          <p>Get started by creating your first parking facility</p>
          <button @click="showAddModal = true" class="btn btn-primary">
            <i class="bi bi-plus-circle me-2"></i>Create First Lot
          </button>
        </div>
      </div>
    </div>

    <!-- Enhanced Add/Edit Modal -->
    <div v-if="showAddModal || editingLot" class="modal fade show d-block" style="background: rgba(0,0,0,0.6);">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content enhanced-modal">
          <div class="modal-header-enhanced">
            <div class="modal-title-section">
              <div class="modal-icon">
                <i class="bi bi-building-add"></i>
              </div>
              <div>
                <h5 class="modal-title">{{ editingLot ? 'Edit Parking Lot' : 'Create New Parking Lot' }}</h5>
                <p class="modal-subtitle">{{ editingLot ? 'Update facility details' : 'Add a new parking facility to your system' }}</p>
              </div>
            </div>
            <button @click="closeModal" class="btn-close-enhanced">
              <i class="bi bi-x"></i>
            </button>
          </div>
          
          <div class="modal-body-enhanced">
            <form @submit.prevent="saveLot" class="enhanced-form">
              <!-- Basic Information -->
              <div class="form-section">
                <h6 class="section-title">
                  <i class="bi bi-info-circle me-2"></i>Basic Information
                </h6>
                <div class="row g-3">
                  <div class="col-md-6">
                    <label class="form-label-enhanced">Facility Name</label>
                    <input
                      v-model="lotForm.name"
                      type="text"
                      class="form-control-enhanced"
                      required
                      placeholder="e.g., Downtown Plaza Parking"
                    />
                  </div>
                  <div class="col-md-6">
                    <label class="form-label-enhanced">Location District</label>
                    <select v-model="lotForm.location" class="form-control-enhanced" required>
                      <option value="">Select location</option>
                      <option value="City Center">City Center</option>
                      <option value="West District">West District</option>
                      <option value="Financial Center">Financial Center</option>
                      <option value="Shopping District">Shopping District</option>
                      <option value="Business Park">Business Park</option>
                    </select>
                  </div>
                  <div class="col-12">
                    <label class="form-label-enhanced">Full Address</label>
                    <textarea
                      v-model="lotForm.address"
                      class="form-control-enhanced"
                      rows="3"
                      required
                      placeholder="Enter complete address with landmarks"
                    ></textarea>
                  </div>
                </div>
              </div>

              <!-- Capacity & Pricing -->
              <div class="form-section">
                <h6 class="section-title">
                  <i class="bi bi-grid-3x3-gap me-2"></i>Capacity & Pricing
                </h6>
                <div class="row g-3">
                  <div class="col-md-6">
                    <label class="form-label-enhanced">Total Parking Spots</label>
                    <input
                      v-model.number="lotForm.total_spots"
                      type="number"
                      class="form-control-enhanced"
                      min="1"
                      max="1000"
                      required
                    />
                    <div class="form-hint">Recommended: 20-200 spots per facility</div>
                  </div>
                  <div class="col-md-6">
                    <label class="form-label-enhanced">Hourly Rate (USD)</label>
                    <div class="input-group">
                      <span class="input-group-text">$</span>
                      <input
                        v-model.number="lotForm.price_per_hour"
                        type="number"
                        class="form-control-enhanced"
                        min="0"
                        step="0.25"
                        required
                      />
                    </div>
                    <div class="form-hint">Market rate: $2-15 per hour</div>
                  </div>
                </div>
              </div>

              <!-- Revenue Projection -->
              <div class="form-section">
                <div class="revenue-projection">
                  <h6 class="section-title">
                    <i class="bi bi-graph-up me-2"></i>Revenue Projection
                  </h6>
                  <div class="projection-grid">
                    <div class="projection-item">
                      <div class="projection-value">${{ calculateProjectedDaily() }}</div>
                      <div class="projection-label">Daily Potential</div>
                    </div>
                    <div class="projection-item">
                      <div class="projection-value">${{ calculateProjectedMonthly() }}</div>
                      <div class="projection-label">Monthly Potential</div>
                    </div>
                    <div class="projection-item">
                      <div class="projection-value">{{ lotForm.total_spots * 8 }}</div>
                      <div class="projection-label">Daily Capacity (8h avg)</div>
                    </div>
                  </div>
                </div>
              </div>
            </form>
          </div>

          <div class="modal-footer-enhanced">
            <button type="button" @click="closeModal" class="btn btn-secondary-enhanced">
              <i class="bi bi-x-circle me-2"></i>Cancel
            </button>
            <button @click="saveLot" class="btn btn-primary-enhanced" :disabled="saving">
              <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-check-circle me-2"></i>
              {{ saving ? 'Saving...' : (editingLot ? 'Update Facility' : 'Create Facility') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Enhanced Parking Grid Modal -->
    <div v-if="selectedLot" class="modal fade show d-block" style="background: rgba(0,0,0,0.6);">
      <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content enhanced-modal">
          <div class="modal-header-enhanced">
            <div class="modal-title-section">
              <div class="modal-icon bg-primary">
                <i class="bi bi-grid-3x3-gap"></i>
              </div>
              <div>
                <h5 class="modal-title">{{ selectedLot.name }}</h5>
                <p class="modal-subtitle">Interactive parking grid management</p>
              </div>
            </div>
            <button @click="selectedLot = null" class="btn-close-enhanced">
              <i class="bi bi-x"></i>
            </button>
          </div>
          <div class="modal-body-enhanced">
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
const sortBy = ref('name')
const showAddModal = ref(false)
const editingLot = ref<ParkingLot | null>(null)
const selectedLot = ref<ParkingLot | null>(null)
const saving = ref(false)

const lotForm = reactive({
  name: '',
  location: '',
  address: '',
  total_spots: 50,
  price_per_hour: 5
})

const totalSpots = computed(() => 
  parkingStore.parkingLots.reduce((sum, lot) => sum + lot.total_spots, 0)
)

const availableSpots = computed(() => 
  parkingStore.parkingLots.reduce((sum, lot) => sum + lot.available_spots, 0)
)

const filteredLots = computed(() => {
  let filtered = [...parkingStore.parkingLots]

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(lot =>
      lot.name.toLowerCase().includes(query) ||
      lot.location.toLowerCase().includes(query) ||
      lot.address.toLowerCase().includes(query)
    )
  }

  // Location filter
  if (locationFilter.value) {
    filtered = filtered.filter(lot => lot.location === locationFilter.value)
  }

  // Sort
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'name':
        return a.name.localeCompare(b.name)
      case 'availability':
        return b.available_spots - a.available_spots
      case 'price':
        return a.price_per_hour - b.price_per_hour
      case 'size':
        return b.total_spots - a.total_spots
      case 'newest':
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      default:
        return 0
    }
  })

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

const duplicateLot = (lot: ParkingLot) => {
  Object.assign(lotForm, {
    name: `${lot.name} (Copy)`,
    location: lot.location,
    address: lot.address,
    total_spots: lot.total_spots,
    price_per_hour: lot.price_per_hour
  })
  showAddModal.value = true
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

const generateReport = (lot: ParkingLot) => {
  alert(`Generating report for ${lot.name} - Feature coming soon!`)
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
    total_spots: 50,
    price_per_hour: 5
  })
}

const clearFilters = () => {
  searchQuery.value = ''
  locationFilter.value = ''
  sortBy.value = 'name'
}

const getOccupancyPercentage = (lot: ParkingLot) => {
  return Math.round(((lot.total_spots - lot.available_spots) / lot.total_spots) * 100)
}

const getOccupancyColor = (lot: ParkingLot) => {
  const percentage = getOccupancyPercentage(lot)
  if (percentage < 50) return 'low'
  if (percentage < 80) return 'medium'
  return 'high'
}

const getStatusBadgeClass = (lot: ParkingLot) => {
  if (lot.available_spots === 0) return 'status-full'
  if (lot.available_spots <= lot.total_spots * 0.2) return 'status-limited'
  return 'status-available'
}

const getStatusText = (lot: ParkingLot) => {
  if (lot.available_spots === 0) return 'Full'
  if (lot.available_spots <= lot.total_spots * 0.2) return 'Limited'
  return 'Available'
}

const calculateDailyRevenue = (lot: ParkingLot) => {
  const avgOccupancy = 0.7 // 70% average occupancy
  const avgHours = 6 // Average parking duration
  return Math.round(lot.total_spots * avgOccupancy * avgHours * lot.price_per_hour)
}

const calculateProjectedDaily = () => {
  const avgOccupancy = 0.7
  const avgHours = 6
  return Math.round(lotForm.total_spots * avgOccupancy * avgHours * lotForm.price_per_hour)
}

const calculateProjectedMonthly = () => {
  return calculateProjectedDaily() * 30
}
</script>

<style scoped>
/* Dashboard Header */
.dashboard-header {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 16px;
  padding: 2rem;
  border: 1px solid #dee2e6;
}

.quick-stat {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-left: 0.5rem;
  min-width: 80px;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #0d6efd;
}

.stat-label {
  font-size: 0.75rem;
  color: #6c757d;
  margin-top: 0.25rem;
}

/* Action Bar */
.action-bar {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  border: 1px solid #e9ecef;
}

.search-container {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
  z-index: 2;
}

.search-input {
  padding-left: 3rem !important;
  padding-right: 3rem !important;
  border: 2px solid #e9ecef !important;
  border-radius: 12px !important;
  background: #f8f9fa !important;
  transition: all 0.3s ease !important;
}

.search-input:focus {
  border-color: #0d6efd !important;
  background: white !important;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25) !important;
}

.clear-search {
  position: absolute;
  right: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: #6c757d;
  cursor: pointer;
  z-index: 2;
}

.filter-select {
  border: 2px solid #e9ecef !important;
  border-radius: 12px !important;
  background: #f8f9fa !important;
  transition: all 0.3s ease !important;
}

.filter-select:focus {
  border-color: #0d6efd !important;
  background: white !important;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25) !important;
}

.refresh-btn, .add-btn {
  border-radius: 12px !important;
  padding: 0.75rem 1rem !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
}

.refresh-btn:hover {
  transform: rotate(180deg) !important;
}

.add-btn {
  background: linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%) !important;
  border: none !important;
}

.add-btn:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 25px rgba(13, 110, 253, 0.3) !important;
}

/* Parking Lots Grid */
.parking-lots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
  gap: 1.5rem;
}

.parking-lot-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.parking-lot-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

.parking-lot-card.fully-occupied {
  border-color: #dc3545;
  background: linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%);
}

.card-header-custom {
  padding: 1.5rem 1.5rem 0;
}

.lot-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.lot-location {
  color: #0d6efd;
  font-weight: 600;
  font-size: 0.9rem;
}

.lot-actions .btn-ghost {
  background: none;
  border: none;
  color: #6c757d;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.lot-actions .btn-ghost:hover {
  background: #f8f9fa;
  color: #0d6efd;
}

.card-body-custom {
  padding: 1.5rem;
}

.lot-address {
  font-size: 0.9rem;
  line-height: 1.4;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.stat-item:hover {
  background: #e9ecef;
  transform: scale(1.02);
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.1rem;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2d3748;
}

.stat-text {
  font-size: 0.8rem;
  color: #6c757d;
}

.occupancy-section {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1rem;
}

.occupancy-label {
  font-size: 0.9rem;
  color: #6c757d;
  font-weight: 600;
}

.occupancy-percentage {
  font-size: 1.1rem;
  font-weight: 700;
  color: #2d3748;
}

.progress-container {
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar-custom {
  height: 100%;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.progress-bar-custom.low {
  background: linear-gradient(90deg, #198754 0%, #20c997 100%);
}

.progress-bar-custom.medium {
  background: linear-gradient(90deg, #fd7e14 0%, #ffc107 100%);
}

.progress-bar-custom.high {
  background: linear-gradient(90deg, #dc3545 0%, #e74c3c 100%);
}

.revenue-estimate {
  background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid #c3e6cb;
}

.card-footer-custom {
  padding: 1.5rem;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.status-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-available {
  background: #d4edda;
  color: #155724;
}

.status-limited {
  background: #fff3cd;
  color: #856404;
}

.status-full {
  background: #f8d7da;
  color: #721c24;
}

/* Add New Lot Card */
.add-lot-card {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border: 2px dashed #dee2e6;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.add-lot-card:hover {
  border-color: #0d6efd;
  background: linear-gradient(135deg, #e7f3ff 0%, #cce7ff 100%);
  transform: translateY(-4px);
}

.add-lot-content {
  text-align: center;
  color: #6c757d;
}

.add-lot-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  color: #0d6efd;
}

.add-lot-title {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #2d3748;
}

.add-lot-subtitle {
  font-size: 0.9rem;
  margin: 0;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #6c757d;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  color: #dee2e6;
}

/* Enhanced Modal */
.enhanced-modal {
  border: none;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.modal-header-enhanced {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 1px solid #dee2e6;
  border-radius: 20px 20px 0 0;
  padding: 2rem;
}

.modal-title-section {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.modal-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  background: #0d6efd;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2d3748;
  margin: 0;
}

.modal-subtitle {
  color: #6c757d;
  margin: 0;
  font-size: 0.9rem;
}

.btn-close-enhanced {
  background: #f8f9fa;
  border: none;
  border-radius: 10px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #6c757d;
  transition: all 0.3s ease;
}

.btn-close-enhanced:hover {
  background: #e9ecef;
  color: #dc3545;
}

.modal-body-enhanced {
  padding: 2rem;
}

.form-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 16px;
  border: 1px solid #e9ecef;
}

.section-title {
  color: #2d3748;
  font-weight: 600;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.form-label-enhanced {
  color: #4a5568;
  font-weight: 600;
  margin-bottom: 0.5rem;
  display: block;
}

.form-control-enhanced {
  background: white !important;
  border: 2px solid #e2e8f0 !important;
  border-radius: 12px !important;
  padding: 0.875rem 1rem !important;
  font-size: 1rem !important;
  transition: all 0.3s ease !important;
  width: 100% !important;
}

.form-control-enhanced:focus {
  border-color: #0d6efd !important;
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25) !important;
  outline: none !important;
}

.form-hint {
  font-size: 0.8rem;
  color: #6c757d;
  margin-top: 0.25rem;
}

.revenue-projection {
  background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
  border: 1px solid #c3e6cb;
  border-radius: 16px;
  padding: 1.5rem;
}

.projection-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-top: 1rem;
}

.projection-item {
  text-align: center;
  background: white;
  padding: 1rem;
  border-radius: 12px;
  border: 1px solid #c3e6cb;
}

.projection-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #198754;
}

.projection-label {
  font-size: 0.8rem;
  color: #6c757d;
  margin-top: 0.25rem;
}

.modal-footer-enhanced {
  background: #f8f9fa;
  border-top: 1px solid #dee2e6;
  border-radius: 0 0 20px 20px;
  padding: 1.5rem 2rem;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn-secondary-enhanced, .btn-primary-enhanced {
  padding: 0.875rem 2rem !important;
  border-radius: 12px !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
}

.btn-primary-enhanced {
  background: linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%) !important;
  border: none !important;
  color: white !important;
}

.btn-primary-enhanced:hover:not(:disabled) {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 25px rgba(13, 110, 253, 0.3) !important;
}

/* Responsive Design */
@media (max-width: 768px) {
  .parking-lots-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .projection-grid {
    grid-template-columns: 1fr;
  }
  
  .dashboard-header {
    padding: 1.5rem;
  }
  
  .quick-stat {
    margin-left: 0;
    margin-top: 0.5rem;
  }
}
</style>