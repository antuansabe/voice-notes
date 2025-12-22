const Hero = () => {
  return (
    <div className="hero">
      <div className="hero-content">
        <h1 className="hero-title">🎙️ VoiceNotes.AI</h1>
        <p className="hero-subtitle">
          Tu asistente de voz con inteligencia artificial
        </p>
        
        <div className="hero-features">
          <div className="feature-item">
            <span className="feature-icon">✓</span>
            <span>Transcripciones precisas</span>
          </div>
          <div className="feature-item">
            <span className="feature-icon">✓</span>
            <span>Resúmenes estructurados</span>
          </div>
          <div className="feature-item">
            <span className="feature-icon">✓</span>
            <span>PDFs profesionales</span>
          </div>
          <div className="feature-item">
            <span className="feature-icon">✓</span>
            <span>Borradores de email</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Hero;
