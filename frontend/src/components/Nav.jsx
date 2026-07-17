import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

function Nav() {
  const { student, logout } = useAuth()

  return (
    <header className="nav">
      <div className="nav__inner">
        <Link to="/" className="nav__mark">
          Disha <span className="nav__mark-accent">AI</span>
        </Link>

        {student ? (
          <div className="nav__user">
            <span className="nav__user-name">Hi, {student.name?.split(' ')[0] || 'there'}</span>
            <button className="nav__cta" onClick={logout} type="button">
              Log out
            </button>
          </div>
        ) : (
          <div className="nav__user">
            <Link className="nav__link" to="/login">
              Log in
            </Link>
            <Link className="nav__cta" to="/signup">
              Sign up
            </Link>
          </div>
        )}
      </div>
    </header>
  )
}

export default Nav
