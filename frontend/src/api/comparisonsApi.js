import axiosInstance from './axiosInstance'

const comparisonsApi = {
  getComparisons: () => axiosInstance.get('/comparisons/'),
  getComparisonDetail: (id) => axiosInstance.get(`/comparisons/${id}/`),
  createComparison: (comparisonData) => axiosInstance.post('/comparisons/', comparisonData),
  deleteComparison: (id) => axiosInstance.delete(`/comparisons/${id}/`),
}

export default comparisonsApi
