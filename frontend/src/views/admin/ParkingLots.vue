<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12">
        <!-- Enhanced Hero Section -->
        <div class="hero-section mb-5">
          <div class="hero-content">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <div>
                <h1 class="hero-title">
                  <i class="bi bi-building-gear me-3"></i>
                  Parking Lots Management
                </h1>
                <p class="hero-subtitle">Manage your parking infrastructure with advanced controls</p>
              </div>
              <button
                @click="showAddModal = true"
                class="btn btn-primary btn-lg hero-cta"
              >
                <i class="bi bi-plus-circle me-2"></i>Add Parking Lot
              </button>
            </div>

            <!-- Enhanced Search and Filter Section -->
            <div class="search-filter-section">
              <div class="row g-3 align-items-center">
                <div class="col-md-5">
                  <div class="search-wrapper">
                    <div class="input-group search-input-group">
                      <span class="input-group-text search-icon">
                        <i class="bi bi-search"></i>
                      </span>
                      <input
                        v-model="searchQuery"
                        type="text"
                        class="form-control search-input"
                        placeholder="Search parking lots, locations, addresses..."
                      />
                      <button v-if="searchQuery" @click="searchQuery = ''" class="btn btn-outline-secondary clear-search">
                        <i class="bi bi-x"></i>
                      </button>
                    </div>
                  </div>
                </div>
                <div class="col-md-3">
                  <select v-model="locationFilter" class="form-select filter-select">
                    <option value="">All Locations</option>
                    <option value="City Center">City Center</option>
                    <option value="West District">West District</option>
                    <option value="Financial Center">Financial Center</option>
                  </select>
                </div>
                <div class="col-md-2">
                  <select v-model="sortBy" class="form-select filter-select">
                    <option value="name">Sort by Name</option>
                    <option value="occupancy">By Occupancy</option>
                    <option value="price">By Price</option>
                    <option value="newest">Newest First</option>
                  </select>
                </div>
                <div class="col-md-2">
                  <button @click="loadParkingLots" class="btn btn-outline-primary w-100 refresh-btn">
                    <i class="bi bi-arrow-clockwise me-2"></i>Refresh
                  </button>
                </div>
              </div>
            </div>

            <!-- Quick Stats -->
            <div class="quick-stats mt-4">
              <div class="row g-3">
                <div class="col-md-3">
                  <div class="stat-card">
                    <div class="stat-icon bg-primary">
                      <i class="bi bi-building"></i>
                    </div>
                    <div class="stat-content">
                      <div class="stat-number">{{ totalLots }}</div>
                      <div class="stat-label">Total Lots</div>
                    </div>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="stat-card">
                    <div class="stat-icon bg-success">
                      <i class="bi bi-grid-3x3-gap"></i>
                    </div>
                    <div class="stat-content">
                      <div class="stat-number">{{ totalSpots }}</div>
                      <div class="stat-label">Total Spots</div>
                    </div>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="stat-card">
                    <div class="stat-icon bg-warning">
                      <i class="bi bi-car-front"></i>
                    </div>
                    <div class="stat-content">
                      <div class="stat-number">{{ occupiedSpots }}</div>
                      <div class="stat-label">Occupied</div>
                    </div>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="stat-card">
                    <div class="stat-icon bg-info">
                      <i class="bi bi-percent"></i>
                    </div>
                    <div class="stat-content">
                      <div class="stat-number">{{ averageOccupancy }}%</div>
                      <div class="stat-label">Avg Occupancy</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Enhanced Parking Lots Grid -->
        <div class="lots-grid-section">
          <div class="row g-4">
            <div
              v-for="lot in filteredLots"
              :key="lot.id"
              class="col-xl-4 col-lg-6"
            >
              <div class="parking-lot-card">
                <div class="card-header-custom">
                  <div class="d-flex justify-content-between align-items-start">
                    <div>
                      <h5 class="lot-title">{{ lot.name }}</h5>
                      <p class="lot-location">
                        <i class="bi bi-geo-alt me-1"></i>{{ lot.location }}
                      </p>
                    </div>
                    <div class="dropdown">
                      <button class="btn btn-outline-secondary btn-sm dropdown-toggle" data-bs-toggle="dropdown">
                        <i class="bi bi-three-dots"></i>
                      </button>
                      <ul class="dropdown-menu">
                        <li><a class="dropdown-item" @click="editLot(lot)" href="#"><i class="bi bi-pencil me-2"></i>Edit Details</a></li>
                        <li><a class="dropdown-item" @click="viewSpots(lot)" href="#"><i class="bi bi-grid-3x3-gap me-2"></i>View Grid</a></li>
                        <li><a class="dropdown-item" @click="viewAnalytics(lot)" href="#"><i class="bi bi-graph-up me-2"></i>Analytics</a></li>
                        <li><hr class="dropdown-divider"></li>
                        <li><a class="dropdown-item text-danger" @click="deleteLot(lot.id)" href="#"><i class="bi bi-trash me-2"></i>Delete</a></li>
                      </ul>
                    </div>
                  </div>
                </div>
                
                <div class="card-body-custom">
                  <div class="lot-address mb-3">
                    <small class="text-muted">{{ lot.address }}</small>
                  </div>
                  
                  <div class="pricing-info mb-3">
                    <div class="price-tag">
                      <i class="bi bi-currency-dollar"></i>
                      <span class="price">${{ lot.price_per_hour }}</span>
                      <span class="period">/hour</span>
                    </div>
                  </div>
                  
                  <div class="occupancy-section mb-3">
                    <div class="occupancy-header">
                      <span class="occupancy-label">Occupancy Status</span>
                      <span class="occupancy-percentage" :class="getOccupancyColorClass(lot)">
                        {{ getOccupancyPercentage(lot) }}%
                      </span>
                    </div>
                    
                    <div class="occupancy-bar mb-2">
                      <div
                        class="occupancy-fill"
                        :class="getOccupancyColor(lot)"
                        :style="{ width: getOccupancyPercentage(lot) + '%' }"
                      ></div>
                    </div>
                    
                    <div class="spots-info">
                      <div class="spots-stat">
                        <span class="spots-number">{{ lot.available_spots }}</span>
                        <span class="spots-label">Available</span>
                      </div>
                      <div class="spots-divider">/</div>
                      <div class="spots-stat">
                        <span class="spots-number">{{ lot.total_spots }}</span>
                        <span class="spots-label">Total</span>
                      </div>
                    </div>
                  </div>
                  
                  <div class="action-buttons">
                    <button
                      @click="viewSpots(lot)"
                      class="btn btn-primary btn-action"
                    >
                      <i class="bi bi-grid-3x3-gap me-2"></i>Manage Spots
                    </button>
                    <button
                      @click="viewAnalytics(lot)"
                      class="btn btn-outline-info btn-action"
                    >
                      <i class="bi bi-graph-up me-2"></i>Analytics
                    </button>
                  </div>
                </div>
                
                <!-- Status Indicator -->
                <div class="status-indicator" :class="getStatusIndicatorClass(lot)">
                  <i :class="getStatusIcon(lot)"></i>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="filteredLots.length === 0" class="empty-state">
            <div class="empty-state-content">
              <div class="empty-state-icon">
                <i class="bi bi-building"></i>
              </div>
              <h4 class="empty-state-title">No parking lots found</h4>
              <p class="empty-state-text">
                {{ parkingStore.parkingLots.length === 0 
                  ? 'Get started by creating your first parking lot' 
                  : 'Try adjusting your search criteria or filters' }}
              </p>
              <button v-if="parkingStore.parkingLots.length === 0" @click="showAddModal = true" class="btn btn-primary">
                <i class="bi bi-plus-circle me-2"></i>Create First Parking Lot
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Enhanced Add/Edit Modal -->
    <div v-if="showAddModal || editingLot" class="modal fade show d-block" style="background: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content enhanced-modal">
          <div class="modal-header enhanced-modal-header">
            <h5 class="modal-title">
              <i class="bi bi-building me-2"></i>
              {{ editingLot ? 'Edit Parking Lot' : 'Create New Parking Lot' }}
            </h5>
            <button @click="closeModal" class="btn-close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveLot" class="enhanced-form">
              <div class="form-section">
                <h6 class="form-section-title">
                  <i class="bi bi-info-circle me-2"></i>Basic Information
                </h6>
                <div class="row g-3">
                  <div class="col-md-6">
                    <label class="form-label">Parking Lot Name</label>
                    <input
                      v-model="lotForm.name"
                      type="text"
                      class="form-control enhanced-input"
                      required
                      placeholder="e.g., Downtown Plaza Parking"
                    />
                  </div>
                  
                  <div class="col-md-6">
                    <label class="form-label">Location/District</label>
                    <input
                      v-model="lotForm.location"
                      type="text"
                      class="form-control enhanced-input"
                      required
                      placeholder="e.g., City Center"
                    />
                  </div>
                  
                  <div class="col-12">
                    <label class="form-label">Full Address</label>
                    <textarea
                      v-model="lotForm.address"
                      class="form-control enhanced-input"
                      rows="3"
                      required
                      placeholder="Enter complete address with landmarks"
                    ></textarea>
                  </div>
                </div>
              </div>
              
              <div class="form-section">
                <h6 class="form-section-title">
                  <i class="bi bi-grid-3x3-gap me-2"></i>Capacity & Pricing
                </h6>
                <div class="row g-3">
                  <div class="col-md-6">
                    <label class="form-label">Total Parking Spots</label>
                    <input
                      v-model.number="lotForm.total_spots"
                      type="number"
                      class="form-control enhanced-input"
                      min="1"
                      max="1000"
                      required
                    />
                    <small class="form-text">Recommended: 10-500 spots</small>
                  </div>
                  
                  <div class="col-md-6">
                    <label class="form-label">Hourly Rate (USD)</label>
                    <div class="input-group">
                      <span class="input-group-text">$</span>
                      <input
                        v-model.number="lotForm.price_per_hour"
                        type="number"
                        class="form-control enhanced-input"
                        min="0"
                        step="0.25"
                        required
                      />
                    </div>
                    <small class="form-text">Market rate: $2-15/hour</small>
                  </div>
                </div>
              </div>
              
              <div class="form-actions">
                <button type="submit" class="btn btn-primary btn-lg" :disabled="saving">
                  <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="bi bi-check-circle me-2"></i>
                  {{ saving ? 'Saving...' : (editingLot ? 'Update Parking Lot' : 'Create Parking Lot') }}
                </button>
                <button
                  type="button"
                  @click="closeModal"
                  class="btn btn-outline-secondary btn-lg"
                >
                  <i class="bi bi-x-circle me-2"></i>Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Enhanced Parking Grid Modal -->
    <div v-if="selectedLot" class="modal fade show d-block" style="background: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content enhanced-modal">
          <div class="modal-header enhanced-modal-header">
            <h5 class="modal-title">
              <i class="bi bi-grid-3x3-gap me-2"></i>{{ selectedLot.name }} - Parking Grid Management
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
const sortBy = ref('name')
const showAddModal = ref(false)
const editingLot = ref<ParkingLot | null>(null)
const selectedLot = ref<ParkingLot | null>(null)
const saving = ref(false)

