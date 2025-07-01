<template>
  <div class="min-vh-100 bg-light">
    <!-- Navigation Header -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-lg fixed-navbar">
      <div class="container-fluid">
        <div class="d-flex align-items-center">
          <i class="bi bi-shield-check text-warning me-2 fs-3"></i>
          <span class="navbar-brand fw-bold mb-0">Admin Dashboard</span>
        </div>
        
        <button 
          class="navbar-toggler" 
          type="button" 
          data-bs-toggle="collapse" 
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
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
              <a 
                class="nav-link dropdown-toggle user-dropdown" 
                href="#" 
                role="button" 
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                <i class="bi bi-person-circle me-2"></i>{{ authStore.currentUser?.fullname }}
              </a>
              <ul class="dropdown-menu dropdown-menu-end user-dropdown-menu">
                <li>
                  <h6 class="dropdown-header">
                    <i class="bi bi-person-circle me-2"></i>{{ authStore.currentUser?.fullname }}
                  </h6>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item" href="#">
                    <i class="bi bi-person me-2"></i>Profile
                  </a>
                </li>
                <li>
                  <a class="dropdown-item" href="#">
                    <i class="bi bi-gear me-2"></i>Settings
                  </a>
                </li>
                <li><hr class="dropdown-divider"></li>
                <li>
                  <a class="dropdown-item text-danger logout-item" @click="logout" href="#">
                    <i class="bi bi-box-arrow-right me-2"></i>Logout
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Content Area -->
    <main class="main-content">
      <div class="container-fluid p-4">
        <router-view />
      </div>
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
.fixed-navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1030;
  height: 70px;
}

.main-content {
  margin-top: 70px;
  min-height: calc(100vh - 70px);
}

.nav-link {
  transition: all 0.3s ease;
  border-radius: 8px;
  margin: 0 4px;
  position: relative;
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
  box-shadow: 0 2px 20px rgba(0,0,0,0.1);
}

.user-dropdown {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.user-dropdown:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.user-dropdown-menu {
  border: none;
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
  border-radius: 12px;
  padding: 0.5rem 0;
  min-width: 220px;
  z-index: 1060;
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 0.5rem;
}

.dropdown-header {
  color: #495057;
  font-weight: 600;
  padding: 0.75rem 1rem 0.5rem;
  margin-bottom: 0;
  font-size: 0.9rem;
}

.dropdown-item {
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
  border-radius: 8px;
  margin: 0 0.5rem;
  font-size: 0.9rem;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
  transform: translateX(5px);
}

.logout-item:hover {
  background-color: #fee;
  color: #dc3545 !important;
}

.dropdown-divider {
  margin: 0.5rem 1rem;
  border-color: #e9ecef;
}

/* Ensure dropdown appears above other content */
.dropdown-menu.show {
  display: block;
  z-index: 1060;
}

/* Fix navbar collapse on mobile */
@media (max-width: 991.98px) {
  .navbar-collapse {
    background: rgba(13, 110, 253, 0.95);
    border-radius: 12px;
    margin-top: 1rem;
    padding: 1rem;
    backdrop-filter: blur(10px);
  }
  
  .user-dropdown-menu {
    position: static;
    float: none;
    width: 100%;
    margin-top: 0.5rem;
    box-shadow: none;
    border: 1px solid rgba(255,255,255,0.2);
    background: rgba(255,255,255,0.1);
  }
  
  .dropdown-item {
    color: white;
  }
  
  .dropdown-item:hover {
    background-color: rgba(255,255,255,0.1);
    color: white;
  }
  
  .logout-item:hover {
    background-color: rgba(220, 53, 69, 0.2);
    color: #ff6b6b !important;
  }
}

/* Prevent navbar from growing too large */
.navbar-brand {
  font-size: 1.25rem;
}

.navbar-nav .nav-link {
  font-size: 0.95rem;
}

/* Smooth transitions */
.navbar-collapse {
  transition: all 0.3s ease;
}

.dropdown-menu {
  transition: all 0.3s ease;
}
</style>