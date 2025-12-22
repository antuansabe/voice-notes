import { useState } from 'react';
import { exportPDF, downloadPDF } from '../../services/api';

const SummaryView = ({ summary, transcription }) => {
  const [isExporting, setIsExporting] = useState(false);
  const [exportMessage, setExportMessage] = useState('');

  if (!summary) return null;

  const handleExportPDF = async () => {
    try {
      setIsExporting(true);
      setExportMessage('Generando PDF...');

      const data = {
        transcription,
        summary
      };

      const result = await exportPDF(data);

      if (result.success) {
        setExportMessage('¡PDF generado! Descargando...');
        
        // Descargar automáticamente
        const downloadUrl = downloadPDF(result.filename);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = result.filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        setExportMessage('✅ PDF descargado exitosamente');
        setTimeout(() => setExportMessage(''), 3000);
      }
    } catch (error) {
      console.error('Error exportando PDF:', error);
      setExportMessage('❌ Error al generar PDF');
      setTimeout(() => setExportMessage(''), 3000);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <div className="summary-view">
      <h2>📝 Resumen Ejecutivo</h2>

      <div className="summary-section">
        <h3>Título</h3>
        <p className="summary-title">{summary.titulo || summary.title}</p>
      </div>

      <div className="summary-section">
        <h3>Resumen</h3>
        <p className="summary-text">{summary.resumen || summary.summary}</p>
      </div>

      <div className="summary-section">
        <h3>Puntos Clave</h3>
        <ul className="key-points">
          {(summary.puntos_clave || summary.key_points || []).map((point, index) => (
            <li key={index}>{point}</li>
          ))}
        </ul>
      </div>

      <div className="summary-section">
        <h3>Palabras Clave</h3>
        <div className="keywords">
          {(summary.palabras_clave || summary.keywords || []).map((keyword, index) => (
            <span key={index} className="keyword-tag">{keyword}</span>
          ))}
        </div>
      </div>

      <div className="export-section">
        <button 
          onClick={handleExportPDF} 
          disabled={isExporting}
          className="export-button"
        >
          {isExporting ? '⏳ Generando...' : '📥 Exportar PDF'}
        </button>
        {exportMessage && <p className="export-message">{exportMessage}</p>}
      </div>
    </div>
  );
};

export default SummaryView;