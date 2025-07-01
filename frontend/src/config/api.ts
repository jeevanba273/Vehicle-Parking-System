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
  
  // Production API URL - your Railway backend
  return 'https://vehicle-parking-system-production.up.railway.app'
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

// Add request interceptor for better error handling
export const apiRequest = async (url: string, options: RequestInit = {}) => {
  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  }

  try {
    const response = await fetch(url, defaultOptions)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return response
  } catch (error) {
    console.error('API request failed:', error)
    throw error
  }
}