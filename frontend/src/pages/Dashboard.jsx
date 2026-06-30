import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import snapshotsApi from '../api/snapshotsApi'
import SnapshotCard from '../components/SnapshotCard'
import LoadingSpinner from '../components/LoadingSpinner'
import EmptyState from '../components/EmptyState'
import ErrorMessage from '../components/ErrorMessage'

export default function Dashboard() {
  const { user } = useAuth()
  const [snapshots, setSnapshots] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchSnapshots = async () => {
      try {
        const response = await snapshotsApi.getSnapshots()
        const snapshotsData = Array.isArray(response.data) 
          ? response.data 
          : response.data.results || []
        setSnapshots(snapshotsData)
      } catch (err) {
        setError('Unable to load your snapshots. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    fetchSnapshots()
  }, [])

  const handleDelete = (deletedId) => {
    setSnapshots((prevSnapshots) => prevSnapshots.filter((snapshot) => snapshot.id !== deletedId))
  }

  return (
    <div className="section animate-fade-in">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.24em] animate-text-shimmer">Snapshots</p>
          <h1 className="mt-3 page-title">Your latest business snapshots</h1>
          <p className="page-subtitle">
            Track your assessments with context. Create a new snapshot when your plan or market signals shift.
          </p>
        </div>
        <Link to="/create-snapshot" className="btn-primary inline-flex items-center justify-center px-6 py-3">
          <svg className="mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
          </svg>
          New snapshot
        </Link>
      </div>

      <div className="mt-10 grid gap-8 lg:grid-cols-3">
        <div className="card-dark">
          <p className="text-sm uppercase tracking-[0.24em] text-slate-300">Overview</p>
          <h2 className="mt-4 text-3xl font-semibold">{user?.first_name || 'Your'} snapshot history</h2>
          <p className="mt-4 text-sm leading-7 text-slate-300">
            Build momentum by saving strategic details and come back later to compare how risks and priorities evolve.
          </p>
          <div className="mt-8 space-y-3 text-sm text-slate-300">
            <div className="rounded-3xl bg-white/5 p-4">
              <p className="font-semibold">Logged in as</p>
              <p className="mt-1 text-slate-200">{user?.email}</p>
            </div>
            <div className="rounded-3xl bg-white/5 p-4">
              <p className="font-semibold">Snapshot count</p>
              <p className={`mt-1 ${snapshots.length === 0 ? 'text-red-400' : snapshots.length < 3 ? 'text-amber-400' : 'text-green-400'}`}>{snapshots.length}</p>
            </div>
          </div>
        </div>

        <div className="lg:col-span-2">
          <div className="card">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-2xl font-semibold text-slate-950">Saved snapshots</h2>
                <p className="mt-1 text-sm text-slate-500">Review your active business scenarios and latest updates.</p>
              </div>
              <div className="text-sm text-slate-500">{snapshots.length} snapshot{snapshots.length !== 1 ? 's' : ''}</div>
            </div>

            {loading ? (
              <div className="mt-10 flex items-center justify-center py-12">
                <LoadingSpinner />
              </div>
            ) : error ? (
              <div className="mt-8">
                <ErrorMessage message={error} onDismiss={() => setError('')} />
              </div>
            ) : snapshots.length === 0 ? (
              <div className="mt-8">
                <EmptyState
                  title="No snapshots yet."
                  description="Create your first snapshot to begin tracking business changes."
                  actionText="Create your first snapshot"
                  actionLink="/create-snapshot"
                />
              </div>
            ) : (
              <div className="mt-8 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
                {snapshots.map((snapshot, index) => (
                  <div key={snapshot.id} className="animate-slide-up" style={{ animationDelay: `${index * 50}ms` }}>
                    <SnapshotCard snapshot={snapshot} onDelete={handleDelete} />
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
