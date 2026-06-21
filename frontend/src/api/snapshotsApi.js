import axiosInstance from './axiosInstance'

const snapshotsApi = {
  getSnapshots: () => axiosInstance.get('/snapshots/'),
  getSnapshotDetail: (id) => axiosInstance.get(`/snapshots/${id}/`),
  createSnapshot: (snapshotData) => axiosInstance.post('/snapshots/', snapshotData),
  deleteSnapshot: (id) => axiosInstance.delete(`/snapshots/${id}/`),
}

export default snapshotsApi
