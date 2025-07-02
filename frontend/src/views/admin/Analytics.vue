<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col-12">
        <div class="d-flex justify-content-between align-items-center mb-4">
          <h2 class="fw-bold text-dark">Analytics Dashboard</h2>
          <button @click="loadAnalytics" class="btn btn-outline-primary">
            <i class="bi bi-arrow-clockwise me-2"></i>Refresh
          </button>
        </div>

        <!-- Timezone Info -->
        <div class="alert alert-info mb-4">
          <i class="bi bi-clock me-2"></i>
          All data and timestamps are displayed in Indian Standard Time (IST)
          <span v-if="analytics.last_updated" class="ms-3">
            Last updated: {{ formatDateTime(analytics.last_updated) }}
          </span>
        </div>

        <!-- Key Metrics -->
        <div class="row g-4 mb-4">
          <div class="col-lg-3 col-md-6">
            <div class="card bg-primary text-white">
              <div class="card-body text-center">
                <i class="bi bi-building display-4 mb-2"></i>
                <h3 class="fw-bold">{{ analytics.total_lots || 0 }}</h3>
                <p class="mb-0">Total Parking Lots</p>
              </div>
            </div>
          </div>
          <div class="col-lg-3 col-md-6">
            <div class="card bg-success text-white">
              <div class="card-body text-center">
                <i class="bi bi-grid-3x3-gap display-4 mb-2"></i>
                <h3 class="fw-bold">{{ analytics.total_spots || 0 }}</h3>
                <p class="mb-0">Total Parking Spots</p>
              </div>
            </div>
          </div>
          <div class="col-lg-3 col-md-6">
            <div class="card bg-warning text-white">
              <div class="card-body text-center">
                <i class="bi bi-car-front display-4 mb-2"></i>
                <h3 class="fw-bold">{{ analytics.occupied_spots || 0 }}</h3>
                <p class="mb-0">Occupied Spots</p>
              </div>
            </div>
          </div>
          <div class="col-lg-3 col-md-6">
            <div class="card bg-info text-white">
              <div class="card-body text-center">
                <i class="bi bi-percent display-4 mb-2"></i>
                <h3 class="fw-bold">{{ analytics.occupancy_rate || 0 }}%</h3>
                <p class="mb-0">Occupancy Rate</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Revenue and Bookings -->
        <div class="row g-4 mb-4">
          <div class="col-lg-4">
            <div class="card">
              <div class="card-body text-center">
                <i class="bi bi-currency-rupee text-success display-4 mb-3"></i>
                <h3 class="fw-bold text-success">₹{{ (analytics.total_revenue || 0).toFixed(2) }}</h3>
                <p class="text-muted mb-0">Total Revenue</p>
              </div>
            </div>
          </div>
          <div class="col-lg-4">
            <div class="card">
              <div class="card-body text-center">
                <i class="bi bi-calendar-check text-primary display-4 mb-3"></i>
                <h3 class="fw-bold text-primary">{{ analytics.total_bookings || 0 }}</h3>
                <p class="text-muted mb-0">Total Bookings</p>
              </div>
            </div>
          </div>
          <div class="col-lg-4">
            <div class="card">
              <div class="card-body text-center">
                <i class="bi bi-clock-history text-warning display-4 mb-3"></i>
                <h3 class="fw-bold text-warning">{{ analytics.active_bookings || 0 }}</h3>
                <p class="text-muted mb-0">Active Bookings</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Charts -->
        <div class="row g-4">
          <div class="col-lg-8">
            <div class="card">
              <div class="card-header">
                <h5 class="card-title mb-0">Revenue by Month (₹)</h5>
              </div>
              <div class="card-body">
                <canvas ref="revenueChart" width="400" height="200"></canvas>
              </div>
            </div>
          </div>
          <div class="col-lg-4">
            <div class="card">
              <div class="card-header">
                <h5 class="card-title mb-0">Occupancy Overview</h5>
              </div>
              <div class="card-body">
                <canvas ref="occupancyChart" width="300" height="300"></canvas>
              </div>
            </div>
          </div>
        </div>

        <!-- Recent Activity -->
        <div class="row g-4 mt-4">
          <div class="col-12">
            <div class="card">
              <div class="card-header">
                <h5 class="card-title mb-0">System Status</h5>
              </div>
              <div class="card-body">
                <div class="row g-3">
                  <div class="col-md-3">
                    <div class="d-flex align-items-center">
                      <div class="bg-success rounded-circle me-3" style="width: 12px; height: 12px;"></div>
                      <div>
                        <div class="fw-bold">Database</div>
                        <small class="text-muted">Connected</small>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-3">
                    <div class="d-flex align-items-center">
                      <div class="bg-warning rounded-circle me-3" style="width: 12px; height: 12px;"></div>
                      <div>
                        <div class="fw-bold">Redis Cache</div>
                        <small class="text-muted">Optional</small>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-3">
                    <div class="d-flex align-items-center">
                      <div class="bg-info rounded-circle me-3" style="width: 12px; height: 12px;"></div>
                      <div>
                        <div class="fw-bold">API Server</div>
                        <small class="text-muted">Running</small>
                      </div>
                    </div>
                  </div>
                  <div class="col-md-3">
                    <div class="d-flex align-items-center">
                      <div class="bg-success rounded-circle me-3" style="width: 12px; height: 12px;"></div>
                      <div>
                        <div class="fw-bold">Timezone</div>
                        <small class="text-muted">IST (Asia/Kolkata)</small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import { getApiUrl } from '../../config/api'

