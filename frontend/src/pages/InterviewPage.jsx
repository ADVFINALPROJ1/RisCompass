import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import interviewsApi from '../api/interviewsApi'
import LoadingSpinner from '../components/LoadingSpinner'

export default function InterviewPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [session, setSession] = useState(null)
  const [questions, setQuestions] = useState([])
  const [answers, setAnswers] = useState({})
  const [loading, setLoading] = useState(true)
  const [submitting, setSubmitting] = useState(false)
  const [completing, setCompleting] = useState(false)
  const [error, setError] = useState('')
  const [saveError, setSaveError] = useState('')

  useEffect(() => {
    const fetchSession = async () => {
      try {
        const response = await interviewsApi.getInterviewSession(id)
        setSession(response.data)
        setQuestions(response.data.questions || [])
        
        // Initialize answers from existing answers if any
        const existingAnswers = {}
        if (response.data.answers && response.data.answers.length > 0) {
          response.data.answers.forEach(answer => {
            existingAnswers[answer.question] = {
              text: answer.answer_text || '',
              value: answer.answer_value || null
            }
          })
        }
        setAnswers(existingAnswers)
      } catch (err) {
        setError('Unable to load interview session. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    fetchSession()
  }, [id])

  const handleAnswerChange = (questionId, field, value) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: {
        ...prev[questionId],
        [field]: value
      }
    }))
  }

  const handleSaveAnswers = async () => {
    setSubmitting(true)
    setSaveError('')
    
    try {
      // Convert answers to the format expected by the API
      const answersArray = Object.entries(answers).map(([questionId, answerData]) => ({
        question_id: parseInt(questionId),
        answer_text: answerData.text || '',
        answer_value: answerData.value || null
      }))

      await interviewsApi.saveAnswers(id, answersArray)
      setSaveError('')
    } catch (err) {
      setSaveError('Failed to save answers. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  const handleCompleteInterview = async () => {
    setCompleting(true)
    setError('')
    
    try {
      // First save any unsaved answers
      const answersArray = Object.entries(answers).map(([questionId, answerData]) => ({
        question_id: parseInt(questionId),
        answer_text: answerData.text || '',
        answer_value: answerData.value || null
      }))

      await interviewsApi.saveAnswers(id, answersArray)
      
      // Then complete the interview
      const response = await interviewsApi.completeInterview(id)
      
      // Get the report ID from the response
      const reportId = response.data.risk_report.id
      navigate(`/reports/${reportId}`)
    } catch (err) {
      console.error('Interview completion error:', err)
      const errorMessage = err.response?.data?.detail || err.response?.data?.error || err.message || 'Failed to complete interview. Please try again.'
      setError(errorMessage)
      setCompleting(false)
    }
  }

  const renderQuestionInput = (question) => {
    const answer = answers[question.id] || { text: '', value: null }

    switch (question.question_type) {
      case 'text':
        return (
          <textarea
            value={answer.text}
            onChange={(e) => handleAnswerChange(question.id, 'text', e.target.value)}
            placeholder="Enter your answer..."
            className="w-full rounded-2xl border border-slate-200 bg-slate-50 p-4 text-slate-900 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
            rows={4}
          />
        )
      
      case 'multiple_choice':
        return (
          <div className="space-y-2">
            <textarea
              value={answer.text}
              onChange={(e) => handleAnswerChange(question.id, 'text', e.target.value)}
              placeholder="Enter your answer..."
              className="w-full rounded-2xl border border-slate-200 bg-slate-50 p-4 text-slate-900 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
              rows={3}
            />
          </div>
        )
      
      case 'scale':
        return (
          <div className="space-y-4">
            <input
              type="range"
              min="1"
              max="10"
              value={answer.value || 5}
              onChange={(e) => handleAnswerChange(question.id, 'value', parseInt(e.target.value))}
              className="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-primary"
            />
            <div className="flex justify-between text-sm text-slate-500">
              <span>1 (Low)</span>
              <span className="font-semibold text-slate-900">{answer.value || 5}</span>
              <span>10 (High)</span>
            </div>
            <textarea
              value={answer.text}
              onChange={(e) => handleAnswerChange(question.id, 'text', e.target.value)}
              placeholder="Add any additional comments (optional)..."
              className="w-full rounded-2xl border border-slate-200 bg-slate-50 p-4 text-slate-900 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
              rows={2}
            />
          </div>
        )
      
      case 'yes_no':
        return (
          <div className="space-y-4">
            <div className="flex gap-4">
              <button
                onClick={() => handleAnswerChange(question.id, 'value', 1)}
                className={`flex-1 rounded-2xl border-2 p-4 font-semibold transition-all ${
                  answer.value === 1
                    ? 'border-primary bg-primary text-white'
                    : 'border-slate-200 bg-slate-50 text-slate-700 hover:border-slate-300'
                }`}
              >
                Yes
              </button>
              <button
                onClick={() => handleAnswerChange(question.id, 'value', 0)}
                className={`flex-1 rounded-2xl border-2 p-4 font-semibold transition-all ${
                  answer.value === 0
                    ? 'border-primary bg-primary text-white'
                    : 'border-slate-200 bg-slate-50 text-slate-700 hover:border-slate-300'
                }`}
              >
                No
              </button>
            </div>
            <textarea
              value={answer.text}
              onChange={(e) => handleAnswerChange(question.id, 'text', e.target.value)}
              placeholder="Add any additional comments (optional)..."
              className="w-full rounded-2xl border border-slate-200 bg-slate-50 p-4 text-slate-900 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
              rows={2}
            />
          </div>
        )
      
      default:
        return (
          <textarea
            value={answer.text}
            onChange={(e) => handleAnswerChange(question.id, 'text', e.target.value)}
            placeholder="Enter your answer..."
            className="w-full rounded-2xl border border-slate-200 bg-slate-50 p-4 text-slate-900 focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20"
            rows={4}
          />
        )
    }
  }

  const getRiskCategoryColor = (category) => {
    const colors = {
      'financial': 'bg-blue-100 text-blue-700',
      'market': 'bg-green-100 text-green-700',
      'legal': 'bg-purple-100 text-purple-700',
      'cultural': 'bg-orange-100 text-orange-700',
      'operational': 'bg-red-100 text-red-700'
    }
    return colors[category] || 'bg-slate-100 text-slate-700'
  }

  if (loading) {
    return <LoadingSpinner />
  }

  if (error) {
    return (
      <div className="section">
        <div className="rounded-3xl border border-red-200 bg-red-50 p-8 text-center">
          <p className="text-red-700">{error}</p>
          <Link to="/dashboard" className="btn-primary mt-4 inline-flex items-center justify-center">
            Back to Dashboard
          </Link>
        </div>
      </div>
    )
  }

  if (!session) {
    return (
      <div className="section">
        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-8 text-center">
          <p className="text-slate-600">Interview session not found.</p>
          <Link to="/dashboard" className="btn-primary mt-4 inline-flex items-center justify-center">
            Back to Dashboard
          </Link>
        </div>
      </div>
    )
  }

  const answeredCount = Object.keys(answers).filter(key => {
    const answer = answers[key]
    return (answer.text && answer.text.trim()) || answer.value !== null
  }).length

  const totalQuestions = questions.length
  const progress = totalQuestions > 0 ? Math.round((answeredCount / totalQuestions) * 100) : 0

  return (
    <div className="section">
      <div className="mb-8">
        <Link to="/dashboard" className="text-sm text-slate-500 hover:text-slate-700">
          ← Back to Dashboard
        </Link>
      </div>

      <div className="space-y-8">
        {/* Header */}
        <div className="rounded-[2rem] border border-slate-200 bg-gradient-to-br from-slate-900 to-slate-950 p-8 text-white shadow-2xl">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-300">Interview</p>
              <h1 className="mt-3 text-4xl font-semibold">Risk Assessment Interview</h1>
              <p className="mt-2 text-sm text-slate-300">
                {session.trigger_reason || 'Please answer the following questions to help us assess your business risks.'}
              </p>
            </div>
            <div className="text-center sm:text-right">
              <div className="text-sm uppercase tracking-[0.2em] text-slate-300">Progress</div>
              <div className="mt-2 text-4xl font-bold">{answeredCount}/{totalQuestions}</div>
              <div className="mt-2 h-2 w-32 overflow-hidden rounded-full bg-slate-700 sm:ml-auto">
                <div 
                  className="h-full bg-primary transition-all duration-300"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          </div>
        </div>

        {/* Questions */}
        <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-xl">
          <h2 className="text-2xl font-semibold text-slate-950">Questions</h2>
          
          {questions.length === 0 ? (
            <div className="mt-6 rounded-2xl bg-slate-50 p-8 text-center">
              <p className="text-slate-600">No questions available for this interview.</p>
            </div>
          ) : (
            <div className="mt-6 space-y-8">
              {questions.map((question, index) => (
                <div key={question.id} className="rounded-2xl border border-slate-200 bg-slate-50 p-6">
                  <div className="mb-4 flex flex-wrap items-center gap-3">
                    <span className="rounded-full bg-primary px-3 py-1 text-sm font-semibold text-white">
                      Q{index + 1}
                    </span>
                    <span className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] ${getRiskCategoryColor(question.risk_category)}`}>
                      {question.risk_category.replace('_', ' ')}
                    </span>
                  </div>
                  <h3 className="mb-4 text-lg font-semibold text-slate-900">{question.question_text}</h3>
                  {renderQuestionInput(question)}
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-xl">
          {saveError && (
            <div className="mb-6 rounded-3xl border border-red-200 bg-red-50 p-5 text-sm text-red-700">
              {saveError}
            </div>
          )}
          
          {error && (
            <div className="mb-6 rounded-3xl border border-red-200 bg-red-50 p-5 text-sm text-red-700">
              {error}
            </div>
          )}

          <div className="flex flex-col gap-4 sm:flex-row sm:justify-end">
            <button
              onClick={handleSaveAnswers}
              disabled={submitting || questions.length === 0}
              className="btn-secondary inline-flex items-center justify-center px-8 py-4"
            >
              {submitting ? 'Saving...' : 'Save Progress'}
            </button>
            <button
              onClick={handleCompleteInterview}
              disabled={completing || answeredCount === 0 || questions.length === 0}
              className="btn-primary inline-flex items-center justify-center px-8 py-4"
            >
              {completing ? 'Processing...' : 'Complete & Generate Report'}
            </button>
          </div>
          
          <p className="mt-4 text-sm text-slate-500">
            {completing 
              ? 'AI is analyzing your responses and generating your risk report. This may take a moment...'
              : 'Save your progress or complete the interview to generate your risk assessment report.'
            }
          </p>
        </div>
      </div>
    </div>
  )
}
