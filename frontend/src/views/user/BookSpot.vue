<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12">
        <!-- Enhanced Header -->
        <div class="page-header mb-4">
          <div class="row align-items-center">
            <div class="col-md-8">
              <h2 class="fw-bold text-dark mb-2">
                <i class="bi bi-geo-alt-fill me-2 text-primary"></i>Find & Book Parking
              </h2>
              <p class="text-muted mb-0">Discover available parking spots near you</p>
            </div>
            <div class="col-md-4 text-md-end">
              <div class="live-indicator">
                <div class="pulse-dot"></div>
                <span>Live Availability</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Enhanced Search & Filter Bar -->
        <div class="search-filter-bar mb-4">
          <div class="row g-3">
            <div class="col-md-4">
              <div class="search-container">
                <i class="bi bi-search search-icon"></i>
                <input
                  v-model="searchQuery"
                  type="text"
                  class="form-control search-input"
                  placeholder="Search by location, name..."
                />
                <button v-if="searchQuery" @click="searchQuery = ''" class="clear-search">
                  <i class="bi bi-x"></i>
                </button>
              </div>
            </div>
            <div class="col-md-2">
              <select v-model="priceFilter" class="form-select filter-select">
                <option value="">All Prices</option>
                <option value="budget">Budget (Under $5)</option>
                <option value="standard">Standard ($5-$10)</option>
                <option value="premium">Premium ($10+)</option>
              </select>
            </div>
            <div class="col-md-2">
              <select v-model="availabilityFilter" class="form-select filter-select">
                <option value="">All Lots</option>
                <option value="available">Available Now</option>
                <option value="limited">Limited Spots</option>
                <option value="full">Full Lots</option>
              </select>
            </div>
            <div class="col-md-2">
              <select v-model="sortBy" class="form-select filter-select">
                <option value="distance">Nearest First</option>
                <option value="price-low">Lowest Price</option>
                <option value="price-high">Highest Price</option>
                <option value="availability">Most Available</option>
                <option value="rating">Highest Rated</option>
              </select>
            </div>
            <div class="col-md-2">
              <button @click="loadParkingLots" class="btn btn-outline-primary w-100 refresh-btn">
                <i class="bi bi-arrow-clockwise me-1"></i>Refresh
              </button>
            </div>
          </div>
        </div>

        <!-- Quick Stats -->
        <div class="quick-stats mb-4">
          <div class="row g-3">
            <div class="col-md-3">
              <div class="stat-card">
                <div class="stat-icon bg-primary">
                  <i class="bi bi-building"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ filteredLots.length }}</div>
                  <div class="stat-label">Available Lots</div>
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="stat-card">
                <div class="stat-icon bg-success">
                  <i class="bi bi-car-front"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ totalAvailableSpots }}</div>
                  <div class="stat-label">Open Spots</div>
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="stat-card">
                <div class="stat-icon bg-info">
                  <i class="bi bi-currency-dollar"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">${{ averagePrice }}</div>
                  <div class="stat-label">Avg. Price/Hour</div>
                </div>
              </div>
            </div>
            <div class="col-md-3">
              <div class="stat-card">
                <div class="stat-icon bg-warning">
                  <i class="bi bi-clock"></i>
                </div>
                <div class="stat-content">
                  <div class="stat-number">{{ Math.round(averageDistance) }}m</div>
                  <div class="stat-label">Avg. Distance</div>
                </div>
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
            :class="{ 
              'fully-occupied': lot.available_spots === 0,
              'limited-spots': lot.available_spots > 0 && lot.available_spots <= lot.total_spots * 0.2
            }"
          >
            <!-- Card Header -->
            <div class="card-header">
              <div class="d-flex justify-content-between align-items-start">
                <div class="lot-info">
                  <h5 class="lot-name">{{ lot.name }}</h5>
                  <div class="lot-location">
                    <i class="bi bi-geo-alt me-1"></i>{{ lot.location }}
                  </div>
                  <div class="lot-distance">
                    <i class="bi bi-compass me-1"></i>{{ getRandomDistance() }}m away
                  </div>
                </div>
                <div class="price-badge">
                  <div class="price-amount">${{ lot.price_per_hour }}</div>
                  <div class="price-unit">per hour</div>
                </div>
              </div>
            </div>

            <!-- Card Body -->
            <div class="card-body">
              <div class="lot-address mb-3">
                <i class="bi bi-building me-2 text-muted"></i>
                <span class="text-muted">{{ lot.address }}</span>
              </div>

              <!-- Availability Section -->
              <div class="availability-section mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                  <span class="availability-label">Availability</span>
                  <span class="availability-count">
                    {{ lot.available_spots }}/{{ lot.total_spots }} spots
                  </span>
                </div>
                <div class="availability-bar">
                  <div
                    class="availability-fill"
                    :class="getAvailabilityColor(lot)"
                    :style="{ width: getAvailabilityPercentage(lot) + '%' }"
                  ></div>
                </div>
                <div class="availability-status mt-2">
                  <span class="status-indicator" :class="getStatusClass(lot)"></span>
                  <span class="status-text">{{ getStatusText(lot) }}</span>
                </div>
              </div>

              <!-- Features -->
              <div class="features-section mb-3">
                <div class="feature-tags">
                  <span class="feature-tag">
                    <i class="bi bi-shield-check me-1"></i>Secure
                  </span>
                  <span class="feature-tag">
                    <i class="bi bi-camera me-1"></i>CCTV
                  </span>
                  <span class="feature-tag" v-if="lot.price_per_hour <= 5">
                    <i class="bi bi-tag me-1"></i>Budget
                  </span>
                  <span class="feature-tag" v-if="lot.total_spots >= 100">
                    <i class="bi bi-building me-1"></i>Large
                  </span>
                </div>
              </div>

              <!-- Estimated Cost -->
              <div class="cost-estimate mb-3">
                <div class="cost-grid">
                  <div class="cost-item">
                    <div class="cost-duration">1 Hour</div>
                    <div class="cost-price">${{ lot.price_per_hour.toFixed(2) }}</div>
                  </div>
                  <div class="cost-item">
                    <div class="cost-duration">4 Hours</div>
                    <div class="cost-price">${{ (lot.price_per_hour * 4).toFixed(2) }}</div>
                  </div>
                  <div class="cost-item">
                    <div class="cost-duration">8 Hours</div>
                    <div class="cost-price">${{ (lot.price_per_hour * 8).toFixed(2) }}</div>
                  </div>
                </div>
              </div>

              <!-- Rating -->
              <div class="rating-section mb-3">
                <div class="d-flex align-items-center justify-content-between">
                  <div class="rating-stars">
                    <i class="bi bi-star-fill text-warning" v-for="n in 5" :key="n"></i>
                    <span class="rating-text ms-2">4.8 (124 reviews)</span>
                  </div>
                  <div class="last-updated">
                    <i class="bi bi-clock me-1"></i>
                    <span>Updated {{ getRandomTime() }} ago</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Card Footer -->
            <div class="card-footer">
              <div class="d-flex gap-2">
                <button
                  @click="viewParkingGrid(lot)"
                  class="btn btn-primary flex-fill book-btn"
                  :disabled="lot.available_spots === 0"
                >
                  <i class="bi bi-grid-3x3-gap me-2"></i>
                  {{ lot.available_spots > 0 ? 'Select Spot' : 'Fully Occupied' }}
                </button>
                <button class="btn btn-outline-secondary info-btn" @click="showLotInfo(lot)">
                  <i class="bi bi-info-circle"></i>
                </button>
                <button class="btn btn-outline-success directions-btn" @click="getDirections(lot)">
                  <i class="bi bi-compass"></i>
                </button>
              </div>
            </div>

            <!-- Status Badge -->
            <div class="status-badge" :class="getStatusBadgeClass(lot)">
              {{ getStatusText(lot) }}
            </div>

            <!-- Trending Badge -->
            <div v-if="Math.random() > 0.7" class="trending-badge">
              <i class="bi bi-fire"></i>
              Popular
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="filteredLots.length === 0" class="empty-state">
          <div class="empty-icon">
            <i class="bi bi-search"></i>
          </div>
          <h4>No parking lots found</h4>
          <p>Try adjusting your search criteria or check back later</p>
          <button @click="clearFilters" class="btn btn-outline-primary">Clear Filters</button>
        </div>
      </div>
    </div>

    <!-- Enhanced Parking Grid Modal -->
    <div v-if="selectedLot" class="modal fade show d-block" style="background: rgba(0,0,0,0.7);">
      <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content enhanced-modal">
          <div class="modal-header-enhanced">
            <div class="modal-title-section">
              <div class="modal-icon bg-primary">
                <i class="bi bi-grid-3x3-gap"></i>
              </div>
              <div>
                <h5 class="modal-title">{{ selectedLot.name }}</h5>
                <p class="modal-subtitle">Select your preferred parking spot</p>
              </div>
            </div>
            <button @click="selectedLot = null" class="btn-close-enhanced">
              <i class="bi bi-x"></i>
            </button>
          </div>
          <div class="modal-body-enhanced">
            <ParkingGrid :lot="selectedLot" :show-booking-form="true" />
          </div>
        </div>
      </div>
    </div>

    <!-- Lot Info Modal -->
    <div v-if="infoLot" class="modal fade show d-block" style="background: rgba(0,0,0,0.6);">
      <div class="modal-dialog modal-lg modal-dialog-centered">
        <div class="modal-content enhanced-modal">
          <div class="modal-header-enhanced">
            <div class="modal-title-section">
              <div class="modal-icon bg-info">
                <i class="bi bi-info-circle"></i>
              </div>
              <div>
                <h5 class="modal-title">{{ infoLot.name }}</h5>
                <p class="modal-subtitle">Parking facility information</p>
              </div>
            </div>
            <button @click="infoLot = null" class="btn-close-enhanced">
              <i class="bi bi-x"></i>
            </button>
          </div>
          <div class="modal-body-enhanced">
            <div class="info-grid">
              <div class="info-section">
                <h6><i class="bi bi-geo-alt me-2"></i>Location Details</h6>
                <p><strong>Address:</strong> {{ infoLot.address }}</p>
                <p><strong>District:</strong> {{ infoLot.location }}</p>
                <p><strong>Distance:</strong> {{ getRandomDistance() }}m from your location</p>
              </div>
              <div class="info-section">
                <h6><i class="bi bi-currency-dollar me-2"></i>Pricing Information</h6>
                <p><strong>Hourly Rate:</strong> ${{ infoLot.price_per_hour }}</p>
                <p><strong>Daily Maximum:</strong> ${{ (infoLot.price_per_hour * 12).toFixed(2) }}</p>
                <p><strong>Weekly Rate:</strong> ${{ (infoLot.price_per_hour * 40).toFixed(2) }}</p>
              </div>
              <div class="info-section">
                <h6><i class="bi bi-building me-2"></i>Facility Features</h6>
                <ul class="feature-list">
                  <li><i class="bi bi-shield-check text-success me-2"></i>24/7 Security</li>
                  <li><i class="bi bi-camera text-primary me-2"></i>CCTV Monitoring</li>
                  <li><i class="bi bi-lightbulb text-warning me-2"></i>Well Lit</li>
                  <li><i class="bi bi-telephone text-info me-2"></i>Emergency Contact</li>
                </ul>
              </div>
              <div class="info-section">
                <h6><i class="bi bi-clock me-2"></i>Operating Hours</h6>
                <p><strong>Monday - Friday:</strong> 24 Hours</p>
                <p><strong>Saturday - Sunday:</strong> 24 Hours</p>
                <p><strong>Holidays:</strong> 24 Hours</p>
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
import ParkingGrid from '../../components/ParkingGrid.vue'
import { getApiUrl } from '../../config/api'
import type { ParkingLot } from '../../stores/parking'