Chart.register(...registerables)

const analytics = ref<any>({})
const revenueChart = ref<HTMLCanvasElement>()
const occupancyChart = ref<HTMLCanvasElement>()
const loading = ref(false)

let revenueChartInstance: Chart | null = null
let occupancyChartInstance: Chart | null = null

onMounted(async () => {
  await loadAnalytics()
  await nextTick()
  initCharts()
})

const loadAnalytics = async () => {
  loading.value = true
  try {
    const response = await fetch(getApiUrl('/api/analytics'))
    if (response.ok) {
      analytics.value = await response.json()
    }
  } catch (error) {
    console.error('Error loading analytics:', error)
  } finally {
    loading.value = false
  }
}

const formatDateTime = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleString('en-IN', {
    timeZone: 'Asia/Kolkata',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true
  })
}

const initCharts = () => {
  if (revenueChart.value) {
    initRevenueChart()
  }
  if (occupancyChart.value) {
    initOccupancyChart()
  }
}

const initRevenueChart = () => {
  if (revenueChartInstance) {
    revenueChartInstance.destroy()
  }

  const ctx = revenueChart.value?.getContext('2d')
  if (!ctx) return

  const revenueData = analytics.value.revenue_by_month || []
  
  revenueChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: revenueData.map((item: any) => item.month),
      datasets: [{
        label: 'Revenue (₹)',
        data: revenueData.map((item: any) => item.revenue),
        borderColor: '#0d6efd',
        backgroundColor: 'rgba(13, 110, 253, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            callback: function(value) {
              return '₹' + value
            }
          }
        }
      }
    }
  })
}

const initOccupancyChart = () => {
  if (occupancyChartInstance) {
    occupancyChartInstance.destroy()
  }

  const ctx = occupancyChart.value?.getContext('2d')
  if (!ctx) return

  const totalSpots = analytics.value.total_spots || 0
  const occupiedSpots = analytics.value.occupied_spots || 0
  const availableSpots = totalSpots - occupiedSpots

  occupancyChartInstance = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Occupied', 'Available'],
      datasets: [{
        data: [occupiedSpots, availableSpots],
        backgroundColor: ['#dc3545', '#198754'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  })
}
</script>

<style scoped>
.card {
  transition: all 0.3s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.1);
}
</style>