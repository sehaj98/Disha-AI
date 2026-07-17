const STEPS = [
  {
    n: '01',
    title: 'Tell us about you',
    body: "Studying or dropped out, your class, and what you're drawn to — just say it in your own words.",
  },
  {
    n: '02',
    title: 'We read your direction',
    body: 'Disha maps what you told us against real streams, subjects, and restart paths.',
  },
  {
    n: '03',
    title: 'Get a path forward',
    body: 'One clear recommendation to act on today, not a list of everything you could possibly do.',
  },
]

function HowItWorks() {
  return (
    <section className="how">
      <div className="how__inner">
        {STEPS.map((step) => (
          <div className="how__step" key={step.n}>
            <span className="how__n">{step.n}</span>
            <h3 className="how__title">{step.title}</h3>
            <p className="how__body">{step.body}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

export default HowItWorks