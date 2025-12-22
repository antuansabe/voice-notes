import { useState } from 'react';
import TranscriptionView from '../shared/TranscriptionView';
import SummaryView from '../shared/SummaryView';
import EmailPreview from '../shared/EmailPreview';

const Results = ({ analysisResult, mode, onReset }) => {
  const [viewMode, setViewMode] = useState('summary'); // 'summary' or 'email'

  return (
    <div className="results-screen">
      <div className="results-header">
        <button onClick={onReset} className="back-button">
          ← Analizar otro
        </button>
        <h2 className="results-title">✅ Análisis Completado</h2>
      </div>

      {mode === 'email' && (
        <div className="view-toggle">
          <button 
            className={`toggle-button ${viewMode === 'summary' ? 'active' : ''}`}
            onClick={() => setViewMode('summary')}
          >
            📄 Vista Resumen
          </button>
          <button 
            className={`toggle-button ${viewMode === 'email' ? 'active' : ''}`}
            onClick={() => setViewMode('email')}
          >
            📧 Vista Email
          </button>
        </div>
      )}

      <div className="results-content">
        <TranscriptionView data={analysisResult.transcription} />
        
        {viewMode === 'summary' ? (
          <SummaryView 
            summary={analysisResult.summary} 
            transcription={analysisResult.transcription}
          />
        ) : (
          <EmailPreview emailData={analysisResult.email} />
        )}
      </div>
    </div>
  );
};

export default Results;
