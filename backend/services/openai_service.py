from openai import AzureOpenAI
import os
import json
from typing import Dict

class OpenAIService:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.endpoint = os.getenv('OPENAI_ENDPOINT')
        self.deployment = os.getenv('OPENAI_DEPLOYMENT')
        
        if not all([self.api_key, self.endpoint, self.deployment]):
            raise ValueError("OPENAI credentials no encontradas en .env")
        
        self.client = AzureOpenAI(
            api_key=self.api_key,
            api_version="2024-02-15-preview",
            azure_endpoint=self.endpoint,
            timeout=30.0
        )
        
        print("[OK] Azure OpenAI Service inicializado")
    
    def generate_summary(self, transcription: str, language: str = "es-MX") -> Dict:
        try:
            is_spanish = language.startswith('es')
            system_prompt = self._get_system_prompt(is_spanish)
            user_prompt = self._get_user_prompt(transcription, is_spanish)
            
            print("[*] Generando resumen con GPT-4o-mini...")
            
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.5,
                max_tokens=1000,
                response_format={"type": "json_object"},
                timeout=30
            )
            
            result = response.choices[0].message.content
            summary_data = json.loads(result)
            
            print("[OK] Resumen generado exitosamente")
            
            return {
                "success": True,
                "summary": summary_data,
                "tokens_used": {
                    "prompt": response.usage.prompt_tokens,
                    "completion": response.usage.completion_tokens,
                    "total": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            print(f"[ERROR] Error generando resumen: {str(e)}")
            return {
                "success": False,
                "error": f"Error generando resumen: {str(e)}"
            }
    
    def _get_system_prompt(self, is_spanish: bool) -> str:
        if is_spanish:
            prompt = 'Eres un asistente experto en crear resumenes estructurados de transcripciones de audio. '
            prompt += 'Tu tarea es analizar la transcripcion y generar un documento estructurado con: '
            prompt += '1. Un titulo descriptivo (maximo 10 palabras) '
            prompt += '2. Un resumen ejecutivo (2-3 oraciones que capturen la esencia) '
            prompt += '3. Entre 3 y 5 puntos clave (los aspectos mas importantes) '
            prompt += '4. Una lista de palabras clave relevantes (5-8 palabras). '
            prompt += 'IMPORTANTE: Debes responder SOLO en formato JSON valido, sin texto adicional. '
            prompt += 'Formato de respuesta: {"titulo": "Titulo aqui", "resumen": "Resumen aqui", '
            prompt += '"puntos_clave": ["Punto 1", "Punto 2"], "palabras_clave": ["palabra1", "palabra2"]}'
            return prompt
        else:
            prompt = 'You are an expert assistant in creating structured summaries of audio transcriptions. '
            prompt += 'Your task is to analyze the transcription and generate a structured document with: '
            prompt += '1. A descriptive title (maximum 10 words) '
            prompt += '2. An executive summary (2-3 sentences capturing the essence) '
            prompt += '3. Between 3 and 5 key points (the most important aspects) '
            prompt += '4. A list of relevant keywords (5-8 words). '
            prompt += 'IMPORTANT: You must respond ONLY in valid JSON format, without additional text. '
            prompt += 'Response format: {"title": "Title here", "summary": "Summary here", '
            prompt += '"key_points": ["Point 1", "Point 2"], "keywords": ["word1", "word2"]}'
            return prompt
    
    def _get_user_prompt(self, transcription: str, is_spanish: bool) -> str:
        if is_spanish:
            return f'Analiza la siguiente transcripcion y genera un resumen estructurado en formato JSON: Transcripcion: {transcription}. Recuerda: responde SOLO con el JSON, sin texto adicional.'
        else:
            return f'Analyze the following transcription and generate a structured summary in JSON format: Transcription: {transcription}. Remember: respond ONLY with the JSON, no additional text.'
    
    def generate_email(self, transcription: str, language: str = "es-MX") -> Dict:
        """Generar borrador de email desde transcripción"""
        try:
            is_spanish = language.startswith('es')
            system_prompt = self._get_email_system_prompt(is_spanish)
            user_prompt = self._get_email_user_prompt(transcription, is_spanish)
            
            print("[*] Generando email con GPT-4o-mini...")
            
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=800,
                response_format={"type": "json_object"},
                timeout=30
            )
            
            result = response.choices[0].message.content
            email_data = json.loads(result)
            
            print("[OK] Email generado exitosamente")
            
            return {
                "success": True,
                "email": email_data,
                "tokens_used": {
                    "prompt": response.usage.prompt_tokens,
                    "completion": response.usage.completion_tokens,
                    "total": response.usage.total_tokens
                }
            }
            
        except Exception as e:
            print(f"[ERROR] Error generando email: {str(e)}")
            return {
                "success": False,
                "error": f"Error generando email: {str(e)}"
            }
    
    def _get_email_system_prompt(self, is_spanish: bool) -> str:
        """System prompt para generación de emails"""
        if is_spanish:
            prompt = 'Eres un asistente experto en redactar emails profesionales. '
            prompt += 'Tu tarea es analizar una transcripcion de voz y convertirla en un borrador de email bien estructurado. '
            prompt += 'Debes generar: 1. Un destinatario sugerido (puede ser generico como "Equipo" si no se especifica), '
            prompt += '2. Un asunto claro y conciso, 3. Un cuerpo de email profesional y bien redactado. '
            prompt += 'IMPORTANTE: Debes responder SOLO en formato JSON valido. '
            prompt += 'Formato: {"para": "Destinatario", "asunto": "Asunto del email", "cuerpo": "Cuerpo del email"}'
            return prompt
        else:
            prompt = 'You are an expert assistant in writing professional emails. '
            prompt += 'Your task is to analyze a voice transcription and convert it into a well-structured email draft. '
            prompt += 'You must generate: 1. A suggested recipient (can be generic like "Team" if not specified), '
            prompt += '2. A clear and concise subject, 3. A professional and well-written email body. '
            prompt += 'IMPORTANT: You must respond ONLY in valid JSON format. '
            prompt += 'Format: {"to": "Recipient", "subject": "Email subject", "body": "Email body"}'
            return prompt
    
    def _get_email_user_prompt(self, transcription: str, is_spanish: bool) -> str:
        """User prompt para generación de emails"""
        if is_spanish:
            return f'Convierte la siguiente transcripcion en un email profesional en formato JSON: Transcripcion: {transcription}. Recuerda: responde SOLO con el JSON, sin texto adicional.'
        else:
            return f'Convert the following transcription into a professional email in JSON format: Transcription: {transcription}. Remember: respond ONLY with the JSON, no additional text.'