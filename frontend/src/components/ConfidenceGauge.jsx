export default function ConfidenceGauge({ score, label }) {
  const getConfidenceColor = (score) => {
    if (score < 30) return 'bg-red-500'
    if (score < 50) return 'bg-orange-500'
    if (score < 70) return 'bg-yellow-500'
    if (score < 85) return 'bg-lime-500'
    return 'bg-green-500'
  }

  const getConfidenceTextColor = (score) => {
    if (score < 30) return 'text-red-600'
    if (score < 50) return 'text-orange-600'
    if (score < 70) return 'text-yellow-600'
    if (score < 85) return 'text-lime-600'
    return 'text-green-600'
  }

  return (
    <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-xl">
      <h2 className="text-2xl font-semibold text-slate-950">Confidence Assessment</h2>
      <div className="mt-6 space-y-6">
        {/* Confidence Score with Progress Bar */}
        <div className="rounded-2xl bg-slate-50 p-6">
          <div className="flex items-center justify-between mb-3">
            <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Confidence Score</div>
            <div className={`text-3xl font-bold ${getConfidenceTextColor(score)}`}>{score}/100</div>
          </div>
          <div className="h-4 w-full overflow-hidden rounded-full bg-slate-200">
            <div
              className={`h-full rounded-full transition-all duration-500 ease-out ${getConfidenceColor(score)}`}
              style={{ width: `${score}%` }}
            />
          </div>
        </div>

        {/* Confidence Label */}
        {label && (
          <div className="rounded-2xl bg-slate-50 p-6">
            <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Confidence Label</div>
            <div className="mt-2 text-3xl font-bold text-slate-900">{label}</div>
          </div>
        )}
      </div>
    </div>
  )
}