const lotForm = reactive({
  name: '',
  location: '',
  address: '',
  total_spots: 20,
  price_per_hour: 5
})

const filteredLots = computed(() => {
  let filtered = [...parkingStore.parkingLots]

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

  // Sort
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'name':
        return a.name.localeCompare(b.name)
      case 'occupancy':
        return getOccupancyPercentage(b) - getOccupancyPercentage(a)
      case 'price':
        return b.price_per_hour - a.price_per_hour
      case 'newest':
        return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      default:
        return 0
    }
  })

  return filtered
})

// Quick stats
const totalLots = computed(() => parkingStore.parkingLots.length)
const totalSpots = computed(() => parkingStore.parkingLots.reduce((sum, lot) => sum + lot.total_spots, 0))
const occupiedSpots = computed(() => parkingStore.parkingLots.reduce((sum, lot) => sum + (lot.total_spots - lot.available_spots), 0))
const averageOccupancy = computed(() => {
  if (totalSpots.value === 0) return 0
  return Math.round((occupiedSpots.value / totalSpots.value) * 100)
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
  if (confirm('Are you sure you want to delete this parking lot? This action cannot be undone and will remove all associated bookings.')) {
    const success = await parkingStore.deleteParkingLot(id)
    if (success) {
      // Show success notification
      showNotification('Parking lot deleted successfully!', 'success')
    } else {
      showNotification('Failed to delete parking lot', 'error')
    }
  }
}

const viewSpots = (lot: ParkingLot) => {
  selectedLot.value = lot
}

const viewAnalytics = (_lot: ParkingLot) => {
  // Future feature: Individual lot analytics
  showNotification(`Analytics for ${_lot.name} - Coming soon!`, 'info')
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
      showNotification(
        `Parking lot ${editingLot.value ? 'updated' : 'created'} successfully!`, 
        'success'
      )
    } else {
      showNotification(
        `Failed to ${editingLot.value ? 'update' : 'create'} parking lot`, 
        'error'
      )
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
    total_spots: 20,
    price_per_hour: 5
  })
}

