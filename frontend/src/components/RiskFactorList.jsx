export default function RiskFactorList({ riskFactors }) {
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

  const getCategoryColor = (category) => {
    const colors = {
      financial: 'bg-blue-100 text-blue-700',
      market: 'bg-purple-100 text-purple-700',
      legal: 'bg-red-100 text-red-700',
      cultural: 'bg-pink-100 text-pink-700',
      operational: 'bg-amber-100 text-amber-700',
    }
    return colors[category?.toLowerCase()] || 'bg-slate-100 text-slate-700'
  }

  if (!riskFactors || riskFactors.length === 0) {
    return null
  }

  return (
    <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-xl">
      <h2 className="text-2xl font-semibold text-slate-950">Risk Factors</h2>
      <div className="mt-6 space-y-4">
        {riskFactors.map((factor, index) => (
          <div key={factor.id || index} className="rounded-2xl bg-slate-50 p-6 transition hover:bg-slate-100">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
              <div className="flex-1">
                <div className="flex flex-wrap items-center gap-3">
                  <span
                    className={`rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] ${getCategoryColor(
                      factor.category
                    )}`}
                  >
                    {factor.category || 'General'}
                  </span>
                  <h3 className="text-lg font-semibold text-slate-900">{factor.name || 'Unnamed Risk Factor'}</h3>
                </div>
                {factor.explanation && (
                  <p className="mt-2 text-sm text-slate-600">{factor.explanation}</p>
                )}
                {factor.source_type && (
                  <div className="mt-2 text-xs text-slate-400">
                    Source: {factor.source_type.replace('_', ' ')}
                  </div>
                )}
              </div>
              <div className="flex shrink-0 flex-col items-center gap-2 sm:text-right">
                <div className="text-3xl font-bold text-slate-900">{factor.score || 0}/100</div>
                <div
                  className={`inline-block rounded-full px-3 py-1 text-xs font-semibold ${getRiskLevelColor(
                    factor.score || 0
                  )}`}
                >
                  {getRiskLevelLabel(factor.score || 0)}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
