const FeaturesSection = ({ onSelectMode }) => {
  const features = [
    {
      id: 'record',
      icon: '🎤',
      title: 'Graba tu Voz',
      description: 'Captura audio directamente desde tu navegador. Transcripción instantánea con detección automática de idioma.',
      benefits: [
        'Grabación en alta calidad',
        'Detección de 50+ idiomas',
        'Transcripción en tiempo real'
      ],
      cta: 'Comenzar a grabar',
      color: '#ea4335'
    },
    {
      id: 'upload',
      icon: '📁',
      title: 'Sube tus Archivos',
      description: 'Analiza grabaciones existentes. Soporta WAV, MP3, M4A y más formatos de audio populares.',
      benefits: [
        'Drag & drop intuitivo',
        'Múltiples formatos',
        'Procesamiento rápido'
      ],
      cta: 'Subir archivo',
      color: '#34a853'
    },
    {
      id: 'email',
      icon: '📧',
      title: 'Genera Emails',
      description: 'Dicta tus ideas y obtén un borrador de correo profesional listo para enviar.',
      benefits: [
        'Formato automático',
        'Tono profesional',
        'Copy-paste directo'
      ],
      cta: 'Crear email',
      color: '#1a73e8'
    }
  ];

  return (
    <section id="features" className="features-section">
      <div className="section-container">
        <div className="section-header">
          <h2 className="section-title">Elige cómo trabajar</h2>
          <p className="section-subtitle">
            Tres modos diseñados para tu flujo de trabajo
          </p>
        </div>

        <div className="features-grid">
          {features.map((feature) => (
            <div 
              key={feature.id} 
              className="feature-card"
              style={{ '--feature-color': feature.color }}
            >
              <div className="feature-icon-wrapper">
                <span className="feature-icon">{feature.icon}</span>
              </div>
              
              <h3 className="feature-title">{feature.title}</h3>
              <p className="feature-description">{feature.description}</p>

              <ul className="feature-benefits">
                {feature.benefits.map((benefit, index) => (
                  <li key={index} className="benefit-item">
                    <span className="benefit-check">✓</span>
                    {benefit}
                  </li>
                ))}
              </ul>

              <button 
                onClick={() => onSelectMode(feature.id)}
                className="feature-cta"
              >
                {feature.cta} →
              </button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
