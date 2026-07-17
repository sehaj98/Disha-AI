import Nav from './components/Nav'
import Hero from './components/Hero'
import HowItWorks from './components/HowItWorks'
import PathMotif from './components/PathMotif'
import ChatWidget from './components/ChatWidget'
import Footer from './components/Footer'
import './App.css'

const WAYPOINTS = [
  { label: 'start', x: 210, y: 145 },
  { label: 'read', x: 610, y: 195 },
  { label: 'path', x: 990, y: 330 },
]

function App() {
  return (
    <>
      <Nav />
      <div className="journey">
        <PathMotif waypoints={WAYPOINTS} />
        <Hero />
        <HowItWorks />
      </div>
      <ChatWidget />
      <Footer />
    </>
  )
}

export default App