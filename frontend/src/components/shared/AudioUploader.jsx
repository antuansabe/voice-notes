import { useState, useRef } from 'react';

const AudioUploader = ({ onFileSelect }) => {
  const [isDragging, setIsDragging] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleFileSelection(files[0]);
    }
  };

  const handleFileInput = (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      handleFileSelection(files[0]);
    }
  };

  const handleFileSelection = (file) => {
    // Validar tipo de archivo
    const validTypes = ['audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/ogg', 'audio/x-m4a'];
    const validExtensions = ['.wav', '.mp3', '.m4a', '.ogg', '.flac'];
    
    const isValidType = validTypes.some(type => file.type.includes(type));
    const isValidExtension = validExtensions.some(ext => file.name.toLowerCase().endsWith(ext));
    
    if (!isValidType && !isValidExtension) {
      alert('Por favor selecciona un archivo de audio válido (WAV, MP3, M4A, OGG, FLAC)');
      return;
    }

    // Validar tamaño (50MB max)
    const maxSize = 50 * 1024 * 1024; // 50MB
    if (file.size > maxSize) {
      alert('El archivo es muy grande. Máximo 50MB.');
      return;
    }

    setSelectedFile(file);
    onFileSelect(file);
  };

  const handleClick = () => {
    fileInputRef.current.click();
  };

  return (
    <div className="audio-uploader">
      <div
        className={`drop-zone ${isDragging ? 'dragging' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={handleClick}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileInput}
          accept=".wav,.mp3,.m4a,.ogg,.flac,audio/*"
          style={{ display: 'none' }}
        />
        
        <div className="drop-zone-content">
          <span className="upload-icon">🎵</span>
          {selectedFile ? (
            <>
              <p className="primary-text">✓ {selectedFile.name}</p>
              <p className="secondary-text">{(selectedFile.size / 1024 / 1024).toFixed(2)} MB</p>
              <div className="formats-text">Listo para procesar</div>
            </>
          ) : (
            <>
              <p className="primary-text">Arrastra tu audio aquí</p>
              <p className="secondary-text">o haz clic para seleccionar</p>
              <div className="formats-text">Formatos: WAV, MP3, M4A, OGG, FLAC</div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default AudioUploader;