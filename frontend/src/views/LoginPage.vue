<template>
  <div class="login-container">
    <!-- Background Pattern -->
    <div class="background-pattern"></div>
    
    <!-- Main Content -->
    <div class="container-fluid h-100">
      <div class="row h-100">
        <!-- Left Side - Branding -->
        <div class="col-lg-6 d-none d-lg-flex branding-section">
          <div class="branding-content">
            <div class="brand-logo">
              <i class="bi bi-car-front-fill"></i>
            </div>
            <h1 class="brand-title">ParkEase</h1>
            <p class="brand-subtitle">Smart Parking Management System</p>
            
            <div class="features-list">
              <div class="feature-item">
                <i class="bi bi-check-circle-fill"></i>
                <span>Real-time Spot Availability</span>
              </div>
              <div class="feature-item">
                <i class="bi bi-check-circle-fill"></i>
                <span>Easy Online Booking</span>
              </div>
              <div class="feature-item">
                <i class="bi bi-check-circle-fill"></i>
                <span>Secure Payment System</span>
              </div>
              <div class="feature-item">
                <i class="bi bi-check-circle-fill"></i>
                <span>24/7 Customer Support</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Right Side - Login Form -->
        <div class="col-lg-6 login-section">
          <div class="login-form-container">
            <!-- Mobile Logo -->
            <div class="mobile-logo d-lg-none">
              <i class="bi bi-car-front-fill"></i>
              <h2>ParkEase</h2>
            </div>
            
            <div class="login-card">
              <div class="login-header">
                <h3>Welcome Back!</h3>
                <p>Sign in to your account to continue</p>
              </div>
              
              <form @submit.prevent="handleLogin" class="login-form">
                <div class="form-group">
                  <label class="form-label">Email Address</label>
                  <div class="input-wrapper">
                    <i class="bi bi-envelope-fill input-icon"></i>
                    <input 
                      v-model="email" 
                      type="email" 
                      class="form-control login-input"
                      placeholder="Enter your email"
                      required
                    />
                  </div>
                </div>
                
                <div class="form-group">
                  <label class="form-label">Password</label>
                  <div class="input-wrapper">
                    <i class="bi bi-lock-fill input-icon"></i>
                    <input 
                      v-model="password" 
                      type="password" 
                      class="form-control login-input"
                      placeholder="Enter your password"
                      required
                    />
                  </div>
                </div>
                
                <button 
                  type="submit" 
                  class="login-btn"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="bi bi-box-arrow-in-right me-2"></i>
                  {{ loading ? 'Signing in...' : 'Sign In' }}
                </button>
                
                <div v-if="error" class="alert alert-danger error-alert">
                  <i class="bi bi-exclamation-triangle-fill me-2"></i>{{ error }}
                </div>
              </form>
              
              <div class="login-footer">
                <p>Don't have an account? 
                  <router-link to="/signup" class="signup-link">
                    Create Account
                  </router-link>
                </p>
              </div>
              
              <!-- Demo Credentials -->
              <div class="demo-credentials">
                <h6><i class="bi bi-info-circle-fill me-2"></i>Demo Credentials</h6>
                <div class="demo-grid">
                  <div class="demo-item">
                    <strong>Admin Access</strong>
                    <div class="demo-details">
                      <span>Email: admin@parking.com</span>
                      <span>Password: admin</span>
                    </div>
                  </div>
                  <div class="demo-item">
                    <strong>User Access</strong>
                    <div class="demo-details">
                      <span>Create new account</span>
                      <span>or register below</span>
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
      error.value = 'Invalid email or password. Please check your credentials and try again.'
    }
  } catch (err) {
    console.error('Login error:', err)
    error.value = 'An error occurred during login. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  position: relative;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  overflow: hidden;
}

.background-pattern {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 25% 25%, rgba(255,255,255,0.1) 2px, transparent 2px),
    radial-gradient(circle at 75% 75%, rgba(255,255,255,0.1) 2px, transparent 2px);
  background-size: 50px 50px;
}

.branding-section {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  align-items: flex-start;
  justify-content: center;
  position: relative;
  overflow: hidden;
  padding-top: 3rem;
}

.branding-section::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="2" fill="rgba(255,255,255,0.1)"/></svg>') repeat;
  animation: drift 30s linear infinite;
}

@keyframes drift {
  0% { transform: translate(0, 0); }
  100% { transform: translate(-50px, -50px); }
}

.branding-content {
  text-align: center;
  color: white;
  z-index: 2;
  position: relative;
  max-width: 400px;
  padding: 2rem;
  margin-top: 2rem;
}

