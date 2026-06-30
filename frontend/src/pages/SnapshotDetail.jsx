import { useEffect, useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import snapshotsApi from '../api/snapshotsApi'
import reportsApi from '../api/reportsApi'
import LoadingSpinner from '../components/LoadingSpinner'

export default function SnapshotDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [snapshot, setSnapshot] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [generating, setGenerating] = useState(false)
  const [generateError, setGenerateError] = useState('')

  useEffect(() => {
    const fetchSnapshot = async () => {
      try {
        const response = await snapshotsApi.getSnapshotDetail(id)
        setSnapshot(response.data)
      } catch (err) {
        setError('Unable to load snapshot details. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    fetchSnapshot()
  }, [id])

  const handleGenerateReport = async () => {
    setGenerating(true)
    setGenerateError('')
    
    try {
      const response = await reportsApi.generateReport(id)
      const reportId = response.data.id
      navigate(`/reports/${reportId}`)
    } catch (err) {
      setGenerateError('Failed to generate report. Please try again.')
      setGenerating(false)
    }
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

  if (!snapshot) {
    return (
      <div className="section">
        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-8 text-center">
          <p className="text-slate-600">Snapshot not found.</p>
          <Link to="/dashboard" className="btn-primary mt-4 inline-flex items-center justify-center">
            Back to Dashboard
          </Link>
        </div>
      </div>
    )
  }

  return (
    <div className="section">
      <div className="mb-8">
        <Link to="/dashboard" className="text-sm text-slate-500 hover:text-slate-700">
          ← Back to Dashboard
        </Link>
      </div>

      <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-xl">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
          <div>
            <p className="text-sm font-semibold uppercase tracking-[0.24em] text-primary">Snapshot Details</p>
            <h1 className="mt-3 text-4xl font-semibold text-slate-950">{snapshot.title}</h1>
            <p className="mt-2 text-sm text-slate-500">
              Created on {new Date(snapshot.created_at).toLocaleDateString()}
            </p>
          </div>
          <span className="rounded-full bg-slate-100 px-4 py-2 text-sm font-semibold uppercase tracking-[0.16em] text-slate-700">
            {snapshot.business_stage.replace('_', ' ')}
          </span>
        </div>

        {snapshot.description && (
          <div className="mt-6">
            <h2 className="text-lg font-semibold text-slate-900">Description</h2>
            <p className="mt-2 text-slate-600">{snapshot.description}</p>
          </div>
        )}

        <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <div className="rounded-2xl bg-slate-50 p-6">
            <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Industry</div>
            <div className="mt-2 text-sm font-semibold text-slate-900">
              {snapshot.industry?.name || snapshot.industry_name || snapshot.industry || 'Unknown'}
            </div>
          </div>
          <div className="rounded-2xl bg-slate-50 p-6">
            <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Region</div>
            <div className="mt-2 text-sm font-semibold text-slate-900">
              {snapshot.region?.name || snapshot.region_name || snapshot.region || 'Unknown'}
            </div>
          </div>
          <div className="rounded-2xl bg-slate-50 p-6">
            <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Budget</div>
            <div className="mt-2 text-sm font-semibold text-slate-900">
              {snapshot.startup_budget ? `${snapshot.currency || '$'}${snapshot.startup_budget}` : 'Not specified'}
            </div>
          </div>
          <div className="rounded-2xl bg-slate-50 p-6">
            <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Business Size</div>
            <div className="mt-2 text-sm font-semibold text-slate-900">
              {snapshot.business_size?.replace('_', ' ') || 'N/A'}
            </div>
          </div>
          <div className="rounded-2xl bg-slate-50 p-6">
            <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Physical Location</div>
            <div className="mt-2 text-sm font-semibold text-slate-900">
              {snapshot.has_physical_location ? 'Yes' : 'No'}
            </div>
          </div>
          <div className="rounded-2xl bg-slate-50 p-6">
            <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Last Updated</div>
            <div className="mt-2 text-sm font-semibold text-slate-900">
              {new Date(snapshot.updated_at).toLocaleDateString()}
            </div>
          </div>
        </div>

        {snapshot.target_customer && (
          <div className="mt-8">
            <h2 className="text-lg font-semibold text-slate-900">Target Customer</h2>
            <p className="mt-2 text-slate-600">{snapshot.target_customer}</p>
          </div>
        )}

        <div className="mt-10 border-t border-slate-200 pt-8">
          {generateError && (
            <div className="mb-6 rounded-3xl border border-red-200 bg-red-50 p-5 text-sm text-red-700">
              {generateError}
            </div>
          )}
          
          {snapshot.interview_session ? (
            <div className="space-y-4">
              <div className="rounded-3xl border border-purple-200 bg-purple-50 p-6">
                <h3 className="text-lg font-semibold text-purple-900">Interview</h3>
                <p className="mt-2 text-sm text-purple-700">
                  {snapshot.interview_session.trigger_reason || 'Enhance your risk assessment with local insights.'}
                </p>
                {snapshot.interview_session.status === 'completed' ? (
                  <div className="mt-4 space-y-3">
                    <Link
                      to={`/reports/${snapshot.interview_session.risk_report_id}`}
                      className="inline-flex items-center justify-center rounded-full bg-green-500 px-6 py-3 text-sm font-semibold text-white transition hover:bg-green-600"
                    >
                      View Interview Report
                    </Link>
                    <Link
                      to={`/interviews/${snapshot.interview_session.id}`}
                      className="ml-3 inline-flex items-center justify-center rounded-full border border-purple-500 px-6 py-3 text-sm font-semibold text-purple-600 transition hover:bg-purple-50"
                    >
                      Edit & Regenerate
                    </Link>
                  </div>
                ) : (
                  <Link
                    to={`/interviews/${snapshot.interview_session.id}`}
                    className={`mt-4 inline-flex items-center justify-center rounded-full px-6 py-3 text-sm font-semibold transition ${
                      snapshot.interview_session.status === 'in_progress'
                        ? 'bg-amber-500 text-white hover:bg-amber-600'
                        : 'bg-purple-500 text-white hover:bg-purple-600'
                    }`}
                  >
                    {snapshot.interview_session.status === 'in_progress'
                      ? 'Continue Interview'
                      : 'Start Interview'}
                  </Link>
                )}
              </div>
              
              <div className="text-center">
                <p className="text-sm text-slate-500">Or generate a report based on available data (World Bank):</p>
                <button
                  onClick={handleGenerateReport}
                  disabled={generating}
                  className="mt-2 btn-secondary inline-flex items-center justify-center px-6 py-3"
                >
                  {generating ? 'Generating Report...' : 'Generate Risk Report (Limited Data)'}
                </button>
              </div>
            </div>
          ) : (
            <button
              onClick={handleGenerateReport}
              disabled={generating}
              className="btn-primary inline-flex items-center justify-center px-8 py-4 text-lg"
            >
              {generating ? 'Generating Report...' : 'Generate Risk Report'}
            </button>
          )}
          
          {!snapshot.interview_session && (
            <p className="mt-3 text-sm text-slate-500">
              This will analyze your snapshot and generate a comprehensive risk assessment.
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
