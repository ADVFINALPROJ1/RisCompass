import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer } from 'recharts'

export default function RiskRadarChart({ riskData }) {
  const data = [
    { subject: 'Financial', value: riskData.financial_risk || 0, fullMark: 100 },
    { subject: 'Market', value: riskData.market_risk || 0, fullMark: 100 },
    { subject: 'Legal', value: riskData.legal_risk || 0, fullMark: 100 },
    { subject: 'Cultural', value: riskData.cultural_risk || 0, fullMark: 100 },
    { subject: 'Operational', value: riskData.operational_risk || 0, fullMark: 100 },
  ]

  const getRiskLevelColor = (score) => {
    if (score < 20) return '#16a34a'
    if (score < 40) return '#65a30d'
    if (score < 60) return '#ca8a04'
    if (score < 80) return '#ea580c'
    return '#dc2626'
  }

  const overallColor = getRiskLevelColor(riskData.overall_risk_score || 0)

  return (
    <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-xl">
      <h2 className="text-2xl font-semibold text-slate-950">Risk Categories Overview</h2>
      <div className="mt-6">
        <ResponsiveContainer width="100%" height={400}>
          <RadarChart data={data}>
            <PolarGrid stroke="#e2e8f0" />
            <PolarAngleAxis
              dataKey="subject"
              tick={{ fill: '#64748b', fontSize: 12, fontWeight: 500 }}
            />
            <PolarRadiusAxis
              angle={90}
              domain={[0, 100]}
              tick={{ fill: '#94a3b8', fontSize: 10 }}
              tickCount={6}
            />
            <Radar
              name="Risk Score"
              dataKey="value"
              stroke={overallColor}
              fill={overallColor}
              fillOpacity={0.3}
              strokeWidth={2}
            />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Risk Category Cards */}
      <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {data.map((item) => {
          const color = getRiskLevelColor(item.value)
          const getRiskLevelLabel = (score) => {
            if (score < 20) return 'Very Low'
            if (score < 40) return 'Low'
            if (score < 60) return 'Medium'
            if (score < 80) return 'High'
            return 'Very High'
          }
          return (
            <div key={item.subject} className="rounded-2xl bg-slate-50 p-4">
              <div className="text-xs uppercase tracking-[0.2em] text-slate-400">{item.subject} Risk</div>
              <div className="mt-2 flex items-center justify-between">
                <div className="text-2xl font-bold text-slate-900">{item.value}/100</div>
                <div
                  className="rounded-full px-3 py-1 text-xs font-semibold text-white"
                  style={{ backgroundColor: color }}
                >
                  {getRiskLevelLabel(item.value)}
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
