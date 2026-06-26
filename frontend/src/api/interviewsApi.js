import axiosInstance from './axiosInstance'

const interviewsApi = {
  // Get interview session with questions
  getInterviewSession: (sessionId) => {
    return axiosInstance.get(`/interviews/${sessionId}/`)
  },

  // Save answers for interview session
  saveAnswers: (sessionId, answers) => {
    return axiosInstance.post(`/interviews/${sessionId}/answers/`, {
      answers: answers
    })
  },

  // Complete interview and generate report
  completeInterview: (sessionId) => {
    return axiosInstance.post(`/interviews/${sessionId}/complete/`)
  }
}

export default interviewsApi
