import { useAuth } from '../context/AuthContext'
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const data = [
  { name: 'Jan', risks: 4, assessments: 2 },
  { name: 'Feb', risks: 3, assessments: 2 },
  { name: 'Mar', risks: 2, assessments: 9 },
  { name: 'Apr', risks: 2, assessments: 3 },
  { name: 'May', risks: 2, assessments: 2 },
  { name: 'Jun', risks: 2, assessments: 2 },
]

export default function Dashboard() {
  const { user } = useAuth()

  return (
    <div className="section">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">
          Welcome, {user?.first_name || 'User'}! 👋
        </h1>
        <p className="text-gray-600">Here's your risk assessment overview</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="card">
          <h3 className="text-gray-600 text-sm font-medium mb-2">Total Risks</h3>
          <p className="text-4xl font-bold text-primary">12</p>
        </div>
        <div className="card">
          <h3 className="text-gray-600 text-sm font-medium mb-2">High Priority</h3>
          <p className="text-4xl font-bold text-danger">3</p>
        </div>
        <div className="card">
          <h3 className="text-gray-600 text-sm font-medium mb-2">Assessments Done</h3>
          <p className="text-4xl font-bold text-secondary">8</p>
        </div>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Risk Trends</h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="risks" stroke="#ef4444" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-6">Assessments Overview</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="assessments" fill="#10b981" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Placeholder for recent risks */}
      <div className="card mt-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Risks</h2>
        <p className="text-gray-500">Risk data will appear here once integrated with the backend.</p>
      </div>
    </div>
  )
}