const getOccupancyPercentage = (lot: ParkingLot) => {
  return Math.round(((lot.total_spots - lot.available_spots) / lot.total_spots) * 100)
}

const getOccupancyColor = (lot: ParkingLot) => {
  const percentage = getOccupancyPercentage(lot)
  if (percentage < 50) return 'occupancy-low'
  if (percentage < 80) return 'occupancy-medium'
  return 'occupancy-high'
}

const getOccupancyColorClass = (lot: ParkingLot) => {
  const percentage = getOccupancyPercentage(lot)
  if (percentage < 50) return 'text-success'
  if (percentage < 80) return 'text-warning'
  return 'text-danger'
}

const getStatusIndicatorClass = (lot: ParkingLot) => {
  if (lot.available_spots === 0) return 'status-full'
  if (lot.available_spots <= lot.total_spots * 0.2) return 'status-almost-full'
  return 'status-available'
}

const getStatusIcon = (lot: ParkingLot) => {
  if (lot.available_spots === 0) return 'bi bi-x-circle-fill'
  if (lot.available_spots <= lot.total_spots * 0.2) return 'bi bi-exclamation-triangle-fill'
  return 'bi bi-check-circle-fill'
}

const showNotification = (message: string, _notificationType: 'success' | 'error' | 'info') => {
  // Enhanced notification system
  alert(message) // Temporary - will be replaced with toast notifications
}
</script>

