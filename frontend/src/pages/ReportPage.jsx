import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import reportsApi from '../api/reportsApi'
import LoadingSpinner from '../components/LoadingSpinner'
import RiskScoreCard from '../components/RiskScoreCard'
import ConfidenceGauge from '../components/ConfidenceGauge'
import RiskRadarChart from '../components/RiskRadarChart'
import RiskFactorList from '../components/RiskFactorList'

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
        <RiskScoreCard
          score={report.overall_risk_score}
          title="Risk Report"
          snapshotTitle={report.snapshot_title}
          createdAt={report.created_at}
        />

        {/* Confidence Score */}
        <ConfidenceGauge
          score={report.confidence_score}
          label={report.confidence_label}
        />

        {/* Risk Categories */}
        <RiskRadarChart
          riskData={{
            overall_risk_score: report.overall_risk_score,
            financial_risk: report.financial_risk,
            market_risk: report.market_risk,
            legal_risk: report.legal_risk,
            cultural_risk: report.cultural_risk,
            operational_risk: report.operational_risk,
          }}
        />

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
        <RiskFactorList riskFactors={report.risk_factors} />

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
