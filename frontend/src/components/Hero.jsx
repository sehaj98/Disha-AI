function Hero() {
  return (
    <section className="hero">
      <div className="hero__inner">
        <p className="eyebrow hero__eyebrow">For students figuring out what's next</p>
        <h1 className="hero__title">
          Find your <span className="hero__title-em">Disha.</span>
        </h1>
        <p className="hero__sub">
          Disha means direction. Tell us where you're standing — still in
          school or already out of it — and we'll help you see a real path
          forward, in one conversation.
        </p>
        <a className="hero__cta" href="#talk">
          Start the conversation
          <span aria-hidden="true">→</span>
        </a>
      </div>
    </section>
  )
}

export default Hero