<style scoped>
/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  padding: 2rem;
  color: white;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
  opacity: 0.3;
}

.hero-content {
  position: relative;
  z-index: 2;
}

.hero-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.hero-subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 0;
}

.hero-cta {
  background: rgba(255,255,255,0.2) !important;
  border: 2px solid rgba(255,255,255,0.3) !important;
  color: white !important;
  backdrop-filter: blur(10px);
  font-weight: 600;
  padding: 0.75rem 2rem;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.hero-cta:hover {
  background: rgba(255,255,255,0.3) !important;
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.2);
}

/* Search and Filter Section */
.search-filter-section {
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid rgba(255,255,255,0.2);
}

.search-wrapper {
  position: relative;
}

.search-input-group {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.search-icon {
  background: white;
  border: none;
  color: #667eea;
  font-size: 1.1rem;
}

.search-input {
  border: none;
  background: white;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  color: #2d3748;
}

.search-input:focus {
  box-shadow: none;
  border: none;
  background: white;
}

.clear-search {
  border: none;
  background: white;
  color: #6c757d;
}

.filter-select {
  border-radius: 12px;
  border: 2px solid rgba(255,255,255,0.3);
  background: rgba(255,255,255,0.9);
  color: #2d3748;
  font-weight: 500;
  padding: 0.75rem 1rem;
}

.refresh-btn {
  border: 2px solid rgba(255,255,255,0.3);
  color: white;
  background: rgba(255,255,255,0.1);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  font-weight: 600;
  padding: 0.75rem 1rem;
}

.refresh-btn:hover {
  background: rgba(255,255,255,0.2);
  border-color: rgba(255,255,255,0.5);
  color: white;
}

/* Quick Stats */
.quick-stats {
  margin-top: 1.5rem;
}

.stat-card {
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid rgba(255,255,255,0.2);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
}

.stat-card:hover {
  background: rgba(255,255,255,0.25);
  transform: translateY(-2px);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-number {
  font-size: 1.8rem;
  font-weight: 800;
  color: white;
  line-height: 1;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
  color: white;
}

/* Parking Lot Cards */
.lots-grid-section {
  margin-top: 2rem;
}

.parking-lot-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
  overflow: hidden;
  position: relative;
}

.parking-lot-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

.card-header-custom {
  padding: 1.5rem 1.5rem 0;
}

.lot-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 0.25rem;
}

