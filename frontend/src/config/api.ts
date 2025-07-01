// API Configuration for different environments
const getApiUrl = () => {
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

export const API_BASE_URL = getApiUrl()

// API endpoints
export const API_ENDPOINTS = {
  AUTH: {
    LOGIN: `${API_BASE_URL}/api/auth/login`,
    REGISTER: `${API_BASE_URL}/api/auth/register`,
  },
  PARKING_LOTS: `${API_BASE_URL}/api/parking-lots`,
  USERS: `${API_BASE_URL}/api/users`,
  BOOKINGS: `${API_BASE_URL}/api/bookings`,
  ANALYTICS: `${API_BASE_URL}/api/analytics`,
}

// Helper function to get API URL with endpoint
export const getApiUrl = (endpoint: string) => `${API_BASE_URL}${endpoint}`