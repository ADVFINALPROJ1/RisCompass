import axiosInstance from './axiosInstance'

const industriesApi = {
  getIndustries: () => axiosInstance.get('/v1/industries/'),
}

export default industriesApi
