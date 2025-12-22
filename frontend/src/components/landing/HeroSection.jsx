const HeroSection = ({ onGetStarted }) => {
  return (
    <section className="hero-section">
      <div className="hero-container">
        <div className="hero-content">
          <h1 className="hero-title">
            Transforma tu voz en
            <span className="hero-highlight"> documentos profesionales</span>
          </h1>
          
          <p className="hero-description">
            Transcripción precisa, resúmenes inteligentes y exportación automática. 
            Todo powered by Azure AI.
          </p>

          <div className="hero-cta">
            <button onClick={onGetStarted} className="cta-primary">
              ▶ Comenzar ahora
            </button>
            <button onClick={() => {
              const demoSection = document.getElementById('features');
              demoSection?.scrollIntoView({ behavior: 'smooth' });
            }} className="cta-secondary">
              📖 Ver más
            </button>
          </div>

          <div className="hero-stats">
            <div className="stat-item">
              <div className="stat-number">95%</div>
              <div className="stat-label">Precisión</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">&lt;3s</div>
              <div className="stat-label">Velocidad</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">50+</div>
              <div className="stat-label">Idiomas</div>
            </div>
          </div>
        </div>

        <div className="hero-visual">
          <div className="floating-card card-1">
            <div className="card-icon">🎤</div>
            <div className="card-text">Transcripción en tiempo real</div>
          </div>
          <div className="floating-card card-2">
            <div className="card-icon">🤖</div>
            <div className="card-text">Resumen con IA</div>
          </div>
          <div className="floating-card card-3">
            <div className="card-icon">📄</div>
            <div className="card-text">PDF profesional</div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
