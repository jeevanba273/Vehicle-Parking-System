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
                  <i class="bi bi-car-front-fill me-3"></i>
                  Find Your Perfect Parking Spot in Bangalore
                </h1>
                <p class="hero-subtitle">Discover available parking spaces in real-time across Bangalore</p>
              </div>
              <div class="hero-stats">
                <div class="stat-item">
                  <span class="stat-number">{{ totalAvailableSpots }}</span>
                  <span class="stat-label">Available Spots</span>
                </div>
              </div>
            </div>

            <!-- Enhanced Search and Filter Section -->
            <div class="search-filter-section">
              <div class="row g-3 align-items-center">
                <div class="col-md-4">
                  <div class="search-wrapper">
                    <div class="input-group search-input-group">
                      <span class="input-group-text search-icon">
                        <i class="bi bi-search"></i>
                      </span>
                      <input
                        v-model="searchQuery"
                        type="text"
                        class="form-control search-input"
                        placeholder="Search parking lots, locations in Bangalore..."
                      />
                      <button v-if="searchQuery" @click="searchQuery = ''" class="btn btn-outline-secondary clear-search">
                        <i class="bi bi-x"></i>
                      </button>
                    </div>
                  </div>
                </div>
                <div class="col-md-3">
                  <select v-model="priceFilter" class="form-select filter-select">
                    <option value="">All Prices</option>
                    <option value="low">Under ₹30/hour</option>
                    <option value="medium">₹30-₹50/hour</option>
                    <option value="high">Over ₹50/hour</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <select v-model="availabilityFilter" class="form-select filter-select">
                    <option value="">All Lots</option>
                    <option value="available">Available Spots</option>
                    <option value="full">Full Lots</option>
                  </select>
                </div>
                <div class="col-md-2">
                  <button @click="loadParkingLots" class="btn btn-outline-primary w-100 refresh-btn">
                    <i class="bi bi-arrow-clockwise me-2"></i>Refresh
                  </button>
                </div>
              </div>
            </div>

            <!-- Quick Filters -->
            <div class="quick-filters mt-3">
              <div class="filter-chips">
                <button 
                  class="filter-chip" 
                  :class="{ active: priceFilter === 'low' }"
                  @click="priceFilter = priceFilter === 'low' ? '' : 'low'"
                >
                  <i class="bi bi-currency-rupee"></i>
                  Budget Friendly
                </button>
                <button 
                  class="filter-chip" 
                  :class="{ active: availabilityFilter === 'available' }"
                  @click="availabilityFilter = availabilityFilter === 'available' ? '' : 'available'"
                >
                  <i class="bi bi-check-circle"></i>
                  Available Now
                </button>
                <button 
                  class="filter-chip" 
                  :class="{ active: sortBy === 'price' }"
                  @click="sortBy = sortBy === 'price' ? 'name' : 'price'"
                >
                  <i class="bi bi-sort-numeric-down"></i>
                  Best Price
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Enhanced Parking Lots Grid -->
        <div class="lots-grid-section">
          <div class="section-header mb-4">
            <h3 class="section-title">Available Parking Lots in Bangalore</h3>
            <p class="section-subtitle">{{ filteredLots.length }} locations found</p>
          </div>

          <div class="row g-4">
            <div
              v-for="lot in filteredLots"
              :key="lot.id"
              class="col-xl-4 col-lg-6"
            >
              <div class="parking-lot-card">
                <div class="card-header-custom">
                  <div class="lot-badge" :class="getAvailabilityBadgeClass(lot)">
                    <i :class="getAvailabilityIcon(lot)"></i>
                    {{ getAvailabilityText(lot) }}
                  </div>
                  <div class="lot-info">
                    <h5 class="lot-title">{{ lot.name }}</h5>
                    <p class="lot-location">
                      <i class="bi bi-geo-alt me-1"></i>{{ lot.location }}
                    </p>
                    <p class="lot-address">{{ lot.address }}</p>
                  </div>
                </div>
                
                <div class="card-body-custom">
                  <div class="pricing-section mb-3">
                    <div class="price-display">
                      <div class="price-main">
                        <span class="currency">₹</span>
                        <span class="amount">{{ lot.price_per_hour.toFixed(0) }}</span>
                        <span class="period">/hour</span>
                      </div>
                      <div class="price-rating">
                        <span class="rating-stars">
                          <i v-for="n in getPriceRating(lot)" :key="n" class="bi bi-star-fill"></i>
                          <i v-for="n in (5 - getPriceRating(lot))" :key="n" class="bi bi-star"></i>
                        </span>
                        <small class="rating-text">{{ getPriceRatingText(lot) }}</small>
                      </div>
                    </div>
                  </div>
                  
                  <div class="availability-section mb-3">
                    <div class="availability-header">
                      <span class="availability-label">Availability</span>
                      <span class="availability-count">
                        <strong>{{ lot.available_spots }}</strong> of {{ lot.total_spots }} spots
                      </span>
                    </div>
                    
                    <div class="availability-bar mb-2">
                      <div
                        class="availability-fill"
                        :class="getOccupancyColor(lot)"
                        :style="{ width: getAvailabilityPercentage(lot) + '%' }"
                      ></div>
                    </div>
                    
                    <div class="availability-percentage">
                      <span :class="getAvailabilityPercentageClass(lot)">
                        {{ getAvailabilityPercentage(lot) }}% Available
                      </span>
                    </div>
                  </div>
                  
                  <div class="features-section mb-3">
                    <div class="feature-tags">
                      <span class="feature-tag" v-if="lot.price_per_hour <= 30">
                        <i class="bi bi-currency-rupee"></i>
                        Budget
                      </span>
                      <span class="feature-tag" v-if="lot.available_spots > lot.total_spots * 0.5">
                        <i class="bi bi-check-circle"></i>
                        High Availability
                      </span>
                      <span class="feature-tag" v-if="lot.total_spots >= 100">
                        <i class="bi bi-building"></i>
                        Large Lot
                      </span>
                      <span class="feature-tag" v-if="lot.location.includes('Metro')">
                        <i class="bi bi-train-front"></i>
                        Metro Access
                      </span>
                    </div>
                  </div>
                  
                  <div class="action-section">
                    <button
                      @click="viewParkingGrid(lot)"
                      class="btn btn-primary btn-book"
                      :disabled="lot.available_spots === 0"
                    >
                      <i class="bi bi-grid-3x3-gap me-2"></i>
                      {{ lot.available_spots > 0 ? 'View & Book Spots' : 'Fully Occupied' }}
                    </button>
                    
                    <div class="quick-info mt-2">
                      <small class="text-muted">
                        <i class="bi bi-clock me-1"></i>
                        Instant booking • Real-time updates • IST timezone
                      </small>
                    </div>
                  </div>
                </div>
                
                <!-- Floating Status Indicator -->
                <div class="status-indicator" :class="getStatusIndicatorClass(lot)">
                  <i :class="getStatusIcon(lot)"></i>
                </div>
              </div>
            </div>
          </div>

          <!-- Enhanced Empty State -->
          <div v-if="filteredLots.length === 0" class="empty-state">
            <div class="empty-state-content">
              <div class="empty-state-animation">
                <i class="bi bi-search"></i>
              </div>
              <h4 class="empty-state-title">No parking lots found in Bangalore</h4>
              <p class="empty-state-text">
                {{ parkingLots.length === 0 
                  ? 'No parking lots are currently available in Bangalore' 
                  : 'Try adjusting your search criteria or filters to find more options' }}
              </p>
              <div class="empty-state-actions">
                <button @click="clearFilters" class="btn btn-outline-primary">
                  <i class="bi bi-arrow-clockwise me-2"></i>Clear Filters
                </button>
                <button @click="loadParkingLots" class="btn btn-primary">
                  <i class="bi bi-arrow-clockwise me-2"></i>Refresh Results
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Enhanced Parking Grid Modal -->
    <div v-if="selectedLot" class="modal fade show d-block" style="background: rgba(0,0,0,0.5);">
      <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content enhanced-modal">
          <div class="modal-header enhanced-modal-header">
            <div class="modal-title-section">
              <h5 class="modal-title">
                <i class="bi bi-grid-3x3-gap me-2"></i>{{ selectedLot.name }}
              </h5>
              <p class="modal-subtitle">Select your preferred parking spot • All times in IST</p>
            </div>
            <button @click="selectedLot = null" class="btn-close btn-close-white"></button>
          </div>
          <div class="modal-body enhanced-modal-body">
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
const sortBy = ref('name')
const loading = ref(false)

