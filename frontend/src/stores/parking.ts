import { defineStore } from 'pinia'
import { ref } from 'vue'
import { API_ENDPOINTS, getApiUrl } from '../config/api'

export interface ParkingLot {
  id: string
  name: string
  location: string
  address: string
  total_spots: number
  available_spots: number
  price_per_hour: number
  created_at: string
}

export interface UserDetails {
  id: string
  fullname: string
  email: string
  address: string
  pin_code: string
}

export interface BookingDetails {
  id: string
  duration_hours: number
  total_cost: number
  start_time: string
}

export interface ParkingSpot {
  id: string
  lot_id: string
  spot_number: string
  status: 'available' | 'occupied' | 'reserved'
  occupied_by?: string
  vehicle_number?: string
  booked_at?: string
  release_time?: string
  user_details?: UserDetails
  booking_details?: BookingDetails
}

export interface Booking {
  id: string
  user_id: string
  lot_id: string
  spot_id: string
  vehicle_number: string
  start_time: string
  end_time?: string
  duration_hours: number
  total_cost: number
  status: 'active' | 'completed'
}

export const useParkingStore = defineStore('parking', () => {
  const parkingLots = ref<ParkingLot[]>([])
  const parkingSpots = ref<ParkingSpot[]>([])
  const bookings = ref<Booking[]>([])

  const fetchParkingLots = async () => {
    try {
      const response = await fetch(API_ENDPOINTS.PARKING_LOTS)
      if (response.ok) {
        parkingLots.value = await response.json()
      }
    } catch (error) {
      console.error('Error fetching parking lots:', error)
    }
  }

  const createParkingLot = async (lotData: Omit<ParkingLot, 'id' | 'created_at' | 'available_spots'>) => {
    try {
      const response = await fetch(API_ENDPOINTS.PARKING_LOTS, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(lotData)
      })
      
      const result = await response.json()
      
      if (result.success) {
        await fetchParkingLots()
        return true
      }
      return false
    } catch (error) {
      console.error('Error creating parking lot:', error)
      return false
    }
  }

  const updateParkingLot = async (id: string, lotData: Partial<ParkingLot>) => {
    try {
      const response = await fetch(getApiUrl(`/api/parking-lots/${id}`), {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(lotData)
      })
      
      const result = await response.json()
      
      if (result.success) {
        await fetchParkingLots()
        return true
      }
      return false
    } catch (error) {
      console.error('Error updating parking lot:', error)
      return false
    }
  }

  const deleteParkingLot = async (id: string) => {
    try {
      const response = await fetch(getApiUrl(`/api/parking-lots/${id}`), {
        method: 'DELETE'
      })
      
      const result = await response.json()
      
      if (result.success) {
        await fetchParkingLots()
        return true
      }
      return false
    } catch (error) {
      console.error('Error deleting parking lot:', error)
      return false
    }
  }

  return {
    parkingLots,
    parkingSpots,
    bookings,
    fetchParkingLots,
    createParkingLot,
    updateParkingLot,
    deleteParkingLot
  }
})