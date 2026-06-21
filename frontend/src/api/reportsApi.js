import axiosInstance from './axiosInstance'

const reportsApi = {
  generateReport: (snapshotId) => axiosInstance.post(`/snapshots/${snapshotId}/generate-report/`),
  getSnapshotReports: (snapshotId) => axiosInstance.get(`/snapshots/${snapshotId}/reports/`),
  getReportDetail: (reportId) => axiosInstance.get(`/reports/${reportId}/`),
}

export default reportsApi
