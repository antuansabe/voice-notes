import AudioUploader from '../shared/AudioUploader';

const UploadMode = ({ onBack, onFileSelect }) => {
  return (
    <div className="mode-screen">
      <div className="mode-header">
        <button onClick={onBack} className="back-button">
          ← Volver
        </button>
        <h2 className="mode-title">📁 Modo: Subir Audio</h2>
      </div>

      <AudioUploader onFileSelect={onFileSelect} />
    </div>
  );
};

export default UploadMode;
