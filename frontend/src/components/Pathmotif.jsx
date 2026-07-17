import { useEffect, useRef, useState } from 'react'

/**
 * The signature element: a single hand-drawn path with three waypoints,
 * running from the hero through "How it works". It draws itself in once
 * on load (respecting reduced-motion), rather than looping or animating
 * on every scroll — one deliberate moment, not ambient decoration.
 */
function PathMotif({ waypoints }) {
  const pathRef = useRef(null)
  const [drawn, setDrawn] = useState(false)

  useEffect(() => {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (reduceMotion) {
      setDrawn(true)
      return
    }
    const t = setTimeout(() => setDrawn(true), 200)
    return () => clearTimeout(t)
  }, [])

  return (
    <svg
      className="path-motif"
      viewBox="0 0 1120 640"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      preserveAspectRatio="none"
      aria-hidden="true"
    >
      <path
        ref={pathRef}
        className={`path-motif__line ${drawn ? 'path-motif__line--drawn' : ''}`}
        d="M -20 120 C 180 60, 300 220, 480 180 S 760 60, 900 200 S 1040 420, 1140 460"
        stroke="url(#pathGradient)"
        strokeWidth="2.5"
        strokeDasharray="1 12"
        strokeLinecap="round"
      />
      <defs>
        <linearGradient id="pathGradient" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stopColor="#f2a93b" stopOpacity="0.9" />
          <stop offset="55%" stopColor="#f2a93b" stopOpacity="0.5" />
          <stop offset="100%" stopColor="#2f8f7a" stopOpacity="0.6" />
        </linearGradient>
      </defs>

      {waypoints?.map((wp, i) => (
        <g
          key={wp.label}
          className={`path-motif__waypoint ${drawn ? 'path-motif__waypoint--in' : ''}`}
          style={{ transitionDelay: `${600 + i * 260}ms` }}
        >
          <circle cx={wp.x} cy={wp.y} r="15" fill="var(--paper)" stroke="var(--marigold)" strokeWidth="1.5" />
          <circle cx={wp.x} cy={wp.y} r="4.5" fill="var(--marigold)" />
        </g>
      ))}
    </svg>
  )
}

export default PathMotif