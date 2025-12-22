import { useState } from 'react';

// Landing components
import Navbar from './components/landing/Navbar';
import HeroSection from './components/landing/HeroSection';
import FeaturesSection from './components/landing/FeaturesSection';
import HowItWorks from './components/landing/HowItWorks';
import TechStack from './components/landing/TechStack';
import Footer from './components/landing/Footer';

// App components
import RecordMode from './components/app/RecordMode';
import UploadMode from './components/app/UploadMode';
import EmailMode from './components/app/EmailMode';
import Results from './components/app/Results';
import LoadingSpinner from './components/shared/LoadingSpinner';

// Services
import { analyzeAudio } from './services/api';

import './App.css';

function App() {
  const [appState, setAppState] = useState('landing'); // 'landing', 'record', 'upload', 'email', 'analyzing', 'results'
  const [currentMode, setCurrentMode] = useState(null);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [error, setError] = useState(null);

  const handleGetStarted = () => {
    const featuresSection = document.getElementById('features');
    featuresSection?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleModeSelect = (mode) => {
    setCurrentMode(mode);
    setAppState(mode);
    setError(null);
    setAnalysisResult(null);
  };

  const handleBack = () => {
    setAppState('landing');
    setCurrentMode(null);
    setError(null);
  };

  const handleFileSelect = async (file) => {
    await processAudio(file, currentMode);
  };

  const processAudio = async (file, mode) => {
    try {
      setAppState('analyzing');
      setError(null);

      console.log('Procesando audio:', file.name, 'Modo:', mode);
      
      const result = await analyzeAudio(file);

      if (result.success) {
        // Si es modo email, generar formato email
        if (mode === 'email') {
          result.email = generateEmailFromSummary(result.summary);
        }
        
        setAnalysisResult(result);
        setAppState('results');
        console.log('Análisis exitoso:', result);
      } else {
        setError(result.error || 'Error desconocido');
        setAppState(currentMode);
      }
    } catch (err) {
      console.error('Error en análisis:', err);
      setError(err.response?.data?.error || err.message || 'Error al procesar el audio');
      setAppState(currentMode);
    }
  };

  const generateEmailFromSummary = (summary) => {
    // Convertir resumen en formato email
    const titulo = summary.titulo || summary.title || 'Sin título';
    const resumen = summary.resumen || summary.summary || '';
    const puntos = summary.puntos_clave || summary.key_points || [];

    let cuerpo = resumen + '\n\n';
    
    if (puntos.length > 0) {
      cuerpo += 'Puntos principales:\n';
      puntos.forEach((punto, index) => {
        cuerpo += `${index + 1}. ${punto}\n`;
      });
    }

    return {
      para: '',
      asunto: titulo,
      cuerpo: cuerpo.trim()
    };
  };

  const handleReset = () => {
    setAppState('landing');
    setCurrentMode(null);
    setAnalysisResult(null);
    setError(null);
  };

  return (
    <div className="app">
      {appState === 'landing' && (
        <>
          <Navbar onGetStarted={handleGetStarted} />
          <HeroSection onGetStarted={handleGetStarted} />
          <FeaturesSection onSelectMode={handleModeSelect} />
          <HowItWorks />
          <TechStack />
          <Footer />
        </>
      )}

      {appState === 'record' && (
        <RecordMode 
          onBack={handleBack}
          onRecordingComplete={handleFileSelect}
        />
      )}

      {appState === 'upload' && (
        <UploadMode 
          onBack={handleBack}
          onFileSelect={handleFileSelect}
        />
      )}

      {appState === 'email' && (
        <EmailMode 
          onBack={handleBack}
          onRecordingComplete={handleFileSelect}
        />
      )}

      {appState === 'analyzing' && (
        <div className="analyzing-screen">
          <LoadingSpinner message="Analizando tu audio... Esto puede tomar unos segundos" />
        </div>
      )}

      {appState === 'results' && analysisResult && (
        <Results 
          analysisResult={analysisResult}
          mode={currentMode}
          onReset={handleReset}
        />
      )}

      {error && appState !== 'results' && (
        <div className="error-overlay">
          <div className="error-message">
            <h3>❌ Error</h3>
            <p>{error}</p>
            <button onClick={() => setError(null)} className="reset-button">
              Intentar de nuevo
            </button>
            <button onClick={handleBack} className="back-button-link">
              Volver al inicio
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
