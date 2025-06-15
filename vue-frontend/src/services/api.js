import axios from 'axios'
import { API_URL } from '@/config'

const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,  // Important for sending cookies cross-domain
})

// Request interceptor to add CSRF token to headers
api.interceptors.request.use((config) => {
  const csrfToken = localStorage.getItem('csrfToken') || ''
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

export default api