const parkingLots = ref<ParkingLot[]>([])
const selectedLot = ref<ParkingLot | null>(null)
const infoLot = ref<ParkingLot | null>(null)
const searchQuery = ref('')
const priceFilter = ref('')
const availabilityFilter = ref('')
const sortBy = ref('distance')
const loading = ref(false)

const totalAvailableSpots = computed(() => 
  filteredLots.value.reduce((sum, lot) => sum + lot.available_spots, 0)
)

const averagePrice = computed(() => {
  if (filteredLots.value.length === 0) return 0
  const total = filteredLots.value.reduce((sum, lot) => sum + lot.price_per_hour, 0)
  return (total / filteredLots.value.length).toFixed(2)
})

const averageDistance = computed(() => {
  return Math.random() * 500 + 100 // Simulated distance
})

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
        case 'budget': return lot.price_per_hour < 5
        case 'standard': return lot.price_per_hour >= 5 && lot.price_per_hour <= 10
        case 'premium': return lot.price_per_hour > 10
        default: return true
      }
    })
  }

  // Availability filter
  if (availabilityFilter.value) {
    filtered = filtered.filter(lot => {
      switch (availabilityFilter.value) {
        case 'available': return lot.available_spots > lot.total_spots * 0.2
        case 'limited': return lot.available_spots > 0 && lot.available_spots <= lot.total_spots * 0.2
        case 'full': return lot.available_spots === 0
        default: return true
      }
    })
  }

  // Sort
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'distance': return Math.random() - 0.5 // Simulated distance sorting
      case 'price-low': return a.price_per_hour - b.price_per_hour
      case 'price-high': return b.price_per_hour - a.price_per_hour
      case 'availability': return b.available_spots - a.available_spots
      case 'rating': return Math.random() - 0.5 // Simulated rating sorting
      default: return 0
    }
  })

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

