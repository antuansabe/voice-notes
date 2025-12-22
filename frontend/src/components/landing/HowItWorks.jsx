const HowItWorks = () => {
  const steps = [
    {
      number: '01',
      title: 'Captura',
      description: 'Graba tu voz o sube un archivo de audio',
      icon: '🎙️'
    },
    {
      number: '02',
      title: 'Procesa',
      description: 'Azure AI transcribe y analiza el contenido',
      icon: '🤖'
    },
    {
      number: '03',
      title: 'Exporta',
      description: 'Descarga PDF, copia email o guarda texto',
      icon: '📥'
    }
  ];

  return (
    <section id="how-it-works" className="how-it-works-section">
      <div className="section-container">
        <div className="section-header">
          <h2 className="section-title">Cómo funciona</h2>
          <p className="section-subtitle">
            Tres pasos simples para resultados profesionales
          </p>
        </div>

        <div className="steps-container">
          {steps.map((step, index) => (
            <div key={step.number} className="step-card">
              <div className="step-number">{step.number}</div>
              <div className="step-icon">{step.icon}</div>
              <h3 className="step-title">{step.title}</h3>
              <p className="step-description">{step.description}</p>
              
              {index < steps.length - 1 && (
                <div className="step-connector">→</div>
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
