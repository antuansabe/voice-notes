from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import time

# Importar servicios
from services.speech_service import SpeechService
from services.openai_service import OpenAIService
from services.pdf_service import PDFService

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuración
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max

# Inicializar servicios
try:
    speech_service = SpeechService()
    print("[OK] Speech Service inicializado")
except Exception as e:
    print(f"[ERROR] Speech Service: {e}")
    speech_service = None

try:
    openai_service = OpenAIService()
    print("[OK] OpenAI Service inicializado")
except Exception as e:
    print(f"[ERROR] OpenAI Service: {e}")
    openai_service = None

try:
    pdf_service = PDFService()
    print("[OK] PDF Service inicializado")
except Exception as e:
    print(f"[ERROR] PDF Service: {e}")
    pdf_service = None

# Formatos de audio permitidos
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a', 'flac'}

def allowed_file(filename):
    """Verificar si el archivo tiene una extensión permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "VoiceNotes.AI Backend is running",
        "services": {
            "speech": speech_service is not None,
            "openai": openai_service is not None,
            "pdf": pdf_service is not None
        }
    }), 200

@app.route('/', methods=['GET'])
def home():
    """Home endpoint"""
    return jsonify({
        "app": "VoiceNotes.AI",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health (GET)",
            "transcribe": "/transcribe (POST)",
            "analyze": "/analyze (POST)",
            "export-pdf": "/export-pdf (POST)",
            "download-pdf": "/download-pdf/<filename> (GET)"
        }
    }), 200

@app.route('/transcribe', methods=['POST'])
def transcribe():
    """
    Endpoint para transcribir audio
    Espera un archivo de audio en el form-data con key 'audio'
    """
    try:
        if speech_service is None:
            return jsonify({"error": "Speech Service no disponible"}), 503
        
        if 'audio' not in request.files:
            return jsonify({"error": "No se encontró archivo de audio"}), 400
        
        file = request.files['audio']
        
        if file.filename == '':
            return jsonify({"error": "Nombre de archivo vacío"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                "error": f"Formato no permitido. Use: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # Guardar archivo temporalmente
        timestamp = int(time.time())
        filename = secure_filename(f"{timestamp}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        print(f"[*] Archivo guardado: {filepath}")
        
        # Transcribir
        result = speech_service.transcribe_audio(filepath)
        
        # Eliminar archivo temporal
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"[*] Archivo eliminado: {filepath}")
        except Exception as e:
            print(f"[WARN] No se pudo eliminar: {e}")
        
        if result['success']:
            return jsonify({
                "success": True,
                "transcription": result['text'],
                "language": result['language'],
                "duration": result['duration']
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": result['error']
            }), 500
            
    except Exception as e:
        print(f"[ERROR] /transcribe: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Endpoint COMPLETO: Transcribir + Analizar + Estructurar
    Espera un archivo de audio y devuelve todo el análisis
    """
    try:
        # Verificar servicios
        if speech_service is None:
            return jsonify({"error": "Speech Service no disponible"}), 503
        
        if openai_service is None:
            return jsonify({"error": "OpenAI Service no disponible"}), 503
        
        # Validar archivo
        if 'audio' not in request.files:
            return jsonify({"error": "No se encontró archivo de audio"}), 400
        
        file = request.files['audio']
        
        if file.filename == '':
            return jsonify({"error": "Nombre de archivo vacío"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({
                "error": f"Formato no permitido. Use: {', '.join(ALLOWED_EXTENSIONS)}"
            }), 400
        
        # Guardar archivo
        timestamp = int(time.time())
        filename = secure_filename(f"{timestamp}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        print(f"[*] Procesando: {filepath}")
        
        # PASO 1: Transcribir
        print("[*] Paso 1/2: Transcribiendo audio...")
        transcription_result = speech_service.transcribe_audio(filepath)
        
        # Eliminar archivo temporal
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception as e:
            print(f"[WARN] No se pudo eliminar: {e}")
        
        if not transcription_result['success']:
            return jsonify({
                "success": False,
                "error": transcription_result['error'],
                "step": "transcription"
            }), 500
        
        # PASO 2: Generar resumen con OpenAI
        print("[*] Paso 2/2: Generando resumen estructurado...")
        summary_result = openai_service.generate_summary(
            transcription=transcription_result['text'],
            language=transcription_result['language']
        )
        
        if not summary_result['success']:
            return jsonify({
                "success": False,
                "error": summary_result['error'],
                "step": "summarization",
                "transcription": transcription_result['text']
            }), 500
        
        # Respuesta exitosa completa
        print("[OK] Análisis completo exitoso")
        
        return jsonify({
            "success": True,
            "transcription": {
                "text": transcription_result['text'],
                "language": transcription_result['language'],
                "duration": transcription_result['duration']
            },
            "summary": summary_result['summary'],
            "tokens_used": summary_result['tokens_used']
        }), 200
        
    except Exception as e:
        print(f"[ERROR] /analyze: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Error: {str(e)}"
        }), 500

@app.route('/export-pdf', methods=['POST'])
def export_pdf():
    """
    Endpoint para generar PDF del análisis
    Espera JSON con transcription y summary
    """
    try:
        if pdf_service is None:
            return jsonify({"error": "PDF Service no disponible"}), 503
        
        # Obtener datos del request
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No se recibieron datos"}), 400
        
        # Validar que tenga los campos necesarios
        if 'transcription' not in data or 'summary' not in data:
            return jsonify({
                "error": "Faltan campos requeridos: transcription, summary"
            }), 400
        
        print("[*] Generando PDF...")
        
        # Generar PDF
        result = pdf_service.generate_pdf(data)
        
        if result['success']:
            return jsonify({
                "success": True,
                "filename": result['filename'],
                "message": "PDF generado exitosamente"
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": result['error']
            }), 500
            
    except Exception as e:
        print(f"[ERROR] /export-pdf: {str(e)}")
        return jsonify({
            "success": False,
            "error": f"Error: {str(e)}"
        }), 500

@app.route('/download-pdf/<filename>', methods=['GET'])
def download_pdf(filename):
    """
    Endpoint para descargar un PDF generado
    """
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        
        if not os.path.exists(filepath):
            return jsonify({"error": "Archivo no encontrado"}), 404
        
        return send_file(
            filepath,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
    except Exception as e:
        print(f"[ERROR] /download-pdf: {str(e)}")
        return jsonify({"error": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    print("\n[*] Iniciando VoiceNotes.AI Backend...")
    print(f"[*] Carpeta uploads: {UPLOAD_FOLDER}")
    print(f"[*] Carpeta outputs: {OUTPUT_FOLDER}")
    
    if speech_service:
        print("[OK] Speech Service: OK")
    else:
        print("[ERROR] Speech Service: FALLO")
    
    if openai_service:
        print("[OK] OpenAI Service: OK")
    else:
        print("[ERROR] OpenAI Service: FALLO")
    
    if pdf_service:
        print("[OK] PDF Service: OK")
    else:
        print("[ERROR] PDF Service: FALLO")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)