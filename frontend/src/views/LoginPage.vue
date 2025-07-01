<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-5">
          <div class="text-center mb-4 fade-in">
            <h1 class="text-white fw-bold mb-2 display-5">Vehicle Parking System</h1>
            <p class="text-white-50 lead">Welcome back! Please sign in to your account.</p>
          </div>
          
          <div class="card glass-effect border-0 shadow-lg slide-in">
            <div class="card-body p-5">
              <h2 class="text-white text-center mb-4 fw-bold">User Login</h2>
              
              <form @submit.prevent="handleLogin">
                <div class="mb-4">
                  <label class="form-label text-white-50 fw-medium">Registered Email ID</label>
                  <input 
                    v-model="email" 
                    type="email" 
                    class="form-control form-control-lg bg-transparent text-white border-light"
                    style="backdrop-filter: blur(10px);"
                    placeholder="Enter your email"
                    required
                  />
                </div>
                
                <div class="mb-4">
                  <label class="form-label text-white-50 fw-medium">Password</label>
                  <input 
                    v-model="password" 
                    type="password" 
                    class="form-control form-control-lg bg-transparent text-white border-light"
                    style="backdrop-filter: blur(10px);"
                    placeholder="Enter your password"
                    required
                  />
                </div>
                
                <button 
                  type="submit" 
                  class="btn btn-primary btn-lg w-100 btn-hover fw-bold"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ loading ? 'Signing in...' : 'Login' }}
                </button>
                
                <div v-if="error" class="alert alert-danger mt-3 glass-effect">
                  <i class="bi bi-exclamation-triangle me-2"></i>{{ error }}
                </div>
              </form>
              
              <div class="text-center mt-4">
                <router-link 
                  to="/signup" 
                  class="text-warning text-decoration-none fw-medium"
                >
                  <i class="bi bi-person-plus me-2"></i>Create Account?
                </router-link>
              </div>
              
              <div class="mt-4 p-4 glass-effect rounded">
                <p class="text-white-50 text-center mb-2 fw-bold">Demo Credentials:</p>
                <div class="row text-center">
                  <div class="col-6">
                    <small class="text-white-50 d-block">Admin</small>
                    <small class="text-warning">admin@parking.com</small><br>
                    <small class="text-warning">admin</small>
                  </div>
                  <div class="col-6">
                    <small class="text-white-50 d-block">User</small>
                    <small class="text-info">Register new account</small>
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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const success = await authStore.login(email.value, password.value)
    
    if (success) {
      if (authStore.isAdmin) {
        router.push('/admin')
      } else {
        router.push('/user')
      }
    } else {
      error.value = 'Invalid email or password'
    }
  } catch (err) {
    error.value = 'An error occurred during login'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.glass-effect {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.fade-in {
  animation: fadeIn 0.8s ease-in-out;
}

.slide-in {
  animation: slideIn 0.6s ease-out;
}

.btn-hover {
  transition: all 0.3s ease;
}

.btn-hover:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0,0,0,0.3);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
  from { 
    transform: translateY(30px) scale(0.95); 
    opacity: 0; 
  }
  to { 
    transform: translateY(0) scale(1); 
    opacity: 1; 
  }
}

.form-control:focus {
  border-color: rgba(255, 255, 255, 0.5);
  box-shadow: 0 0 0 0.2rem rgba(255, 255, 255, 0.25);
}

.form-control::placeholder {
  color: rgba(255, 255, 255, 0.6);
}
</style>