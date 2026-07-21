import { Routes, Route } from 'react-router-dom'
import Nav from './components/Nav'
import Hero from './components/Hero'
import HowItWorks from './components/HowItWorks'
import PathMotif from './components/PathMotif'
import ChatWidget from './components/ChatWidget'
import Footer from './components/Footer'
import Login from './pages/Login'
import Signup from './pages/Signup'
import Dashboard from './pages/Dashboard'
import './App.css'

const WAYPOINTS = [
  { label: 'start', x: 210, y: 145 },
  { label: 'read', x: 610, y: 195 },
  { label: 'path', x: 990, y: 330 },
]

function Home() {
  return (
    <>
      <div className="journey">
        <PathMotif waypoints={WAYPOINTS} />
        <Hero />
        <HowItWorks />
      </div>
      <ChatWidget />
    </>
  )
}

function App() {
  return (
    <>
      <Nav />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
      <Footer />
    </>
  )
}

export default App
