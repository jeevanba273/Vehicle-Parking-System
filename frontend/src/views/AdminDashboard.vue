<template>
  <div class="min-vh-100 bg-light">
    <!-- Navigation Header -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-lg">
      <div class="container-fluid">
        <div class="d-flex align-items-center">
          <i class="bi bi-shield-check text-warning me-2 fs-3"></i>
          <span class="navbar-brand fw-bold mb-0">Admin Dashboard</span>
        </div>
        
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        
        <div class="collapse navbar-collapse" id="navbarNav">
          <div class="navbar-nav me-auto ms-4">
            <router-link
              to="/admin/parking-lots"
              class="nav-link fw-medium"
              :class="{ 'active': $route.name === 'ParkingLots' }"
            >
              <i class="bi bi-building me-2"></i>Parking Lots
            </router-link>
            <router-link
              to="/admin/users"
              class="nav-link fw-medium"
              :class="{ 'active': $route.name === 'RegisteredUsers' }"
            >
              <i class="bi bi-people me-2"></i>Registered Users
            </router-link>
            <router-link
              to="/admin/analytics"
              class="nav-link fw-medium"
              :class="{ 'active': $route.name === 'Analytics' }"
            >
              <i class="bi bi-graph-up me-2"></i>Analytics
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