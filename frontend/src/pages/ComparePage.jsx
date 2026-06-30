import { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { Link } from 'react-router-dom'
import snapshotsApi from '../api/snapshotsApi'
import comparisonsApi from '../api/comparisonsApi'
import reportsApi from '../api/reportsApi'
import LoadingSpinner from '../components/LoadingSpinner'
import ErrorMessage from '../components/ErrorMessage'
import EmptyState from '../components/EmptyState'

const FILTER_FOCUS_OPTIONS = [
  { value: 'overall', label: 'Overall' },
  { value: 'financial', label: 'Financial' },
  { value: 'market', label: 'Market' },
  { value: 'legal', label: 'Legal' },
  { value: 'cultural', label: 'Cultural' },
  { value: 'operational', label: 'Operational' },
]

export default function ComparePage() {
  const { user } = useAuth()
  const [snapshots, setSnapshots] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [snapshotA, setSnapshotA] = useState('')
  const [snapshotB, setSnapshotB] = useState('')
  const [filterFocus, setFilterFocus] = useState('overall')
  const [comparing, setComparing] = useState(false)
  const [comparisonResult, setComparisonResult] = useState(null)
  const [comparisonError, setComparisonError] = useState('')

  useEffect(() => {
    const fetchSnapshots = async () => {
      try {
        const response = await snapshotsApi.getSnapshots()
        const snapshotsData = Array.isArray(response.data)
          ? response.data
          : response.data.results || []
        
        // Check which snapshots have risk reports
        const snapshotsWithReports = await Promise.all(
          snapshotsData.map(async (snapshot) => {
            try {
              const reportResponse = await reportsApi.getSnapshotReports(snapshot.id)
              const hasReport = Array.isArray(reportResponse.data)
                ? reportResponse.data.length > 0
                : (reportResponse.data.results?.length > 0 || false)
              return { ...snapshot, has_risk_report: hasReport }
            } catch {
              return { ...snapshot, has_risk_report: false }
            }
          })
        )
        
        setSnapshots(snapshotsWithReports)
      } catch (err) {
        setError('Unable to load your snapshots. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    fetchSnapshots()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    setComparisonError('')

    if (!snapshotA || !snapshotB) {
      setComparisonError('Please select both snapshots to compare.')
      return
    }

    if (snapshotA === snapshotB) {
      setComparisonError('Please select different snapshots to compare.')
      return
    }

    // Check if selected snapshots have risk reports
    const snapshotAData = snapshots.find(s => s.id === parseInt(snapshotA))
    const snapshotBData = snapshots.find(s => s.id === parseInt(snapshotB))
    
    if (!snapshotAData?.has_risk_report || !snapshotBData?.has_risk_report) {
      setComparisonError(
        'Both snapshots must have risk reports to compare. Please generate risk reports for the snapshots first.'
      )
      return
    }

    setComparing(true)
    setComparisonResult(null)

    try {
      const response = await comparisonsApi.createComparison({
        snapshot_a: snapshotA,
        snapshot_b: snapshotB,
        filter_focus: filterFocus,
      })
      setComparisonResult(response.data)
    } catch (err) {
      console.error('Comparison error:', err)
      const errorDetail = err.response?.data?.detail || ''
      if (errorDetail.includes('No risk report found')) {
        setComparisonError(
          'One or both snapshots do not have risk reports. Please generate risk reports for both snapshots before comparing them.'
        )
      } else {
        setComparisonError(
          errorDetail || 'Failed to create comparison. Please try again.'
        )
      }
    } finally {
      setComparing(false)
    }
  }

  const handleReset = () => {
    setComparisonResult(null)
    setComparisonError('')
    setSnapshotA('')
    setSnapshotB('')
  }

  if (loading) {
    return (
      <div className="section">
        <LoadingSpinner />
      </div>
    )
  }

  if (error) {
    return (
      <div className="section">
        <ErrorMessage message={error} />
        <div className="mt-6">
          <Link to="/dashboard" className="btn-primary">
            Back to Dashboard
          </Link>
        </div>
      </div>
    )
  }

  const snapshotsWithReports = snapshots.filter(s => s.has_risk_report)
  
  if (snapshotsWithReports.length < 2) {
    return (
      <div className="section">
        <EmptyState
          title="Need at least 2 snapshots with risk reports"
          description={`You have ${snapshots.length} snapshot${snapshots.length !== 1 ? 's' : ''}, but only ${snapshotsWithReports.length} have risk reports. Generate risk reports for at least 2 snapshots to compare them.`}
          actionText="Go to Dashboard"
          actionLink="/dashboard"
        />
      </div>
    )
  }

  return (
    <div className="section animate-fade-in">
      <div className="mb-8">
        <p className="text-sm font-semibold uppercase tracking-[0.24em] animate-text-shimmer">Compare</p>
        <h1 className="mt-3 page-title">Compare Snapshots</h1>
        <p className="page-subtitle">
          Compare two of your business snapshots to see which has lower risk based on different categories.
        </p>
      </div>

      <div className="grid gap-8 lg:grid-cols-2">
        <div className="card">
          <h2 className="text-2xl font-semibold text-slate-950">Select Snapshots</h2>
          <p className="mt-1 text-sm text-slate-500">Choose two snapshots to compare their risk profiles.</p>

          <form onSubmit={handleSubmit} className="mt-6 space-y-6">
            <div>
              <label htmlFor="snapshotA" className="block text-sm font-medium text-slate-700">
                Snapshot A
              </label>
              <select
                id="snapshotA"
                value={snapshotA}
                onChange={(e) => setSnapshotA(e.target.value)}
                className="mt-2 block w-full input-field"
                required
              >
                <option value="">Select first snapshot</option>
                {snapshots.map((snapshot) => (
                  <option 
                    key={snapshot.id} 
                    value={snapshot.id}
                    disabled={!snapshot.has_risk_report}
                    className={!snapshot.has_risk_report ? 'text-slate-400' : ''}
                  >
                    {snapshot.title} {!snapshot.has_risk_report ? '(No report)' : '✓'}
                  </option>
                ))}
              </select>
              {!snapshotA || !snapshots.find(s => s.id === parseInt(snapshotA))?.has_risk_report ? (
                <p className="mt-1 text-xs text-slate-500">Only snapshots with risk reports can be compared</p>
              ) : null}
            </div>

            <div>
              <label htmlFor="snapshotB" className="block text-sm font-medium text-slate-700">
                Snapshot B
              </label>
              <select
                id="snapshotB"
                value={snapshotB}
                onChange={(e) => setSnapshotB(e.target.value)}
                className="mt-2 block w-full input-field"
                required
              >
                <option value="">Select second snapshot</option>
                {snapshots.map((snapshot) => (
                  <option 
                    key={snapshot.id} 
                    value={snapshot.id}
                    disabled={!snapshot.has_risk_report}
                    className={!snapshot.has_risk_report ? 'text-slate-400' : ''}
                  >
                    {snapshot.title} {!snapshot.has_risk_report ? '(No report)' : '✓'}
                  </option>
                ))}
              </select>
              {!snapshotB || !snapshots.find(s => s.id === parseInt(snapshotB))?.has_risk_report ? (
                <p className="mt-1 text-xs text-slate-500">Only snapshots with risk reports can be compared</p>
              ) : null}
            </div>

            <div>
              <label htmlFor="filterFocus" className="block text-sm font-medium text-slate-700">
                Filter Focus
              </label>
              <select
                id="filterFocus"
                value={filterFocus}
                onChange={(e) => setFilterFocus(e.target.value)}
                className="mt-2 block w-full input-field"
              >
                {FILTER_FOCUS_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>

            {comparisonError && (
              <ErrorMessage message={comparisonError} onDismiss={() => setComparisonError('')} />
            )}

            <button
              type="submit"
              disabled={comparing}
              className="btn-primary w-full"
            >
              {comparing ? 'Comparing...' : 'Compare Snapshots'}
            </button>
          </form>
        </div>

        <div className="card">
          <h2 className="text-2xl font-semibold text-slate-950">Comparison Results</h2>
          <p className="mt-1 text-sm text-slate-500">View the comparison results here.</p>

          {comparing ? (
            <div className="mt-6 flex items-center justify-center py-12">
              <LoadingSpinner />
            </div>
          ) : comparisonResult ? (
            <div className="mt-6 space-y-6">
              <div className="card-dark">
                <h3 className="text-lg font-semibold">Winner</h3>
                <p className="mt-2 text-3xl font-bold">
                  {comparisonResult.winner_snapshot_title || 'Tie'}
                </p>
                <p className="mt-2 text-sm text-slate-300">
                  Based on {comparisonResult.filter_focus} risk analysis
                </p>
              </div>

              <div className="grid gap-4 sm:grid-cols-2">
                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <h4 className="text-sm font-semibold text-slate-700">Snapshot A</h4>
                  <p className="mt-1 text-lg font-semibold text-slate-900">
                    {comparisonResult.snapshot_a_title}
                  </p>
                  <p className="mt-2 text-sm text-slate-600">
                    Risk score: <span className="font-bold text-slate-900">{comparisonResult.snapshot_a_score ?? 'N/A'}</span>
                  </p>
                  <p className="mt-1 text-xs text-slate-500">
                    Based on {comparisonResult.filter_focus} category
                  </p>
                </div>

                <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                  <h4 className="text-sm font-semibold text-slate-700">Snapshot B</h4>
                  <p className="mt-1 text-lg font-semibold text-slate-900">
                    {comparisonResult.snapshot_b_title}
                  </p>
                  <p className="mt-2 text-sm text-slate-600">
                    Risk score: <span className="font-bold text-slate-900">{comparisonResult.snapshot_b_score ?? 'N/A'}</span>
                  </p>
                  <p className="mt-1 text-xs text-slate-500">
                    Based on {comparisonResult.filter_focus} category
                  </p>
                </div>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-slate-50 p-4">
                <h4 className="text-sm font-semibold text-slate-700">Summary</h4>
                <p className="mt-2 text-sm text-slate-600 whitespace-pre-line">
                  {comparisonResult.summary}
                </p>
              </div>

              <button
                onClick={handleReset}
                className="btn-secondary w-full"
              >
                Compare Different Snapshots
              </button>
            </div>
          ) : (
            <div className="mt-6">
              <EmptyState
                icon={
                  <svg
                    className="h-16 w-16 text-slate-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={1.5}
                      d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                    />
                  </svg>
                }
                title="No comparison yet"
                description="Select snapshots and click compare to see results"
              />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
