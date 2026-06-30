import { Link } from 'react-router-dom'

export default function EmptyState({ 
  icon, 
  title, 
  description, 
  actionText, 
  actionLink,
  className = ''
}) {
  return (
    <div className={`rounded-3xl border border-dashed border-slate-300 bg-slate-50 p-8 text-center text-slate-600 ${className}`}>
      {icon && (
        <div className="mb-4 flex justify-center">
          {icon}
        </div>
      )}
      <p className="text-lg font-semibold text-slate-900">{title}</p>
      <p className="mt-2">{description}</p>
      {actionText && actionLink && (
        <Link to={actionLink} className="btn-primary mt-6 inline-flex items-center justify-center">
          {actionText}
        </Link>
      )}
    </div>
  )
}
