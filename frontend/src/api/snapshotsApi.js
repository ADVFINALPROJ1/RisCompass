import axiosInstance from './axiosInstance'

const snapshotsApi = {
  getSnapshots: () => axiosInstance.get('/snapshots/'),
  getSnapshotDetail: (id) => axiosInstance.get(`/snapshots/${id}/`),
  createSnapshot: (snapshotData) => axiosInstance.post('/snapshots/', snapshotData),
}

export default snapshotsApi
