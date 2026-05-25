import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || '/api',
  timeout: 30000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = window.location.origin + import.meta.env.BASE_URL + '#/login'
    }
    return Promise.reject(err)
  },
)

export default api

// Auth
export const sendCode = (data) => api.post('/auth/send-code', data)
export const login = (data) => api.post('/auth/login', data)
export const getMe = () => api.get('/auth/me')

// Attractions
export const searchAttractions = (params) => {
  const clean = {}
  if (params.city) clean.city = params.city
  if (params.province) clean.province = params.province
  if (params.keyword) clean.keyword = params.keyword
  return api.get('/attractions', { params: clean })
}
export const getCities = () => api.get('/attractions/cities')
export const getAttraction = (id) => api.get(`/attractions/${id}`)

// Plans
export const generatePlan = (data) => api.post('/plans/generate', data)
export const listPlans = () => api.get('/plans')
export const getPlan = (id) => api.get(`/plans/${id}`)
export const deletePlan = (id) => api.delete(`/plans/${id}`)
export const getRouteOptions = (params) => api.get('/plans/route/options', { params })
