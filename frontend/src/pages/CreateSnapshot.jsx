import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import industriesApi from '../api/industriesApi'
import regionsApi from '../api/regionsApi'
import snapshotsApi from '../api/snapshotsApi'
import LoadingSpinner from '../components/LoadingSpinner'

const businessStages = [
  { value: 'idea', label: 'Idea' },
  { value: 'startup', label: 'Startup' },
  { value: 'existing_business', label: 'Existing Business' },
  { value: 'pivot', label: 'Pivot' },
  { value: 'expansion', label: 'Expansion' },
]

const businessSizes = [
  { value: 'micro', label: 'Micro' },
  { value: 'small', label: 'Small' },
  { value: 'medium', label: 'Medium' },
]

export default function CreateSnapshot() {
  const navigate = useNavigate()
  const [regions, setRegions] = useState([])
  const [industries, setIndustries] = useState([])
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    industry: '',
    region: '',
    business_stage: 'idea',
    startup_budget: '',
    currency: 'USD',
    target_customer: '',
    business_size: 'micro',
    has_physical_location: false,
  })

  useEffect(() => {
    const loadOptions = async () => {
      try {
        const [regionsResponse, industriesResponse] = await Promise.all([
          regionsApi.getRegions(),
          industriesApi.getIndustries(),
        ])
        const regionsData = Array.isArray(regionsResponse.data) 
          ? regionsResponse.data 
          : regionsResponse.data.results || []
        const industriesData = Array.isArray(industriesResponse.data) 
          ? industriesResponse.data 
          : industriesResponse.data.results || []
        setRegions(regionsData)
        setIndustries(industriesData)
      } catch (err) {
        setError('Unable to load industries and regions. Please refresh.')
      } finally {
        setLoading(false)
      }
    }

    loadOptions()
  }, [])

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setSaving(true)

    const payload = {
      ...formData,
      startup_budget: formData.startup_budget ? Number(formData.startup_budget) : null,
    }

    try {
      await snapshotsApi.createSnapshot(payload)
      navigate('/dashboard')
    } catch (err) {
      const apiError = err.response?.data
      if (!apiError) {
        setError('Something went wrong while saving your snapshot.')
      } else if (typeof apiError === 'string') {
        setError(apiError)
      } else {
        const firstError = Object.values(apiError)[0]
        setError(Array.isArray(firstError) ? firstError[0] : firstError || 'Please fix the highlighted fields.')
      }
    } finally {
      setSaving(false)
    }
  }

  if (loading) return <LoadingSpinner />

  return (
    <div className="section">
      <div className="grid gap-8 xl:grid-cols-[1.05fr_0.95fr]">
        <div className="space-y-6">
          <div className="rounded-[2rem] border border-slate-200 bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 p-8 text-white shadow-2xl">
            <span className="inline-flex rounded-full bg-white/10 px-4 py-2 text-xs uppercase tracking-[0.25em] text-slate-200">
              Snapshot Studio
            </span>
            <h1 className="mt-6 text-4xl font-semibold tracking-tight">Build a future-ready business snapshot</h1>
            <p className="mt-4 max-w-2xl text-slate-300 leading-7">
              Capture the most important details of your strategy in one enriched snapshot. Use your industry, region, and funding assumptions to unlock better risk insights over time.
            </p>
            <div className="mt-8 grid gap-4 sm:grid-cols-2">
              <div className="rounded-3xl bg-white/5 p-5 ring-1 ring-white/10">
                <p className="text-sm uppercase tracking-[0.2em] text-slate-400">Why snapshots</p>
                <p className="mt-2 text-lg font-semibold text-white">Track your decisions with context</p>
              </div>
              <div className="rounded-3xl bg-white/5 p-5 ring-1 ring-white/10">
                <p className="text-sm uppercase tracking-[0.2em] text-slate-400">What you’ll get</p>
                <p className="mt-2 text-lg font-semibold text-white">Historical view of your business priorities</p>
              </div>
            </div>
            <div className="mt-8 flex flex-col gap-3 text-sm text-slate-300">
              <div className="flex items-center gap-3">
                <span className="h-2 w-2 rounded-full bg-secondary" />
                <span>Preload all industry and region options.</span>
              </div>
              <div className="flex items-center gap-3">
                <span className="h-2 w-2 rounded-full bg-secondary" />
                <span>Submit quickly and revisit your snapshot later.</span>
              </div>
            </div>
          </div>

          <div className="rounded-[2rem] border border-slate-200 bg-white p-8 shadow-xl">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-2xl font-semibold text-slate-900">Snapshot details</h2>
                <p className="text-sm text-slate-500">Fill in the essentials to save your business profile.</p>
              </div>
              <Link to="/dashboard" className="btn-outline inline-flex items-center justify-center">
                Back to dashboard
              </Link>
            </div>

            {error && (
              <div className="mt-6 rounded-3xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="mt-8 grid gap-6">
              <div className="grid gap-6 sm:grid-cols-2">
                <label className="space-y-2">
                  <span className="text-sm font-medium text-slate-700">Snapshot title</span>
                  <input
                    name="title"
                    value={formData.title}
                    onChange={handleChange}
                    required
                    className="input-field"
                    placeholder="Next-gen marketplace sprint"
                  />
                </label>
                <label className="space-y-2">
                  <span className="text-sm font-medium text-slate-700">Currency</span>
                  <input
                    name="currency"
                    value={formData.currency}
                    onChange={handleChange}
                    className="input-field"
                    placeholder="USD"
                  />
                </label>
              </div>

              <label className="space-y-2">
                <span className="text-sm font-medium text-slate-700">Description</span>
                <textarea
                  name="description"
                  value={formData.description}
                  onChange={handleChange}
                  rows={4}
                  className="input-field min-h-[140px] resize-none"
                  placeholder="Describe the customer problem, your approach, and business outlook."
                />
              </label>

              <div className="grid gap-6 sm:grid-cols-3">
                <label className="space-y-2">
                  <span className="text-sm font-medium text-slate-700">Industry</span>
                  <select
                    name="industry"
                    value={formData.industry}
                    onChange={handleChange}
                    required
                    className="input-field"
                  >
                    <option value="">Select industry</option>
                    {industries.map((industry) => (
                      <option key={industry.id} value={industry.id}>
                        {industry.name}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="space-y-2">
                  <span className="text-sm font-medium text-slate-700">Region</span>
                  <select
                    name="region"
                    value={formData.region}
                    onChange={handleChange}
                    required
                    className="input-field"
                  >
                    <option value="">Select region</option>
                    {regions.map((region) => (
                      <option key={region.id} value={region.id}>
                        {region.name}
                      </option>
                    ))}
                  </select>
                </label>

                <label className="space-y-2">
                  <span className="text-sm font-medium text-slate-700">Business stage</span>
                  <select
                    name="business_stage"
                    value={formData.business_stage}
                    onChange={handleChange}
                    className="input-field"
                  >
                    {businessStages.map((stage) => (
                      <option key={stage.value} value={stage.value}>
                        {stage.label}
                      </option>
                    ))}
                  </select>
                </label>
              </div>

              <div className="grid gap-6 sm:grid-cols-3">
                <label className="space-y-2">
                  <span className="text-sm font-medium text-slate-700">Startup budget</span>
                  <input
                    name="startup_budget"
                    type="number"
                    step="0.01"
                    value={formData.startup_budget}
                    onChange={handleChange}
                    className="input-field"
                    placeholder="120000"
                  />
                </label>

                <label className="space-y-2">
                  <span className="text-sm font-medium text-slate-700">Target customer</span>
                  <input
                    name="target_customer"
                    value={formData.target_customer}
                    onChange={handleChange}
                    className="input-field"
                    placeholder="SMBs, urban commuters, health-conscious consumers"
                  />
                </label>

                <label className="space-y-2">
                  <span className="text-sm font-medium text-slate-700">Business size</span>
                  <select
                    name="business_size"
                    value={formData.business_size}
                    onChange={handleChange}
                    className="input-field"
                  >
                    {businessSizes.map((size) => (
                      <option key={size.value} value={size.value}>
                        {size.label}
                      </option>
                    ))}
                  </select>
                </label>
              </div>

              <label className="flex items-center gap-3 rounded-3xl border border-slate-200 bg-slate-50 px-4 py-4 text-sm text-slate-700">
                <input
                  type="checkbox"
                  name="has_physical_location"
                  checked={formData.has_physical_location}
                  onChange={handleChange}
                  className="h-5 w-5 rounded border-slate-300 text-primary focus:ring-primary"
                />
                <span>I have a physical business location</span>
              </label>

              <button type="submit" disabled={saving} className="btn-primary inline-flex items-center justify-center">
                {saving ? 'Saving snapshot…' : 'Create snapshot'}
              </button>
            </form>
          </div>
        </div>

        <aside className="space-y-6 rounded-[2rem] border border-slate-200 bg-white p-8 shadow-xl">
          <div className="rounded-3xl bg-gradient-to-br from-primary to-cyan-500 p-6 text-white shadow-inner">
            <h2 className="text-xl font-semibold">Snapshot insight</h2>
            <p className="mt-3 text-sm leading-6 text-white/90">
              The more detail you provide, the richer the snapshot can become. This page captures your current business assumptions in a format that is ready for analysis.
            </p>
          </div>

          <div className="grid gap-4">
            <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
              <h3 className="text-sm font-semibold text-slate-900">Industry-driven context</h3>
              <p className="mt-2 text-sm text-slate-600">Pick the best industry match to align your snapshot with relevant market signals.</p>
            </div>
            <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
              <h3 className="text-sm font-semibold text-slate-900">Regional accuracy</h3>
              <p className="mt-2 text-sm text-slate-600">Regions help the system understand local regulations, demand, and risk exposure.</p>
            </div>
            <div className="rounded-3xl border border-slate-200 bg-slate-50 p-5">
              <h3 className="text-sm font-semibold text-slate-900">Operational clarity</h3>
              <p className="mt-2 text-sm text-slate-600">Include your business size, budget and whether you operate from a physical location.</p>
            </div>
          </div>
        </aside>
      </div>
    </div>
  )
}
