<template>
  <div class="min-vh-100 d-flex align-items-center justify-content-center" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="text-center mb-4 fade-in">
            <h1 class="text-white fw-bold mb-2 display-5">Vehicle Parking System</h1>
            <p class="text-white-50 lead">Create your account to get started.</p>
          </div>
          
          <div class="card glass-effect border-0 shadow-lg slide-in">
            <div class="card-body p-5">
              <h2 class="text-white text-center mb-4 fw-bold">User Signup</h2>
              
              <form @submit.prevent="handleSignup">
                <div class="row g-3">
                  <div class="col-12">
                    <label class="form-label text-white-50 fw-medium">Email ID (Username)</label>
                    <input 
                      v-model="formData.email" 
                      type="email" 
                      class="form-control form-control-lg bg-transparent text-white border-light"
                      style="backdrop-filter: blur(10px);"
                      placeholder="Enter your email"
                      required
                    />
                  </div>
                  
                  <div class="col-12">
                    <label class="form-label text-white-50 fw-medium">Password</label>
                    <input 
                      v-model="formData.password" 
                      type="password" 
                      class="form-control form-control-lg bg-transparent text-white border-light"
                      style="backdrop-filter: blur(10px);"
                      placeholder="Enter your password"
                      required
                    />
                  </div>
                  
                  <div class="col-12">
                    <label class="form-label text-white-50 fw-medium">Full Name</label>
                    <input 
                      v-model="formData.fullname" 
                      type="text" 
                      class="form-control form-control-lg bg-transparent text-white border-light"
                      style="backdrop-filter: blur(10px);"
                      placeholder="Enter your full name"
                      required
                    />
                  </div>
                  
                  <div class="col-12">
                    <label class="form-label text-white-50 fw-medium">Address</label>
                    <textarea 
                      v-model="formData.address" 
                      class="form-control bg-transparent text-white border-light"
                      style="backdrop-filter: blur(10px);"
                      rows="3"
                      placeholder="Enter your address"
                      required
                    ></textarea>
                  </div>
                  
                  <div class="col-12">
                    <label class="form-label text-white-50 fw-medium">Pin Code</label>
                    <input 
                      v-model="formData.pin_code" 
                      type="text" 
                      class="form-control form-control-lg bg-transparent text-white border-light"
                      style="backdrop-filter: blur(10px);"
                      placeholder="Enter 6-digit pin code"
                      pattern="[0-9]{6}"
                      maxlength="6"
                      required
                    />
                  </div>
                </div>
                
                <button 
                  type="submit" 
                  class="btn btn-primary btn-lg w-100 btn-hover fw-bold mt-4"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  {{ loading ? 'Creating Account...' : 'Register' }}
                </button>
                
                <div v-if="error" class="alert alert-danger mt-3 glass-effect">
                  <i class="bi bi-exclamation-triangle me-2"></i>{{ error }}
                </div>
              </form>
              
              <div class="text-center mt-4">
                <router-link 
                  to="/login" 
                  class="text-warning text-decoration-none fw-medium"
                >
                  <i class="bi bi-arrow-left me-2"></i>Login here!
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const formData = reactive({
  email: '',
  password: '',
  fullname: '',
  address: '',
  pin_code: ''
})

const loading = ref(false)
const error = ref('')

const handleSignup = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const success = await authStore.signup({
      email: formData.email,
      password: formData.password,
      fullname: formData.fullname,
      address: formData.address,
      pin_code: formData.pin_code
    })
    
    if (success) {
      router.push('/user')
    } else {
      error.value = 'Email already exists or registration failed'
    }
  } catch (err) {
    error.value = 'An error occurred during registration'
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