.brand-logo {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.brand-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.brand-subtitle {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.features-list {
  text-align: left;
}

.feature-item {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.feature-item i {
  color: #00ff88;
  margin-right: 1rem;
  font-size: 1.2rem;
}

.login-section {
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-form-container {
  width: 100%;
  max-width: 450px;
  position: relative;
  z-index: 10;
}

.mobile-logo {
  text-align: center;
  margin-bottom: 2rem;
  color: #667eea;
}

.mobile-logo i {
  font-size: 3rem;
  margin-bottom: 0.5rem;
  display: block;
}

.mobile-logo h2 {
  font-weight: 800;
  margin: 0;
}

.login-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  border: 1px solid #e9ecef;
  position: relative;
  z-index: 10;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h3 {
  color: #2d3748;
  font-weight: 700;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.login-header p {
  color: #718096;
  font-size: 1rem;
  margin: 0;
}

.login-form {
  position: relative;
  z-index: 10;
}

.form-group {
  margin-bottom: 1.5rem;
  position: relative;
  z-index: 10;
}

.form-label {
  color: #4a5568;
  font-weight: 600;
  margin-bottom: 0.5rem;
  display: block;
}

.input-wrapper {
  position: relative;
  z-index: 10;
}

.input-icon {
  position: absolute;
  left: 1.25rem;
  top: 50%;
  transform: translateY(-50%);
  color: #a0aec0;
  font-size: 1.1rem;
  z-index: 12;
  pointer-events: none;
}

.login-input {
  background: #f7fafc !important;
  border: 2px solid #e2e8f0 !important;
  border-radius: 12px !important;
  padding: 0.875rem 1.25rem 0.875rem 4rem !important;
  font-size: 1rem !important;
  transition: all 0.3s ease !important;
  width: 100% !important;
  line-height: 1.5 !important;
  cursor: text !important;
  pointer-events: auto !important;
  position: relative !important;
  z-index: 11 !important;
}

.login-input:focus {
  background: #ffffff !important;
  border-color: #667eea !important;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
  outline: none !important;
}

.login-input::placeholder {
  color: #a0aec0 !important;
  font-size: 1rem !important;
  padding-left: 0.25rem !important;
}

.login-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
  border: none !important;
  border-radius: 12px !important;
  padding: 0.875rem 2rem !important;
  font-size: 1.1rem !important;
  font-weight: 600 !important;
  width: 100% !important;
  margin-bottom: 1.5rem !important;
  transition: all 0.3s ease !important;
  color: white !important;
  cursor: pointer !important;
  pointer-events: auto !important;
  user-select: none !important;
  display: block !important;
  text-align: center !important;
  position: relative !important;
  z-index: 15 !important;
  outline: none !important;
  text-decoration: none !important;
  font-family: inherit !important;
  line-height: 1.5 !important;
  vertical-align: middle !important;
  touch-action: manipulation !important;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px) !important;
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3) !important;
  background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%) !important;
}

.login-btn:active {
  transform: translateY(0) !important;
}

.login-btn:disabled {
  opacity: 0.7 !important;
  cursor: not-allowed !important;
  pointer-events: none !important;
}

.error-alert {
  background: #fed7d7;
  border: 1px solid #feb2b2;
  color: #c53030;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.login-footer {
  text-align: center;
  margin-bottom: 2rem;
  position: relative;
  z-index: 10;
}

.login-footer p {
  color: #718096;
  margin: 0;
}

.signup-link {
  color: #667eea !important;
  text-decoration: none !important;
  font-weight: 600 !important;
  transition: color 0.3s ease !important;
  cursor: pointer !important;
  pointer-events: auto !important;
  position: relative !important;
  z-index: 15 !important;
}

.signup-link:hover {
  color: #5a67d8 !important;
  text-decoration: underline !important;
}

.demo-credentials {
  background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid #e2e8f0;
}

.demo-credentials h6 {
  color: #4a5568;
  font-weight: 600;
  margin-bottom: 1rem;
  text-align: center;
}

.demo-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.demo-item {
  text-align: center;
}

.demo-item strong {
  color: #2d3748;
  font-size: 0.9rem;
  display: block;
  margin-bottom: 0.5rem;
}

.demo-details {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.demo-details span {
  color: #718096;
  font-size: 0.8rem;
  background: #ffffff;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
  border: 1px solid #e2e8f0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .login-card {
    padding: 2rem 1.5rem;
    margin: 1rem;
  }
  
  .demo-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .brand-title {
    font-size: 2rem;
  }
  
  .login-section {
    padding: 1rem;
  }
  
  .branding-section {
    padding-top: 2rem;
  }
  
  .branding-content {
    margin-top: 1rem;
  }
}

@media (max-width: 576px) {
  .login-card {
    padding: 1.5rem 1rem;
  }
  
  .login-input {
    padding: 0.75rem 1rem 0.75rem 3.5rem !important;
  }
  
  .input-icon {
    left: 1rem;
    font-size: 1rem;
  }
}
</style>