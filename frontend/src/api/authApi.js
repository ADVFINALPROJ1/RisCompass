import axiosInstance from './axiosInstance'

const authApi = {
  login: (credentials) => axiosInstance.post('/auth/login/', credentials),
  register: (registrationData) => axiosInstance.post('/auth/register/', registrationData),
  refreshToken: (refreshToken) => axiosInstance.post('/auth/refresh/', { refresh: refreshToken }),
  getMe: () => axiosInstance.get('/auth/me/'),
}

export default authApi
