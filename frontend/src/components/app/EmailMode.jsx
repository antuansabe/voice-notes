import AudioRecorder from '../shared/AudioRecorder';

const EmailMode = ({ onBack, onRecordingComplete }) => {
  return (
    <div className="mode-screen">
      <div className="mode-header">
        <button onClick={onBack} className="back-button">
          ← Volver
        </button>
        <h2 className="mode-title">📧 Modo: Email Rápido</h2>
      </div>

      <div className="email-mode-info">
        <p className="info-text">
          Graba tu mensaje y generaremos un borrador de email profesional listo para copiar.
        </p>
      </div>

      <AudioRecorder onRecordingComplete={onRecordingComplete} />
    </div>
  );
};

export default EmailMode;
