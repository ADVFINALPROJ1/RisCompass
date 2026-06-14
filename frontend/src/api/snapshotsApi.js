import axiosInstance from './axiosInstance'

const snapshotsApi = {
  getSnapshots: () => axiosInstance.get('/snapshots/'),
  createSnapshot: (snapshotData) => axiosInstance.post('/snapshots/', snapshotData),
}

export default snapshotsApi