.lot-location {
  color: #667eea;
  font-weight: 500;
  margin-bottom: 0;
  font-size: 0.9rem;
}

.card-body-custom {
  padding: 1rem 1.5rem 1.5rem;
}

.lot-address {
  color: #6c757d;
  font-size: 0.85rem;
  line-height: 1.4;
}

.pricing-info {
  text-align: center;
  padding: 1rem;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  margin-bottom: 1rem;
}

.price-tag {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
}

.price {
  font-size: 1.5rem;
  font-weight: 800;
  color: #667eea;
}

.period {
  color: #6c757d;
  font-weight: 500;
}

.occupancy-section {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1rem;
}

.occupancy-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.occupancy-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #495057;
}

.occupancy-percentage {
  font-size: 0.9rem;
  font-weight: 700;
}

.occupancy-bar {
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.occupancy-fill {
  height: 100%;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.occupancy-low {
  background: linear-gradient(90deg, #28a745, #20c997);
}

.occupancy-medium {
  background: linear-gradient(90deg, #ffc107, #fd7e14);
}

.occupancy-high {
  background: linear-gradient(90deg, #dc3545, #e83e8c);
}

.spots-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.spots-stat {
  text-align: center;
}

.spots-number {
  font-size: 1.2rem;
  font-weight: 700;
  color: #2d3748;
  display: block;
}

.spots-label {
  font-size: 0.75rem;
  color: #6c757d;
  font-weight: 500;
}

.spots-divider {
  color: #dee2e6;
  font-weight: 300;
  font-size: 1.2rem;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
  margin-top: 1rem;
}

.btn-action {
  flex: 1;
  padding: 0.75rem;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.btn-action:hover {
  transform: translateY(-1px);
}

/* Status Indicators */
.status-indicator {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
}

.status-available {
  background: #28a745;
  color: white;
}

.status-almost-full {
  background: #ffc107;
  color: #212529;
}

.status-full {
  background: #dc3545;
  color: white;
}

/* Enhanced Modal */
.enhanced-modal {
  border-radius: 20px;
  border: none;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.enhanced-modal-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 20px 20px 0 0;
  padding: 1.5rem 2rem;
  border: none;
}

.enhanced-modal-header .modal-title {
  font-weight: 700;
  font-size: 1.3rem;
}

.enhanced-modal-header .btn-close {
  filter: invert(1);
  opacity: 0.8;
}

.enhanced-form {
  padding: 1rem;
}

.form-section {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.form-section-title {
  color: #495057;
  font-weight: 600;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #dee2e6;
}

.enhanced-input {
  border: 2px solid #e9ecef;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.enhanced-input:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25);
}

.form-text {
  color: #6c757d;
  font-size: 0.8rem;
  margin-top: 0.25rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  padding-top: 1rem;
  border-top: 1px solid #dee2e6;
}

.form-actions .btn {
  min-width: 150px;
  border-radius: 10px;
  font-weight: 600;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-state-content {
  max-width: 400px;
  margin: 0 auto;
}

.empty-state-icon {
  font-size: 4rem;
  color: #dee2e6;
  margin-bottom: 1.5rem;
}

.empty-state-title {
  color: #495057;
  font-weight: 600;
  margin-bottom: 1rem;
}

.empty-state-text {
  color: #6c757d;
  margin-bottom: 2rem;
  line-height: 1.6;
}

/* Responsive Design */
@media (max-width: 768px) {
  .hero-title {
    font-size: 2rem;
  }
  
  .hero-subtitle {
    font-size: 1rem;
  }
  
  .search-filter-section {
    padding: 1rem;
  }
  
  .stat-card {
    padding: 1rem;
  }
  
  .stat-number {
    font-size: 1.5rem;
  }
  
  .parking-lot-card {
    margin-bottom: 1rem;
  }
  
  .action-buttons {
    flex-direction: column;
  }
  
  .form-actions {
    flex-direction: column;
  }
}

@media (max-width: 576px) {
  .hero-section {
    padding: 1.5rem;
  }
  
  .quick-stats .row {
    gap: 0.5rem;
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
    gap: 0.5rem;
  }
  
  .enhanced-form {
    padding: 0.5rem;
  }
  
  .form-section {
    padding: 1rem;
  }
}
</style>