const showLotInfo = (lot: ParkingLot) => {
  infoLot.value = lot
}

const getDirections = (lot: ParkingLot) => {
  alert(`Getting directions to ${lot.name} - Feature coming soon!`)
}

const clearFilters = () => {
  searchQuery.value = ''
  priceFilter.value = ''
  availabilityFilter.value = ''
  sortBy.value = 'distance'
}

const getAvailabilityPercentage = (lot: ParkingLot) => {
  return (lot.available_spots / lot.total_spots) * 100
}

const getAvailabilityColor = (lot: ParkingLot) => {
  const percentage = getAvailabilityPercentage(lot)
  if (percentage > 50) return 'high'
  if (percentage > 20) return 'medium'
  return 'low'
}

const getStatusClass = (lot: ParkingLot) => {
  if (lot.available_spots === 0) return 'status-full'
  if (lot.available_spots <= lot.total_spots * 0.2) return 'status-limited'
  return 'status-available'
}

const getStatusText = (lot: ParkingLot) => {
  if (lot.available_spots === 0) return 'Full'
  if (lot.available_spots <= lot.total_spots * 0.2) return 'Limited'
  return 'Available'
}

const getStatusBadgeClass = (lot: ParkingLot) => {
  if (lot.available_spots === 0) return 'badge-full'
  if (lot.available_spots <= lot.total_spots * 0.2) return 'badge-limited'
  return 'badge-available'
}

