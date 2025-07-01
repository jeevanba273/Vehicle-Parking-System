// API Configuration for different environments
const getBaseUrl = () => {
  // Check if we're in development
  if (import.meta.env.DEV) {
    return 'http://localhost:5000'
  }
  
  // Check for custom API URL from environment variables
  if (import.meta.env.VITE_API_URL) {
    return import.meta.env.VITE_API_URL
  }
  
  // Default production API URL (replace with your Railway backend URL)
  return 'https://your-backend-app.railway.app'
}

export const API_BASE_URL = getBaseUrl()

// Helper function to get API URL with endpoint
export const getApiUrl = (endpoint: string) => {
  return `${API_BASE_URL}${endpoint}`
}

// API endpoints
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: getApiUrl('/api/auth/login'),
    REGISTER: getApiUrl('/api/auth/register'),
  },
  PARKING_LOTS: getApiUrl('/api/parking-lots'),
  USERS: getApiUrl('/api/users'),
  BOOKINGS: getApiUrl('/api/bookings'),
  ANALYTICS: getApiUrl('/api/analytics'),
}