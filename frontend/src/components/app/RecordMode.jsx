import AudioRecorder from '../shared/AudioRecorder';

const RecordMode = ({ onBack, onRecordingComplete }) => {
  return (
    <div className="mode-screen">
      <div className="mode-header">
        <button onClick={onBack} className="back-button">
          ← Volver
        </button>
        <h2 className="mode-title">🎤 Modo: Grabar Voz</h2>
      </div>

      <AudioRecorder onRecordingComplete={onRecordingComplete} />
    </div>
  );
};

export default RecordMode;