const totalAvailableSpots = computed(() => 
  parkingLots.value.reduce((sum, lot) => sum + lot.available_spots, 0)
)

const filteredLots = computed(() => {
  let filtered = [...parkingLots.value]

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(lot =>
      lot.name.toLowerCase().includes(query) ||
      lot.location.toLowerCase().includes(query) ||
      lot.address.toLowerCase().includes(query)
    )
  }

  // Price filter - Updated for Indian pricing
  if (priceFilter.value) {
    filtered = filtered.filter(lot => {
      switch (priceFilter.value) {
        case 'low': return lot.price_per_hour < 30
        case 'medium': return lot.price_per_hour >= 30 && lot.price_per_hour <= 50
        case 'high': return lot.price_per_hour > 50
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

  // Sort
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'price':
        return a.price_per_hour - b.price_per_hour
      case 'availability':
        return b.available_spots - a.available_spots
      case 'name':
      default:
        return a.name.localeCompare(b.name)
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

const clearFilters = () => {
  searchQuery.value = ''
  priceFilter.value = ''
  availabilityFilter.value = ''
  sortBy.value = 'name'
}

const getAvailabilityPercentage = (lot: ParkingLot) => {
  return Math.round((lot.available_spots / lot.total_spots) * 100)
}

const getOccupancyColor = (lot: ParkingLot) => {
  const percentage = getAvailabilityPercentage(lot)
  if (percentage >= 50) return 'availability-high'
  if (percentage >= 20) return 'availability-medium'
  return 'availability-low'
}

const getAvailabilityBadgeClass = (lot: ParkingLot) => {
  if (lot.available_spots === 0) return 'badge-full'
  if (lot.available_spots <= lot.total_spots * 0.2) return 'badge-limited'
  return 'badge-available'
}

const getAvailabilityIcon = (lot: ParkingLot) => {
  if (lot.available_spots === 0) return 'bi bi-x-circle-fill'
  if (lot.available_spots <= lot.total_spots * 0.2) return 'bi bi-exclamation-triangle-fill'
  return 'bi bi-check-circle-fill'
}

const getAvailabilityText = (lot: ParkingLot) => {
  if (lot.available_spots === 0) return 'Full'
  if (lot.available_spots <= lot.total_spots * 0.2) return 'Limited'
  return 'Available'
}

const getAvailabilityPercentageClass = (lot: ParkingLot) => {
  const percentage = getAvailabilityPercentage(lot)
  if (percentage >= 50) return 'text-success'
  if (percentage >= 20) return 'text-warning'
  return 'text-danger'
}

const getStatusIndicatorClass = (lot: ParkingLot) => {
  if (lot.available_spots === 0) return 'status-full'
  if (lot.available_spots <= lot.total_spots * 0.2) return 'status-limited'
  return 'status-available'
}

const getStatusIcon = (lot: ParkingLot) => {
  if (lot.available_spots === 0) return 'bi bi-x-circle-fill'
  if (lot.available_spots <= lot.total_spots * 0.2) return 'bi bi-exclamation-triangle-fill'
  return 'bi bi-check-circle-fill'
}

// Updated price rating for Indian pricing
const getPriceRating = (lot: ParkingLot) => {
  if (lot.price_per_hour <= 20) return 5  // Very affordable
  if (lot.price_per_hour <= 30) return 4  // Affordable
  if (lot.price_per_hour <= 40) return 3  // Moderate
  if (lot.price_per_hour <= 55) return 2  // Expensive
  return 1  // Very expensive
}

const getPriceRatingText = (lot: ParkingLot) => {
  const rating = getPriceRating(lot)
  if (rating >= 4) return 'Great Value'
  if (rating >= 3) return 'Good Value'
  if (rating >= 2) return 'Fair Price'
  return 'Premium'
}
</script>

<style scoped>
/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
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

.hero-stats {
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid rgba(255,255,255,0.2);
  text-align: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-number {
  font-size: 2rem;
  font-weight: 800;
  color: white;
  line-height: 1;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
  color: white;
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
  color: #28a745;
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

/* Quick Filters */
.quick-filters {
  margin-top: 1rem;
}

.filter-chips {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  justify-content: center;
}

.filter-chip {
  background: rgba(255,255,255,0.1);
  border: 2px solid rgba(255,255,255,0.3);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 25px;
  font-size: 0.9rem;
  font-weight: 500;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.filter-chip:hover {
  background: rgba(255,255,255,0.2);
  border-color: rgba(255,255,255,0.5);
  transform: translateY(-2px);
}

.filter-chip.active {
  background: rgba(255,255,255,0.3);
  border-color: rgba(255,255,255,0.6);
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

/* Section Header */
.section-header {
  text-align: center;
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.section-subtitle {
  color: #6c757d;
  font-size: 1.1rem;
  margin-bottom: 0;
}

/* Parking Lot Cards */
.parking-lot-card {
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
  overflow: hidden;
  position: relative;
  height: 100%;
}

.parking-lot-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.15);
}

.card-header-custom {
  padding: 1.5rem;
  position: relative;
}

.lot-badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-available {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
}

.badge-limited {
  background: linear-gradient(135deg, #ffc107, #fd7e14);
  color: #212529;
}

.badge-full {
  background: linear-gradient(135deg, #dc3545, #c82333);
  color: white;
}

.lot-info {
  margin-top: 2rem;
}

.lot-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 0.5rem;
}

.lot-location {
  color: #28a745;
  font-weight: 600;
  margin-bottom: 0.25rem;
  font-size: 1rem;
}

.lot-address {
  color: #6c757d;
  font-size: 0.9rem;
  margin-bottom: 0;
  line-height: 1.4;
}

.card-body-custom {
  padding: 0 1.5rem 1.5rem;
}

/* Pricing Section */
.pricing-section {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
}

.price-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.price-main {
  display: flex;
  align-items: baseline;
  gap: 0.25rem;
}

.currency {
  font-size: 1.2rem;
  font-weight: 600;
  color: #28a745;
}

.amount {
  font-size: 2rem;
  font-weight: 800;
  color: #28a745;
}

.period {
  font-size: 1rem;
  color: #6c757d;
  font-weight: 500;
}

.price-rating {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.25rem;
}

.rating-stars {
  color: #ffc107;
  font-size: 0.9rem;
}

.rating-text {
  color: #6c757d;
  font-weight: 500;
}

/* Availability Section */
.availability-section {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 1rem;
}

.availability-header {
  display: flex;
  justify-content: between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.availability-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #495057;
}

.availability-count {
  font-size: 0.9rem;
  color: #6c757d;
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

.availability-high {
  background: linear-gradient(90deg, #28a745, #20c997);
}

.availability-medium {
  background: linear-gradient(90deg, #ffc107, #fd7e14);
}

.availability-low {
  background: linear-gradient(90deg, #dc3545, #e83e8c);
}

.availability-percentage {
  text-align: center;
  font-size: 0.9rem;
  font-weight: 600;
}

/* Features Section */
.features-section {
  margin-bottom: 1rem;
}

.feature-tags {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.feature-tag {
  background: linear-gradient(135deg, #e3f2fd, #bbdefb);
  color: #1976d2;
  padding: 0.25rem 0.75rem;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

/* Action Section */
.action-section {
  text-align: center;
}

.btn-book {
  background: linear-gradient(135deg, #28a745, #20c997);
  border: none;
  color: white;
  font-weight: 600;
  padding: 0.75rem 2rem;
  border-radius: 12px;
  transition: all 0.3s ease;
  width: 100%;
}

.btn-book:hover:not(:disabled) {
  background: linear-gradient(135deg, #218838, #1e7e34);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(40, 167, 69, 0.4);
}

.btn-book:disabled {
  background: #6c757d;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.quick-info {
  text-align: center;
}

/* Status Indicators */
.status-indicator {
  position: absolute;
  top: 1rem;
  left: 1rem;
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

.status-limited {
  background: #ffc107;
  color: #212529;
}

.status-full {
  background: #dc3545;
  color: white;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
}

.empty-state-content {
  max-width: 500px;
  margin: 0 auto;
}

.empty-state-animation {
  font-size: 5rem;
  color: #dee2e6;
  margin-bottom: 2rem;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.empty-state-title {
  color: #495057;
  font-weight: 600;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.empty-state-text {
  color: #6c757d;
  margin-bottom: 2rem;
  line-height: 1.6;
  font-size: 1.1rem;
}

.empty-state-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

/* Enhanced Modal */
.enhanced-modal {
  border-radius: 20px;
  border: none;
  box-shadow: 0 25px 50px rgba(0,0,0,0.3);
}

.enhanced-modal-header {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
  border-radius: 20px 20px 0 0;
  padding: 2rem;
  border: none;
}

.modal-title-section {
  flex: 1;
}

.modal-title {
  font-weight: 700;
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.modal-subtitle {
  opacity: 0.9;
  margin-bottom: 0;
  font-size: 1rem;
}

.btn-close-white {
  filter: invert(1);
  opacity: 0.8;
}

.enhanced-modal-body {
  padding: 2rem;
  background: #f8f9fa;
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
  
  .filter-chips {
    justify-content: flex-start;
  }
  
  .parking-lot-card {
    margin-bottom: 1rem;
  }
  
  .empty-state-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .empty-state-actions .btn {
    width: 200px;
  }
}

@media (max-width: 576px) {
  .hero-section {
    padding: 1.5rem;
  }
  
  .hero-stats {
    margin-top: 1rem;
  }
  
  .section-title {
    font-size: 1.5rem;
  }
  
  .lot-badge {
    position: static;
    margin-bottom: 1rem;
    align-self: flex-start;
  }
  
  .lot-info {
    margin-top: 0;
  }
  
  .price-main {
    flex-direction: column;
    align-items: center;
  }
  
  .enhanced-modal-header {
    padding: 1.5rem;
  }
  
  .enhanced-modal-body {
    padding: 1rem;
  }
}
</style>