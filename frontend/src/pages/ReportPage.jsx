import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import reportsApi from '../api/reportsApi'
import LoadingSpinner from '../components/LoadingSpinner'

export default function ReportPage() {
  const { id } = useParams()
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchReport = async () => {
      try {
        const response = await reportsApi.getReportDetail(id)
        setReport(response.data)
      } catch (err) {
        setError('Unable to load report details. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    fetchReport()
  }, [id])

  const getRiskLevelColor = (score) => {
    if (score < 20) return 'text-green-600 bg-green-50'
    if (score < 40) return 'text-lime-600 bg-lime-50'
    if (score < 60) return 'text-yellow-600 bg-yellow-50'
    if (score < 80) return 'text-orange-600 bg-orange-50'
    return 'text-red-600 bg-red-50'
  }

  const getRiskLevelLabel = (score) => {
    if (score < 20) return 'Very Low'
    if (score < 40) return 'Low'
    if (score < 60) return 'Medium'
    if (score < 80) return 'High'
    return 'Very High'
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

  if (!report) {
    return (
      <div className="section">
        <div className="rounded-3xl border border-slate-200 bg-slate-50 p-8 text-center">
          <p className="text-slate-600">Report not found.</p>
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

      <div className="space-y-8">
        {/* Overall Risk Score */}
        <div className="rounded-[2rem] border border-slate-200 bg-gradient-to-br from-slate-900 to-slate-950 p-8 text-white shadow-2xl">
          <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-300">Risk Report</p>
              <h1 className="mt-3 text-4xl font-semibold">{report.snapshot_title || 'Risk Assessment'}</h1>
              <p className="mt-2 text-sm text-slate-300">
                Generated on {new Date(report.created_at).toLocaleDateString()}
              </p>
            </div>
            <div className="text-center sm:text-right">
              <div className="text-sm uppercase tracking-[0.2em] text-slate-300">Overall Risk Score</div>
              <div className="mt-2 text-6xl font-bold">{report.overall_risk_score}/100</div>
              <div className={`mt-2 inline-block rounded-full px-4 py-2 text-sm font-semibold ${getRiskLevelColor(report.overall_risk_score).replace('text-', 'text-white ').replace('bg-', 'bg-')}`}>
                {getRiskLevelLabel(report.overall_risk_score)}
              </div>
            </div>
          </div>
        </div>

        {/* Confidence Score */}
        <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-xl">
          <h2 className="text-2xl font-semibold text-slate-950">Confidence Assessment</h2>
          <div className="mt-6 grid gap-6 sm:grid-cols-2">
            <div className="rounded-2xl bg-slate-50 p-6">
              <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Confidence Score</div>
              <div className="mt-2 text-3xl font-bold text-slate-900">{report.confidence_score}/100</div>
            </div>
            <div className="rounded-2xl bg-slate-50 p-6">
              <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Confidence Label</div>
              <div className="mt-2 text-3xl font-bold text-slate-900">{report.confidence_label}</div>
            </div>
          </div>
        </div>

        {/* Risk Categories */}
        <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-xl">
          <h2 className="text-2xl font-semibold text-slate-950">Risk Categories</h2>
          <div className="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            <div className="rounded-2xl bg-slate-50 p-6">
              <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Financial Risk</div>
              <div className="mt-2 text-3xl font-bold text-slate-900">{report.financial_risk}/100</div>
              <div className={`mt-2 inline-block rounded-full px-3 py-1 text-xs font-semibold ${getRiskLevelColor(report.financial_risk)}`}>
                {getRiskLevelLabel(report.financial_risk)}
              </div>
            </div>
            <div className="rounded-2xl bg-slate-50 p-6">
              <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Market Risk</div>
              <div className="mt-2 text-3xl font-bold text-slate-900">{report.market_risk}/100</div>
              <div className={`mt-2 inline-block rounded-full px-3 py-1 text-xs font-semibold ${getRiskLevelColor(report.market_risk)}`}>
                {getRiskLevelLabel(report.market_risk)}
              </div>
            </div>
            <div className="rounded-2xl bg-slate-50 p-6">
              <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Legal Risk</div>
              <div className="mt-2 text-3xl font-bold text-slate-900">{report.legal_risk}/100</div>
              <div className={`mt-2 inline-block rounded-full px-3 py-1 text-xs font-semibold ${getRiskLevelColor(report.legal_risk)}`}>
                {getRiskLevelLabel(report.legal_risk)}
              </div>
            </div>
            <div className="rounded-2xl bg-slate-50 p-6">
              <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Cultural Risk</div>
              <div className="mt-2 text-3xl font-bold text-slate-900">{report.cultural_risk}/100</div>
              <div className={`mt-2 inline-block rounded-full px-3 py-1 text-xs font-semibold ${getRiskLevelColor(report.cultural_risk)}`}>
                {getRiskLevelLabel(report.cultural_risk)}
              </div>
            </div>
            <div className="rounded-2xl bg-slate-50 p-6">
              <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Operational Risk</div>
              <div className="mt-2 text-3xl font-bold text-slate-900">{report.operational_risk}/100</div>
              <div className={`mt-2 inline-block rounded-full px-3 py-1 text-xs font-semibold ${getRiskLevelColor(report.operational_risk)}`}>
                {getRiskLevelLabel(report.operational_risk)}
              </div>
            </div>
          </div>
        </div>

        {/* Summary and Recommendation */}
        <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-xl">
          <h2 className="text-2xl font-semibold text-slate-950">Summary & Recommendation</h2>
          <div className="mt-6 space-y-6">
            <div className="rounded-2xl bg-slate-50 p-6">
              <h3 className="text-lg font-semibold text-slate-900">Summary</h3>
              <p className="mt-2 text-slate-600">{report.summary || 'No summary available.'}</p>
            </div>
            <div className="rounded-2xl bg-slate-50 p-6">
              <h3 className="text-lg font-semibold text-slate-900">Recommendation</h3>
              <p className="mt-2 text-slate-600">{report.recommendation || 'No recommendation available.'}</p>
            </div>
          </div>
        </div>

        {/* Risk Factors */}
        {report.risk_factors && report.risk_factors.length > 0 && (
          <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-xl">
            <h2 className="text-2xl font-semibold text-slate-950">Risk Factors</h2>
            <div className="mt-6 space-y-4">
              {report.risk_factors.map((factor) => (
                <div key={factor.id} className="rounded-2xl bg-slate-50 p-6">
                  <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                    <div className="flex-1">
                      <div className="flex items-center gap-3">
                        <span className="rounded-full bg-slate-200 px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] text-slate-700">
                          {factor.category}
                        </span>
                        <h3 className="text-lg font-semibold text-slate-900">{factor.name}</h3>
                      </div>
                      <p className="mt-2 text-sm text-slate-600">{factor.explanation || 'No explanation available.'}</p>
                      <div className="mt-2 text-xs text-slate-400">
                        Source: {factor.source_type?.replace('_', ' ') || 'Unknown'}
                      </div>
                    </div>
                    <div className="text-center sm:text-right">
                      <div className="text-3xl font-bold text-slate-900">{factor.score}/100</div>
                      <div className={`mt-1 inline-block rounded-full px-3 py-1 text-xs font-semibold ${getRiskLevelColor(factor.score)}`}>
                        {getRiskLevelLabel(factor.score)}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Data Sources */}
        {report.data_sources_used && report.data_sources_used.length > 0 && (
          <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-xl">
            <h2 className="text-2xl font-semibold text-slate-950">Data Sources</h2>
            <div className="mt-4 flex flex-wrap gap-2">
              {report.data_sources_used.map((source, index) => (
                <span key={index} className="rounded-full bg-slate-100 px-4 py-2 text-sm text-slate-700">
                  {source}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
