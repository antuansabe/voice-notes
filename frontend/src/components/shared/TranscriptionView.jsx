const TranscriptionView = ({ data }) => {
    if (!data) return null;
  
    return (
      <div className="transcription-view">
        <h2>🎤 Transcripción</h2>
        
        <div className="metadata">
          <div className="metadata-item">
            <span className="label">Idioma:</span>
            <span className="value">{data.language}</span>
          </div>
          <div className="metadata-item">
            <span className="label">Duración:</span>
            <span className="value">{data.duration.toFixed(2)} segundos</span>
          </div>
        </div>
  
        <div className="transcription-text">
          <p>{data.text}</p>
        </div>
      </div>
    );
  };
  
  export default TranscriptionView;