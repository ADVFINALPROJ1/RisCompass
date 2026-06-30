import { useState } from 'react'
import { Link } from 'react-router-dom'
import snapshotsApi from '../api/snapshotsApi'

export default function SnapshotCard({ snapshot, onDelete }) {
  const [expanded, setExpanded] = useState(false)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false)
  const [deleting, setDeleting] = useState(false)

  const toggleExpanded = () => setExpanded((value) => !value)

  const handleKeyDown = (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault()
      toggleExpanded()
    }
  }

  const handleDelete = async (e) => {
    e.stopPropagation()
    setShowDeleteConfirm(true)
  }

  const confirmDelete = async () => {
    setDeleting(true)
    try {
      await snapshotsApi.deleteSnapshot(snapshot.id)
      setShowDeleteConfirm(false)
      if (onDelete) {
        onDelete(snapshot.id)
      }
    } catch (err) {
      console.error('Failed to delete snapshot:', err)
      alert('Failed to delete snapshot. Please try again.')
    } finally {
      setDeleting(false)
    }
  }

  const cancelDelete = () => {
    setShowDeleteConfirm(false)
  }

  return (
    <article
      role="button"
      tabIndex={0}
      onClick={toggleExpanded}
      onKeyDown={handleKeyDown}
      className="group relative overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-xl transition-all hover:-translate-y-1 hover:shadow-2xl focus:outline-none focus:ring-2 focus:ring-primary-500/40"
    >
      <div className="absolute inset-x-0 top-0 h-2 bg-gradient-to-r from-primary-500 via-secondary-500 to-cyan-500" />
      <div className="p-6">
        <div className="flex items-start justify-between gap-3 mb-3">
          <div>
            <h3 className="text-lg font-semibold text-slate-900">{snapshot.title}</h3>
            <p className="text-sm text-slate-500">{new Date(snapshot.created_at).toLocaleDateString()}</p>
          </div>
          <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold uppercase tracking-[0.16em] text-slate-700">
            {snapshot.business_stage?.replace('_', ' ') || 'Unknown'}
          </span>
        </div>

        <p className="text-sm leading-6 text-slate-600 mb-5 line-clamp-3">
          {snapshot.description || 'No description provided yet.'}
        </p>

        <div className="grid gap-3 sm:grid-cols-2">
          <div className="rounded-2xl bg-slate-50 p-4">
            <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Industry</div>
            <div className="mt-2 text-sm font-semibold text-slate-900">
              {snapshot.industry?.name || snapshot.industry_name || snapshot.industry || 'Unknown'}
            </div>
          </div>
          <div className="rounded-2xl bg-slate-50 p-4">
            <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Region</div>
            <div className="mt-2 text-sm font-semibold text-slate-900">
              {snapshot.region?.name || snapshot.region_name || snapshot.region || 'Unknown'}
            </div>
          </div>
          <div className="rounded-2xl bg-slate-50 p-4">
            <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Budget</div>
            <div className="mt-2 text-sm font-semibold text-slate-900">
              {snapshot.startup_budget ? `${snapshot.currency || '$'}${snapshot.startup_budget}` : 'Not specified'}
            </div>
          </div>
          <div className="rounded-2xl bg-slate-50 p-4">
            <div className="text-xs uppercase tracking-[0.2em] text-slate-400">Physical</div>
            <div className="mt-2 text-sm font-semibold text-slate-900">
              {snapshot.has_physical_location ? 'Yes' : 'No'}
            </div>
          </div>
        </div>

        <div className="mt-6 flex flex-col gap-3">
          <Link
            to={`/snapshots/${snapshot.id}`}
            onClick={(e) => e.stopPropagation()}
            className="btn-primary text-sm"
          >
            View Full Details
          </Link>
          {snapshot.interview_session && (
            snapshot.interview_session.status === 'completed' ? (
              <Link
                to={`/reports/${snapshot.interview_session.risk_report_id}`}
                onClick={(e) => e.stopPropagation()}
                className="btn-secondary text-sm"
              >
                View Interview Report
              </Link>
            ) : (
              <Link
                to={`/interviews/${snapshot.interview_session.id}`}
                onClick={(e) => e.stopPropagation()}
                className={`btn-primary text-sm ${
                  snapshot.interview_session.status === 'in_progress'
                    ? 'bg-amber-500 hover:bg-amber-600'
                    : 'bg-purple-500 hover:bg-purple-600'
                }`}
              >
                {snapshot.interview_session.status === 'in_progress'
                  ? 'Continue Interview'
                  : 'Start Interview'}
              </Link>
            )
          )}
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation()
              toggleExpanded()
            }}
            className="btn-outline text-sm"
          >
            {expanded ? 'Hide details' : 'View details'}
          </button>
          <button
            type="button"
            onClick={handleDelete}
            disabled={deleting}
            className="btn-danger text-sm"
          >
            {deleting ? 'Deleting...' : 'Delete'}
          </button>
          <p className="text-xs text-slate-400">Click the card or button to reveal more information.</p>
        </div>

        {expanded && (
          <div className="mt-6 space-y-4 rounded-3xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-700">
            <div>
              <span className="font-semibold text-slate-900">Customer profile:</span> {snapshot.target_customer || 'N/A'}
            </div>
            <div>
              <span className="font-semibold text-slate-900">Business size:</span> {snapshot.business_size?.replace('_', ' ') || 'N/A'}
            </div>
            <div>
              <span className="font-semibold text-slate-900">Created:</span> {new Date(snapshot.created_at).toLocaleString()}
            </div>
          </div>
        )}

        {showDeleteConfirm && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
            <div className="max-w-md card">
              <h3 className="text-xl font-semibold text-slate-900 mb-4">Delete Snapshot</h3>
              <p className="text-slate-600 mb-6">
                Are you sure you want to delete "{snapshot.title}"? This action cannot be undone.
              </p>
              <div className="flex gap-3 justify-end">
                <button
                  onClick={cancelDelete}
                  disabled={deleting}
                  className="btn-ghost"
                >
                  Cancel
                </button>
                <button
                  onClick={confirmDelete}
                  disabled={deleting}
                  className="btn-danger"
                >
                  {deleting ? 'Deleting...' : 'Delete'}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </article>
  )
}
