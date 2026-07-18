import { useCallback, useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import { API_URL } from '../api'
import { useAuth } from '../context/AuthContext'
import ChatWidget from '../components/ChatWidget'

function Dashboard() {
  const { token, student, loading: authLoading } = useAuth()
  const [digest, setDigest] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const fetchUpdates = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const res = await fetch(`${API_URL}/updates`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (!res.ok) throw new Error('Could not load your updates right now.')
      const data = await res.json()
      setDigest(data.digest)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [token])

  useEffect(() => {
    if (token) fetchUpdates()
  }, [token, fetchUpdates])

  // Not logged in and we're done checking -> bounce to login.
  if (!authLoading && !token) {
    return <Navigate to="/login" replace />
  }

  return (
    <>
      <section className="dashboard">
        <div className="dashboard__intro">
          <p className="eyebrow dashboard__eyebrow">Your direction, updated</p>
          <h1 className="dashboard__title">
            {student ? `Here's what's new for you, ${student.name?.split(' ')[0] || ''}` : 'Your updates'}
          </h1>
          <p className="dashboard__sub">
            {student?.current_class
              ? `Based on class ${student.current_class}${student.interests?.length ? ` and your interest in ${student.interests.join(', ')}` : ''}.`
              : 'Complete your profile for more specific updates.'}
          </p>
        </div>

        <div className="dashboard__card">
          {loading && <p className="dashboard__loading">Looking up what's new for you…</p>}

          {!loading && error && (
            <p className="dashboard__error">{error}</p>
          )}

          {!loading && !error && (
            <p className="dashboard__digest">{digest}</p>
          )}

          <button
            className="dashboard__refresh"
            type="button"
            onClick={fetchUpdates}
            disabled={loading}
          >
            {loading ? 'Refreshing…' : 'Refresh my updates'}
          </button>
        </div>
      </section>

      <ChatWidget />
    </>
  )
}

export default Dashboard
