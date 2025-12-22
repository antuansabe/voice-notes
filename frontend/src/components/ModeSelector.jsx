const ModeSelector = ({ onModeSelect, currentMode }) => {
  const modes = [
    {
      id: 'record',
      icon: '🎤',
      title: 'Grabar Voz',
      description: 'Graba tu voz en tiempo real',
      color: '#ff6b6b'
    },
    {
      id: 'upload',
      icon: '📁',
      title: 'Subir Audio',
      description: 'Arrastra o selecciona un archivo',
      color: '#4ecdc4'
    },
    {
      id: 'email',
      icon: '📧',
      title: 'Email Rápido',
      description: 'Genera un borrador de correo',
      color: '#45b7d1'
    }
  ];

  return (
    <div className="mode-selector">
      <h2 className="mode-selector-title">¿Qué quieres hacer hoy?</h2>
      
      <div className="mode-cards">
        {modes.map((mode) => (
          <div
            key={mode.id}
            className={`mode-card ${currentMode === mode.id ? 'active' : ''}`}
            onClick={() => onModeSelect(mode.id)}
            style={{ '--mode-color': mode.color }}
          >
            <div className="mode-icon">{mode.icon}</div>
            <h3 className="mode-title">{mode.title}</h3>
            <p className="mode-description">{mode.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ModeSelector;
