<template>
  <div class="signup-container">
    <!-- Background Pattern -->
    <div class="background-pattern"></div>
    
    <!-- Main Content -->
    <div class="container-fluid h-100">
      <div class="row h-100">
        <!-- Left Side - Branding -->
        <div class="col-lg-6 d-none d-lg-flex branding-section">
          <div class="branding-content">
            <div class="brand-logo">
              <i class="bi bi-person-plus-fill"></i>
            </div>
            <h1 class="brand-title">Join ParkEase</h1>
            <p class="brand-subtitle">Create your account and start parking smarter</p>
            
            <div class="benefits-list">
              <div class="benefit-item">
                <i class="bi bi-lightning-charge-fill"></i>
                <span>Instant Booking</span>
              </div>
              <div class="benefit-item">
                <i class="bi bi-shield-check-fill"></i>
                <span>Secure & Safe</span>
              </div>
              <div class="benefit-item">
                <i class="bi bi-clock-fill"></i>
                <span>24/7 Access</span>
              </div>
              <div class="benefit-item">
                <i class="bi bi-star-fill"></i>
                <span>Premium Locations</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Right Side - Signup Form -->
        <div class="col-lg-6 signup-section">
          <div class="signup-form-container">
            <!-- Mobile Logo -->
            <div class="mobile-logo d-lg-none">
              <i class="bi bi-person-plus-fill"></i>
              <h2>Join ParkEase</h2>
            </div>
            
            <div class="signup-card">
              <div class="signup-header">
                <h3>Create Account</h3>
                <p>Fill in your details to get started</p>
              </div>
              
              <form @submit.prevent="handleSignup" class="signup-form">
                <div class="form-row">
                  <div class="form-group">
                    <label class="form-label">Email Address</label>
                    <div class="input-wrapper">
                      <i class="bi bi-envelope-fill input-icon"></i>
                      <input 
                        v-model="formData.email" 
                        type="email" 
                        class="form-control"
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
                        v-model="formData.password" 
                        type="password" 
                        class="form-control"
                        placeholder="Create password"
                        required
                      />
                    </div>
                  </div>
                </div>
                
                <div class="form-group">
                  <label class="form-label">Full Name</label>
                  <div class="input-wrapper">
                    <i class="bi bi-person-fill input-icon"></i>
                    <input 
                      v-model="formData.fullname" 
                      type="text" 
                      class="form-control"
                      placeholder="Enter your full name"
                      required
                    />
                  </div>
                </div>
                
                <div class="form-group">
                  <label class="form-label">Address</label>
                  <div class="input-wrapper">
                    <i class="bi bi-geo-alt-fill input-icon"></i>
                    <textarea 
                      v-model="formData.address" 
                      class="form-control textarea-control"
                      rows="3"
                      placeholder="Enter your address"
                      required
                    ></textarea>
                  </div>
                </div>
                
                <div class="form-group">
                  <label class="form-label">PIN Code</label>
                  <div class="input-wrapper">
                    <i class="bi bi-mailbox-fill input-icon"></i>
                    <input 
                      v-model="formData.pin_code" 
                      type="text" 
                      class="form-control"
                      placeholder="Enter 6-digit PIN code"
                      pattern="[0-9]{6}"
                      maxlength="6"
                      required
                    />
                  </div>
                </div>
                
                <button 
                  type="submit" 
                  class="btn btn-primary signup-btn"
                  :disabled="loading"
                >
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="bi bi-person-check-fill me-2"></i>
                  {{ loading ? 'Creating Account...' : 'Create Account' }}
                </button>
                
                <div v-if="error" class="alert alert-danger error-alert">
                  <i class="bi bi-exclamation-triangle-fill me-2"></i>{{ error }}
                </div>
              </form>
              
              <div class="signup-footer">
                <p>Already have an account? 
                  <router-link to="/login" class="login-link">
                    Sign In
                  </router-link>
                </p>
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
      error.value = 'Email already exists or registration failed. Please try again.'
    }
  } catch (err) {
    error.value = 'An error occurred during registration. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.signup-container {
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
  animation: float 20s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(1deg); }
}

.branding-section {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
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
}

.brand-logo {
  font-size: 4rem;
  margin-bottom: 1rem;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.05); }
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

.benefits-list {
  text-align: left;
}

.benefit-item {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  font-size: 1.1rem;
}

.benefit-item i {
  color: #ffd700;
  margin-right: 1rem;
  font-size: 1.2rem;
}

.signup-section {
  background: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  overflow-y: auto;
}

.signup-form-container {
  width: 100%;
  max-width: 500px;
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

.signup-card {
  background: #ffffff;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  border: 1px solid #e9ecef;
}

.signup-header {
  text-align: center;
  margin-bottom: 2rem;
}

.signup-header h3 {
  color: #2d3748;
  font-weight: 700;
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.signup-header p {
  color: #718096;
  font-size: 1rem;
  margin: 0;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row .form-group {
  margin-bottom: 0;
}

.form-label {
  color: #4a5568;
  font-weight: 600;
  margin-bottom: 0.5rem;
  display: block;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 1rem;
  top: 1rem;
  color: #a0aec0;
  font-size: 1.1rem;
  z-index: 2;
}

.form-control {
  background: #f7fafc;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 0.75rem 1rem 0.75rem 3rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  width: 100%;
}

.textarea-control {
  resize: vertical;
  min-height: 80px;
  padding-top: 1rem;
}

.textarea-control + .input-icon {
  top: 1rem;
}

.form-control:focus {
  background: #ffffff;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
  outline: none;
}

.form-control::placeholder {
  color: #a0aec0;
}

.signup-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 12px;
  padding: 0.875rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  width: 100%;
  margin-bottom: 1.5rem;
  transition: all 0.3s ease;
  color: white;
}

.signup-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
  background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
}

.signup-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
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

.signup-footer {
  text-align: center;
}

.signup-footer p {
  color: #718096;
  margin: 0;
}

.login-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
}

.login-link:hover {
  color: #5a67d8;
  text-decoration: underline;
}

/* Responsive Design */
@media (max-width: 768px) {
  .signup-card {
    padding: 2rem 1.5rem;
    margin: 1rem;
  }
  
  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }
  
  .form-row .form-group {
    margin-bottom: 1.5rem;
  }
  
  .brand-title {
    font-size: 2rem;
  }
  
  .signup-section {
    padding: 1rem;
  }
}

@media (max-width: 576px) {
  .signup-card {
    padding: 1.5rem 1rem;
  }
  
  .form-control {
    padding: 0.625rem 0.875rem 0.625rem 2.5rem;
  }
  
  .input-icon {
    left: 0.875rem;
    font-size: 1rem;
  }
  
  .textarea-control + .input-icon {
    top: 0.875rem;
  }
}
</style>