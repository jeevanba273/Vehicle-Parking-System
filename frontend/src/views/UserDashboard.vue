<template>
  <div class="min-vh-100 bg-light">
    <!-- Navigation Header -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-success shadow-lg">
      <div class="container-fluid">
        <div class="d-flex align-items-center">
          <i class="bi bi-car-front text-warning me-2 fs-3"></i>
          <span class="navbar-brand fw-bold mb-0">User Dashboard</span>
        </div>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
          <div class="navbar-nav me-auto ms-4">
            <router-link
              to="/user/book-spot"
              class="nav-link fw-medium"
              :class="{ 'active': $route.name === 'BookSpot' }"
            >
              <i class="bi bi-plus-circle me-2"></i>Book Spot
            </router-link>
            <router-link
              to="/user/history"
              class="nav-link fw-medium"
              :class="{ 'active': $route.name === 'BookingHistory' }"
            >
              <i class="bi bi-clock-history me-2"></i>Booking History
            </router-link>
          </div>
          
          <div class="navbar-nav">
            <div class="nav-item dropdown">
              <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                <i class="bi bi-person-circle me-2"></i>{{ authStore.currentUser?.fullname }}
              </a>
              <ul class="dropdown-menu dropdown-menu-end">
                <li><a class="dropdown-item" href="#"><i class="bi bi-person me-2"></i>Profile</a></li>
                <li><a class="dropdown-item" href="#"><i class="bi bi-gear me-2"></i>Settings</a></li>
                <li><hr class="dropdown-divider"></li>
                <li><a class="dropdown-item text-danger" @click="logout" href="#"><i class="bi bi-box-arrow-right me-2"></i>Logout</a></li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Content Area -->
    <main class="container-fluid p-4">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useParkingStore } from '../stores/parking'
import { onMounted } from 'vue'

const router = useRouter()
const authStore = useAuthStore()
const parkingStore = useParkingStore()

onMounted(() => {
  parkingStore.fetchParkingLots()
})

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.nav-link {
  transition: all 0.3s ease;
  border-radius: 8px;
  margin: 0 4px;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  transform: translateY(-1px);
}

.nav-link.active {
  background-color: rgba(255, 255, 255, 0.2);
  font-weight: 600;
}

.navbar {
  backdrop-filter: blur(10px);
}
</style>