export default function LoadingSpinner() {
  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50">
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 bg-gradient-to-r from-primary to-secondary rounded-full animate-spin"></div>
        <div className="absolute inset-1 bg-gray-50 rounded-full"></div>
      </div>
    </div>
  )
}
