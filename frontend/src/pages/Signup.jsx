import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

// Matches the keyword list backend/nodes/profile_node.py already looks for,
// so a profile filled in here lines up with what the chat graph understands.
const INTEREST_OPTIONS = [
  'coding',
  'computer',
  'biology',
  'business',
  'math',
  'physics',
  'chemistry',
  'design',
  'art',
]

function Signup() {
  const { signup } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({
    name: '',
    email: '',
    password: '',
    current_class: '',
    country: '',
  })
  const [interests, setInterests] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  function update(field, value) {
    setForm((f) => ({ ...f, [field]: value }))
  }

  function toggleInterest(word) {
    setInterests((prev) =>
      prev.includes(word) ? prev.filter((i) => i !== word) : [...prev, word]
    )
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await signup({
        ...form,
        current_class: form.current_class ? Number(form.current_class) : null,
        interests,
      })
      navigate('/dashboard')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="auth">
      <form className="auth__card" onSubmit={handleSubmit}>
        <p className="eyebrow auth__eyebrow">Get started</p>
        <h1 className="auth__title">Create your Disha account</h1>

        {error && <p className="auth__error">{error}</p>}

        <label className="auth__field">
          <span>Name</span>
          <input value={form.name} onChange={(e) => update('name', e.target.value)} required />
        </label>

        <label className="auth__field">
          <span>Email</span>
          <input
            type="email"
            value={form.email}
            onChange={(e) => update('email', e.target.value)}
            required
          />
        </label>

        <label className="auth__field">
          <span>Password</span>
          <input
            type="password"
            value={form.password}
            onChange={(e) => update('password', e.target.value)}
            required
            minLength={6}
          />
        </label>

        <div className="auth__row">
          <label className="auth__field">
            <span>Class (optional)</span>
            <input
              type="number"
              min="1"
              max="12"
              value={form.current_class}
              onChange={(e) => update('current_class', e.target.value)}
            />
          </label>

          <label className="auth__field">
            <span>Country (optional)</span>
            <input value={form.country} onChange={(e) => update('country', e.target.value)} />
          </label>
        </div>

        <div className="auth__field">
          <span>Interests (optional)</span>
          <div className="auth__chips">
            {INTEREST_OPTIONS.map((word) => (
              <button
                type="button"
                key={word}
                className={`auth__chip ${interests.includes(word) ? 'auth__chip--active' : ''}`}
                onClick={() => toggleInterest(word)}
              >
                {word}
              </button>
            ))}
          </div>
        </div>

        <button className="auth__submit" type="submit" disabled={loading}>
          {loading ? 'Creating account…' : 'Create account'}
        </button>

        <p className="auth__switch">
          Already have an account? <Link to="/login">Log in</Link>
        </p>
      </form>
    </section>
  )
}

export default Signup
