import { useState, useRef, useEffect } from 'react';

const AudioRecorder = ({ onRecordingComplete }) => {
  const [isRecording, setIsRecording] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioURL, setAudioURL] = useState(null);
  
  const mediaRecorderRef = useRef(null);
  const chunksRef = useRef([]);
  const timerRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
      if (timerRef.current) {
        clearInterval(timerRef.current);
      }
    };
  }, []);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/wav' });
        const url = URL.createObjectURL(blob);
        setAudioURL(url);
        
        // Crear archivo para enviar
        const file = new File([blob], `recording_${Date.now()}.wav`, { 
          type: 'audio/wav' 
        });
        onRecordingComplete(file);
      };

      mediaRecorder.start();
      setIsRecording(true);
      setRecordingTime(0);

      // Timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);

    } catch (error) {
      console.error('Error al acceder al micrófono:', error);
      alert('No se pudo acceder al micrófono. Por favor verifica los permisos.');
    }
  };

  const pauseRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      if (isPaused) {
        mediaRecorderRef.current.resume();
        timerRef.current = setInterval(() => {
          setRecordingTime(prev => prev + 1);
        }, 1000);
      } else {
        mediaRecorderRef.current.pause();
        clearInterval(timerRef.current);
      }
      setIsPaused(!isPaused);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      streamRef.current.getTracks().forEach(track => track.stop());
      clearInterval(timerRef.current);
      setIsRecording(false);
      setIsPaused(false);
    }
  };

  const resetRecording = () => {
    setAudioURL(null);
    setRecordingTime(0);
    chunksRef.current = [];
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="audio-recorder">
      <div className="recorder-container">
        {!isRecording && !audioURL ? (
          <div className="recorder-idle">
            <div className="mic-icon-large">🎤</div>
            <p className="recorder-prompt">Presiona el botón para comenzar a grabar</p>
            <button onClick={startRecording} className="record-button start">
              ● Iniciar Grabación
            </button>
          </div>
        ) : isRecording ? (
          <div className="recorder-active">
            <div className={`recording-indicator ${isPaused ? 'paused' : ''}`}>
              <span className="pulse-dot"></span>
              {isPaused ? 'Pausado' : 'Grabando'}
            </div>
            
            <div className="recording-timer">
              {formatTime(recordingTime)}
            </div>

            <div className="waveform">
              {[...Array(20)].map((_, i) => (
                <div 
                  key={i} 
                  className="wave-bar"
                  style={{
                    animationDelay: `${i * 0.1}s`,
                    animationPlayState: isPaused ? 'paused' : 'running'
                  }}
                />
              ))}
            </div>

            <div className="recorder-controls">
              <button onClick={pauseRecording} className="control-button pause">
                {isPaused ? '▶️ Reanudar' : '⏸️ Pausar'}
              </button>
              <button onClick={stopRecording} className="control-button stop">
                ⏹️ Detener
              </button>
            </div>
          </div>
        ) : (
          <div className="recorder-complete">
            <div className="success-icon">✅</div>
            <p className="recorder-message">Grabación completada</p>
            <p className="recording-duration">Duración: {formatTime(recordingTime)}</p>
            
            {audioURL && (
              <audio controls src={audioURL} className="audio-preview" />
            )}

            <div className="recorder-actions">
              <button onClick={resetRecording} className="action-button secondary">
                🔄 Grabar de nuevo
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AudioRecorder;
