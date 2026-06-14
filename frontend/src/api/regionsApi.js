import axiosInstance from './axiosInstance'

const regionsApi = {
  getRegions: () => axiosInstance.get('/v1/regions/'),
}

export default regionsApi
