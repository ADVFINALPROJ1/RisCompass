export default function RiskScoreCard({ score, title, snapshotTitle, createdAt }) {
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

  const getRiskLevelBgColor = (score) => {
    if (score < 20) return 'bg-green-500'
    if (score < 40) return 'bg-lime-500'
    if (score < 60) return 'bg-yellow-500'
    if (score < 80) return 'bg-orange-500'
    return 'bg-red-500'
  }

  return (
    <div className="rounded-[2rem] border border-slate-200 bg-gradient-to-br from-slate-900 to-slate-950 p-8 text-white shadow-2xl">
      <div className="flex flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.24em] text-slate-300">{title}</p>
          <h1 className="mt-3 text-4xl font-semibold">{snapshotTitle || 'Risk Assessment'}</h1>
          {createdAt && (
            <p className="mt-2 text-sm text-slate-300">
              Generated on {new Date(createdAt).toLocaleDateString()}
            </p>
          )}
        </div>
        <div className="text-center sm:text-right">
          <div className="text-sm uppercase tracking-[0.2em] text-slate-300">Overall Risk Score</div>
          <div className="mt-2 text-6xl font-bold">{score}/100</div>
          <div className={`mt-2 inline-block rounded-full px-4 py-2 text-sm font-semibold ${getRiskLevelBgColor(score)}`}>
            {getRiskLevelLabel(score)}
          </div>
        </div>
      </div>
    </div>
  )
}
