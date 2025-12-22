import azure.cognitiveservices.speech as speechsdk
import os
import subprocess
from typing import Dict

class SpeechService:
    def __init__(self):
        """Inicializar Speech Service con credenciales de .env"""
        self.speech_key = os.getenv('SPEECH_KEY')
        self.speech_region = os.getenv('SPEECH_REGION')
        
        if not self.speech_key or not self.speech_region:
            raise ValueError("SPEECH_KEY o SPEECH_REGION no encontradas en .env")
    
    def _convert_to_wav(self, audio_file_path: str) -> str:
        """
        Convierte cualquier formato de audio a WAV compatible con Azure Speech usando ffmpeg
        
        Args:
            audio_file_path: Ruta al archivo original
            
        Returns:
            Ruta al archivo WAV convertido
        """
        try:
            print(f"[*] Convirtiendo audio a formato WAV compatible...")
            
            # Crear nuevo nombre de archivo
            wav_path = audio_file_path.rsplit('.', 1)[0] + '_converted.wav'
            
            # Usar ffmpeg para convertir
            # Formato: mono, 16kHz, 16-bit PCM
            command = [
                'ffmpeg',
                '-i', audio_file_path,
                '-acodec', 'pcm_s16le',  # 16-bit PCM
                '-ac', '1',               # Mono
                '-ar', '16000',           # 16kHz
                '-y',                     # Sobrescribir si existe
                wav_path
            ]
            
            # Ejecutar comando
            result = subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=30
            )
            
            if result.returncode == 0 and os.path.exists(wav_path):
                print(f"[OK] Audio convertido exitosamente: {wav_path}")
                return wav_path
            else:
                print(f"[WARN] ffmpeg falló, usando archivo original")
                return audio_file_path
            
        except FileNotFoundError:
            print(f"[WARN] ffmpeg no encontrado, usando archivo original")
            return audio_file_path
        except Exception as e:
            print(f"[WARN] Error convirtiendo audio: {str(e)}")
            return audio_file_path
    
    def transcribe_audio(self, audio_file_path: str) -> Dict:
        """
        Transcribe un archivo de audio con detección automática de idioma
        
        Args:
            audio_file_path: Ruta completa al archivo de audio
            
        Returns:
            Dict con el resultado de la transcripción
        """
        converted_path = None
        
        try:
            # Convertir audio a formato compatible
            converted_path = self._convert_to_wav(audio_file_path)
            
            # Configurar Speech SDK
            speech_config = speechsdk.SpeechConfig(
                subscription=self.speech_key,
                region=self.speech_region
            )
            
            # Habilitar puntuación automática (dictation mode)
            speech_config.enable_dictation()
            
            # Configurar audio desde archivo
            audio_config = speechsdk.audio.AudioConfig(filename=converted_path)
            
            # Configurar detección automática de idioma (español e inglés)
            auto_detect_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
                languages=["es-MX", "en-US", "es-ES"]
            )
            
            # Crear recognizer con detección de idioma
            recognizer = speechsdk.SpeechRecognizer(
                speech_config=speech_config,
                auto_detect_source_language_config=auto_detect_config,
                audio_config=audio_config
            )
            
            print(f"[*] Transcribiendo audio: {converted_path}")
            
            # Reconocer una vez (para audios cortos)
            result = recognizer.recognize_once()
            
            # Procesar resultado según el reason
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                # Obtener idioma detectado
                auto_detect_result = speechsdk.AutoDetectSourceLanguageResult(result)
                detected_language = auto_detect_result.language
                
                print(f"[OK] Transcripción exitosa - Idioma: {detected_language}")
                
                # Limpiar archivo convertido
                if converted_path != audio_file_path and os.path.exists(converted_path):
                    try:
                        os.remove(converted_path)
                        print(f"[*] Archivo convertido eliminado: {converted_path}")
                    except:
                        pass
                
                return {
                    "success": True,
                    "text": result.text,
                    "language": detected_language,
                    "duration": result.duration / 10000000 if result.duration else 0
                }
            
            elif result.reason == speechsdk.ResultReason.NoMatch:
                print("[ERROR] No se detectó habla en el audio")
                return {
                    "success": False,
                    "error": "No se detectó habla en el audio",
                    "details": str(result.no_match_details)
                }
            
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                error_msg = f"Transcripción cancelada: {cancellation.reason}"
                
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    error_msg += f" - {cancellation.error_details}"
                
                print(f"[ERROR] {error_msg}")
                return {
                    "success": False,
                    "error": error_msg
                }
            
            else:
                print(f"[ERROR] Resultado inesperado: {result.reason}")
                return {
                    "success": False,
                    "error": f"Resultado inesperado: {result.reason}"
                }
                
        except Exception as e:
            print(f"[ERROR] Error en transcripción: {str(e)}")
            return {
                "success": False,
                "error": f"Error en transcripción: {str(e)}"
            }
        finally:
            # Limpiar archivo convertido en caso de error
            if converted_path and converted_path != audio_file_path and os.path.exists(converted_path):
                try:
                    os.remove(converted_path)
                except:
                    pass
