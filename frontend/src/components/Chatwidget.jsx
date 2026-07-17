import { useEffect, useRef, useState } from 'react'
import { API_URL } from '../api'
import { useAuth } from '../context/AuthContext'

const STARTERS = [
  "I'm in class 11 in India and I love coding",
  "I'm interested in biology and want to become a doctor",
  'I dropped out of school and want to restart',
]

const INITIAL_MESSAGES = [
  {
    role: 'assistant',
    text:
      "Hi, I'm Disha. Tell me what class you're in, where you're from, and what you enjoy — or tell me if you're not studying right now. I'll help you find your direction.",
  },
]

function ChatWidget() {
  const { token } = useAuth()
  const [messages, setMessages] = useState(INITIAL_MESSAGES)
  const [input, setInput] = useState('')
  const [status, setStatus] = useState('idle') // idle | sending | error
  const threadRef = useRef(null)

  useEffect(() => {
    threadRef.current?.scrollTo({ top: threadRef.current.scrollHeight, behavior: 'smooth' })
  }, [messages, status])

  async function sendMessage(text) {
    const trimmed = text.trim()
    if (!trimmed || status === 'sending') return

    setMessages((prev) => [...prev, { role: 'user', text: trimmed }])
    setInput('')
    setStatus('sending')

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: `Bearer ${token}` } : {}),
        },
        body: JSON.stringify({ message: trimmed }),
      })

      if (!res.ok) throw new Error(`Request failed with ${res.status}`)

      const data = await res.json()
      setMessages((prev) => [...prev, { role: 'assistant', text: data.response }])
      setStatus('idle')
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: "I couldn't reach the guidance service. Make sure the backend is running, then try again.",
          isError: true,
        },
      ])
      setStatus('error')
    }
  }

  function handleSubmit(e) {
    e.preventDefault()
    sendMessage(input)
  }

  return (
    <section className="chat" id="talk">
      <div className="chat__intro">
        <p className="eyebrow chat__eyebrow">Talk to Disha</p>
        <h2 className="chat__title">One honest conversation.</h2>
      </div>

      <div className="chat__card">
        <div className="chat__thread" ref={threadRef}>
          {messages.map((m, i) => (
            <div
              key={i}
              className={`chat__bubble chat__bubble--${m.role}${m.isError ? ' chat__bubble--error' : ''}`}
            >
              {m.text}
            </div>
          ))}
          {status === 'sending' && (
            <div className="chat__bubble chat__bubble--assistant chat__bubble--typing">
              <span className="chat__dot" />
              <span className="chat__dot" />
              <span className="chat__dot" />
            </div>
          )}
        </div>

        {messages.length <= 1 && (
          <div className="chat__starters">
            {STARTERS.map((s) => (
              <button
                type="button"
                key={s}
                className="chat__starter"
                onClick={() => sendMessage(s)}
              >
                {s}
              </button>
            ))}
          </div>
        )}

        <form className="chat__form" onSubmit={handleSubmit}>
          <input
            className="chat__input"
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="I'm in class 12, from India, and I like..."
            aria-label="Message Disha"
          />
          <button
            className="chat__send"
            type="submit"
            disabled={status === 'sending' || !input.trim()}
          >
            Send
          </button>
        </form>
      </div>
    </section>
  )
}

export default ChatWidget
