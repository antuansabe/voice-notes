# 🎙️ VoiceNotes.AI

**Transforma tus notas de voz en documentos estructurados con IA**

VoiceNotes.AI es una aplicación web moderna que utiliza inteligencia artificial para convertir grabaciones de audio en transcripciones precisas, resúmenes estructurados y documentos PDF profesionales. Perfecta para reuniones, conferencias, entrevistas y notas personales.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![React](https://img.shields.io/badge/React-19.2.0-61DAFB?logo=react)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-000000?logo=flask)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-412991?logo=openai)](https://openai.com/)

---

## ✨ Características Principales

- 🎤 **Grabación en tiempo real** - Graba directamente desde tu navegador
- 📤 **Carga de archivos** - Soporta múltiples formatos de audio (WAV, MP3, M4A, OGG, FLAC)
- 🌍 **Transcripción multiidioma** - Detección automática del idioma
- 🤖 **Análisis con IA** - Resúmenes estructurados mediante OpenAI GPT
- 📧 **Modo Email** - Extrae información y genera borradores de respuesta
- 📄 **Exportación PDF** - Documentos profesionales listos para compartir
- 🎨 **Diseño moderno** - Interfaz intuitiva y responsive
- ⚡ **Procesamiento rápido** - Resultados en segundos

---

## 🛠️ Stack Tecnológico

### Frontend
- **React 19.2.0** - Framework UI moderno
- **Vite** - Build tool ultrarrápido
- **Axios** - Cliente HTTP
- **CSS3** - Diseño responsive y animaciones

### Backend
- **Flask 3.1.0** - Framework web Python
- **Azure Cognitive Services** - Speech-to-Text
- **OpenAI API (GPT-4)** - Análisis y resumen de texto
- **ReportLab** - Generación de PDFs
- **Gunicorn** - Servidor WSGI para producción

---

## 🚀 Inicio Rápido

### Prerrequisitos

- Python 3.9+
- Node.js 18+
- Cuentas en:
  - [Azure Cognitive Services](https://azure.microsoft.com/en-us/services/cognitive-services/speech-to-text/)
  - [OpenAI](https://platform.openai.com/)

### Instalación Local

#### 1. Clonar el repositorio

```bash
git clone https://github.com/antuansabe/voice-notes.git
cd voice-notes
```

#### 2. Configurar Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env
cat > .env << EOF
AZURE_SPEECH_KEY=tu_azure_speech_key
AZURE_SPEECH_REGION=tu_region
OPENAI_API_KEY=tu_openai_api_key
PORT=5000
EOF

# Iniciar servidor
python app.py
```

El backend estará corriendo en `http://localhost:5000`

#### 3. Configurar Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Crear archivo .env
cat > .env << EOF
VITE_API_URL=http://localhost:5000
EOF

# Iniciar aplicación
npm run dev
```

El frontend estará disponible en `http://localhost:5173`

---

## 📋 Variables de Entorno

### Backend (.env)

| Variable | Descripción | Obligatoria |
|----------|-------------|-------------|
| `AZURE_SPEECH_KEY` | Clave de API de Azure Speech | ✅ |
| `AZURE_SPEECH_REGION` | Región de Azure (ej: eastus) | ✅ |
| `OPENAI_API_KEY` | Clave de API de OpenAI | ✅ |
| `PORT` | Puerto del servidor (default: 5000) | ❌ |

### Frontend (.env)

| Variable | Descripción | Obligatoria |
|----------|-------------|-------------|
| `VITE_API_URL` | URL del backend API | ✅ |

---

## 📡 API Endpoints

### `GET /health`
Health check del servidor

**Respuesta:**
```json
{
  "status": "healthy",
  "services": {
    "speech": true,
    "openai": true,
    "pdf": true
  }
}
```

### `POST /transcribe`
Transcribe un archivo de audio

**Request:**
- `audio`: Archivo de audio (multipart/form-data)

**Respuesta:**
```json
{
  "success": true,
  "transcription": "Texto transcrito...",
  "language": "es-ES",
  "duration": 45.2
}
```

### `POST /analyze`
Transcribe y analiza el audio (endpoint completo)

**Request:**
- `audio`: Archivo de audio (multipart/form-data)

**Respuesta:**
```json
{
  "success": true,
  "transcription": {
    "text": "Texto transcrito...",
    "language": "es-ES",
    "duration": 45.2
  },
  "summary": {
    "title": "Título del resumen",
    "main_points": ["Punto 1", "Punto 2"],
    "action_items": ["Acción 1"],
    "key_insights": ["Insight 1"]
  },
  "tokens_used": 150
}
```

### `POST /export-pdf`
Genera un PDF del análisis

**Request (JSON):**
```json
{
  "transcription": { "text": "...", "language": "es" },
  "summary": { "title": "...", "main_points": [] }
}
```

**Respuesta:**
```json
{
  "success": true,
  "filename": "voicenotes_20231222_142614.pdf"
}
```

### `GET /download-pdf/<filename>`
Descarga un PDF generado

---

## 📁 Estructura del Proyecto

```
voice-notes/
├── backend/
│   ├── app.py                 # Aplicación Flask principal
│   ├── requirements.txt       # Dependencias Python
│   ├── render.yaml           # Configuración Render
│   ├── services/
│   │   ├── speech_service.py # Azure Speech-to-Text
│   │   ├── openai_service.py # OpenAI GPT
│   │   └── pdf_service.py    # Generación PDF
│   ├── uploads/              # Archivos temporales
│   └── outputs/              # PDFs generados
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── landing/      # Componentes landing page
│   │   │   ├── app/          # Componentes aplicación
│   │   │   └── shared/       # Componentes compartidos
│   │   ├── services/
│   │   │   └── api.js        # Cliente API
│   │   ├── App.jsx           # Componente principal
│   │   └── main.jsx          # Entry point
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## 🌐 Deploy en Producción

### Backend (Render)

1. Conecta tu repositorio en [Render](https://render.com)
2. Render detectará automáticamente el `render.yaml`
3. Configura las variables de entorno:
   - `AZURE_SPEECH_KEY`
   - `AZURE_SPEECH_REGION`
   - `OPENAI_API_KEY`
4. Deploy automático

### Frontend (Vercel)

1. Importa el proyecto en [Vercel](https://vercel.com)
2. Configura:
   - **Root Directory:** `frontend/`
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
3. Variables de entorno:
   - `VITE_API_URL`: URL del backend en Render
4. Deploy

---

## 🎯 Casos de Uso

### 📝 Reuniones de Trabajo
Graba tus reuniones y obtén automáticamente:
- Transcripción completa
- Puntos principales discutidos
- Acción items asignados
- PDF para compartir con el equipo

### 🎓 Clases y Conferencias
Convierte tus apuntes de voz en:
- Notas estructuradas
- Resúmenes por temas
- Material de estudio

### 📧 Gestión de Emails
Graba un email recibido y obtén:
- Transcripción del mensaje
- Extracción de información clave
- Sugerencia de respuesta

### 💡 Ideas y Brainstorming
Captura tus ideas al vuelo:
- Graba rápidamente
- Organiza automáticamente
- Exporta en formato profesional

---

## 🔒 Seguridad y Privacidad

- Los archivos de audio se eliminan automáticamente después del procesamiento
- Las transcripciones no se almacenan en el servidor
- Comunicación segura mediante HTTPS en producción
- Variables de entorno para credenciales sensibles

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 👨‍💻 Autor

**Antuan Sabe**
- GitHub: [@antuansabe](https://github.com/antuansabe)
- Proyecto: [voice-notes](https://github.com/antuansabe/voice-notes)

---

## 🙏 Agradecimientos

- [Azure Cognitive Services](https://azure.microsoft.com/services/cognitive-services/) por el reconocimiento de voz
- [OpenAI](https://openai.com/) por las capacidades de IA
- [React](https://reactjs.org/) y [Flask](https://flask.palletsprojects.com/) comunidades

---

## 📞 Soporte

¿Encontraste un bug? ¿Tienes una sugerencia?
- Abre un [Issue](https://github.com/antuansabe/voice-notes/issues)
- Contáctame en GitHub

---

<div align="center">

**⭐ Si este proyecto te fue útil, considera darle una estrella ⭐**

Hecho con ❤️ y ☕

</div>
