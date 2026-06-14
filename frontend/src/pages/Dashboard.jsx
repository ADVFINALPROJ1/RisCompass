import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import snapshotsApi from '../api/snapshotsApi'
import SnapshotCard from '../components/SnapshotCard'
import LoadingSpinner from '../components/LoadingSpinner'

export default function Dashboard() {
  const { user } = useAuth()
  const [snapshots, setSnapshots] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    const fetchSnapshots = async () => {
      try {
        const response = await snapshotsApi.getSnapshots()
        setSnapshots(response.data)
      } catch (err) {
        setError('Unable to load your snapshots. Please try again.')
      } finally {
        setLoading(false)
      }
    }

    fetchSnapshots()
  }, [])

  return (
    <div className="section">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.24em] text-primary">Snapshots</p>
          <h1 className="mt-3 text-4xl font-semibold text-slate-950">Your latest business snapshots</h1>
          <p className="mt-2 max-w-2xl text-sm text-slate-600">
            Track your assessments with context. Create a new snapshot when your plan or market signals shift.
          </p>
        </div>
        <Link to="/create-snapshot" className="btn-secondary inline-flex items-center justify-center px-6 py-3">
          + New snapshot
        </Link>
      </div>

      <div className="mt-10 grid gap-8 lg:grid-cols-3">
        <div className="rounded-[2rem] border border-slate-200 bg-gradient-to-br from-slate-900 to-slate-950 p-8 text-white shadow-2xl">
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
              <p className="mt-1 text-slate-200">{snapshots.length}</p>
            </div>
          </div>
        </div>

        <div className="lg:col-span-2">
          <div className="rounded-[2rem] border border-slate-200 bg-white p-6 shadow-xl">
            <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h2 className="text-2xl font-semibold text-slate-950">Saved snapshots</h2>
                <p className="mt-1 text-sm text-slate-500">Review your active business scenarios and latest updates.</p>
              </div>
              <div className="text-sm text-slate-500">{snapshots.length} snapshots</div>
            </div>

            {loading ? (
              <div className="mt-10">
                <LoadingSpinner />
              </div>
            ) : error ? (
              <div className="mt-8 rounded-3xl border border-red-200 bg-red-50 p-5 text-sm text-red-700">
                {error}
              </div>
            ) : snapshots.length === 0 ? (
              <div className="mt-8 rounded-3xl border border-dashed border-slate-300 bg-slate-50 p-8 text-center text-slate-600">
                <p className="text-lg font-semibold text-slate-900">No snapshots yet</p>
                <p className="mt-2">Create your first snapshot to begin tracking business changes.</p>
                <Link to="/create-snapshot" className="btn-primary mt-6 inline-flex items-center justify-center">
                  Create your first snapshot
                </Link>
              </div>
            ) : (
              <div className="mt-8 grid gap-6 md:grid-cols-2 xl:grid-cols-3">
                {snapshots.map((snapshot) => (
                  <SnapshotCard key={snapshot.id} snapshot={snapshot} />
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
