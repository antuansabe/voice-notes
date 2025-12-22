import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Endpoint para análisis completo
export const analyzeAudio = async (audioFile) => {
  const formData = new FormData();
  formData.append('audio', audioFile);
  
  const response = await api.post('/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

// Endpoint para exportar PDF
export const exportPDF = async (data) => {
  const response = await api.post('/export-pdf', data);
  return response.data;
};

// Endpoint para descargar PDF
export const downloadPDF = (filename) => {
  return `${API_URL}/download-pdf/${filename}`;
};

// Endpoint para generar email desde audio
export const analyzeForEmail = async (audioFile) => {
  const formData = new FormData();
  formData.append('audio', audioFile);
  
  const response = await api.post('/analyze-for-email', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export default api;