const getRandomDistance = () => {
  return Math.floor(Math.random() * 800) + 50
}

const getRandomTime = () => {
  const times = ['2 min', '5 min', '10 min', '15 min', '30 min']
  return times[Math.floor(Math.random() * times.length)]
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

.live-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #198754;
  font-weight: 600;
  font-size: 0.9rem;
}

.pulse-dot {
  width: 8px;
  height: 8px;
  background: #198754;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.2); opacity: 0.7; }
  100% { transform: scale(1); opacity: 1; }
}

/* Search & Filter Bar */
.search-filter-bar {
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

.refresh-btn {
  border-radius: 12px !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
}

.refresh-btn:hover {
  transform: rotate(180deg) !important;
}

/* Quick Stats */
.quick-stats {
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  border: 1px solid #e9ecef;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.stat-icon {
  width: 50px;
  height: 50px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
}

.stat-number {
  font-size: 1.75rem;
  font-weight: 700;
  color: #2d3748;
}

.stat-label {
  color: #6c757d;
  font-size: 0.9rem;
}

/* Parking Lots Grid */
.parking-lots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
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

.parking-lot-card.limited-spots {
  border-color: #ffc107;
  background: linear-gradient(135deg, #fffbf0 0%, #fff3cd 100%);
}

.card-header {
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
  margin-bottom: 0.25rem;
}

.lot-distance {
  color: #6c757d;
  font-size: 0.8rem;
}

.price-badge {
  background: linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%);
  color: white;
  padding: 0.75rem 1rem;
  border-radius: 12px;
  text-align: center;
  min-width: 80px;
}

.price-amount {
  font-size: 1.25rem;
  font-weight: 700;
}

.price-unit {
  font-size: 0.7rem;
  opacity: 0.9;
}

.card-body {
  padding: 1.5rem;
}

.lot-address {
  font-size: 0.9rem;
  line-height: 1.4;
}

/* Availability Section */
.availability-section {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1rem;
}

.availability-label {
  font-weight: 600;
  color: #2d3748;
  font-size: 0.9rem;
}

.availability-count {
  font-weight: 700;
  color: #0d6efd;
  font-size: 0.9rem;
}

.availability-bar {
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.availability-fill {
  height: 100%;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.availability-fill.high {
  background: linear-gradient(90deg, #198754 0%, #20c997 100%);
}

.availability-fill.medium {
  background: linear-gradient(90deg, #fd7e14 0%, #ffc107 100%);
}

.availability-fill.low {
  background: linear-gradient(90deg, #dc3545 0%, #e74c3c 100%);
}

.availability-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.status-indicator.status-available {
  background: #198754;
}

.status-indicator.status-limited {
  background: #ffc107;
}

.status-indicator.status-full {
  background: #dc3545;
}

.status-text {
  font-size: 0.8rem;
  font-weight: 600;
}

/* Features Section */
.features-section {
  margin-bottom: 1rem;
}

.feature-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.feature-tag {
  background: #e9ecef;
  color: #495057;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
  display: flex;
  align-items: center;
}

/* Cost Estimate */
.cost-estimate {
  background: linear-gradient(135deg, #e8f5e8 0%, #d4edda 100%);
  border-radius: 12px;
  padding: 1rem;
  border: 1px solid #c3e6cb;
}

.cost-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0.5rem;
}

.cost-item {
  text-align: center;
  background: white;
  padding: 0.75rem 0.5rem;
  border-radius: 8px;
  border: 1px solid #c3e6cb;
}

.cost-duration {
  font-size: 0.8rem;
  color: #6c757d;
  margin-bottom: 0.25rem;
}

.cost-price {
  font-size: 1rem;
  font-weight: 700;
  color: #198754;
}

/* Rating Section */
.rating-section {
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 12px;
}

.rating-stars {
  display: flex;
  align-items: center;
}

.rating-text {
  color: #6c757d;
  font-size: 0.9rem;
}

.last-updated {
  color: #6c757d;
  font-size: 0.8rem;
}

/* Card Footer */
.card-footer {
  padding: 1.5rem;
  background: #f8f9fa;
  border-top: 1px solid #e9ecef;
}

.book-btn {
  background: linear-gradient(135deg, #0d6efd 0%, #0b5ed7 100%) !important;
  border: none !important;
  border-radius: 12px !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
}

.book-btn:hover:not(:disabled) {
  transform: translateY(-2px) !important;
  box-shadow: 0 8px 25px rgba(13, 110, 253, 0.3) !important;
}

.info-btn, .directions-btn {
  border-radius: 12px !important;
  font-weight: 600 !important;
  transition: all 0.3s ease !important;
}

.info-btn:hover, .directions-btn:hover {
  transform: translateY(-2px) !important;
}

/* Status Badges */
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
  z-index: 2;
}

.badge-available {
  background: #d4edda;
  color: #155724;
}

.badge-limited {
  background: #fff3cd;
  color: #856404;
}

.badge-full {
  background: #f8d7da;
  color: #721c24;
}

.trending-badge {
  position: absolute;
  top: 1rem;
  left: 1rem;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  z-index: 2;
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

/* Info Modal */
.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.info-section {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #e9ecef;
}

.info-section h6 {
  color: #2d3748;
  font-weight: 600;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
}

.feature-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li {
  padding: 0.5rem 0;
  display: flex;
  align-items: center;
}

/* Responsive Design */
@media (max-width: 768px) {
  .parking-lots-grid {
    grid-template-columns: 1fr;
  }
  
  .cost-grid {
    grid-template-columns: 1fr;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .quick-stats .row {
    gap: 1rem;
  }
  
  .stat-card {
    padding: 1rem;
  }
  
  .page-header {
    padding: 1.5rem;
  }
}
</style>