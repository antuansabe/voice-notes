from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from datetime import datetime
import os
from typing import Dict

class PDFService:
    def __init__(self):
        """Inicializar servicio de PDF"""
        self.output_folder = 'outputs'
        os.makedirs(self.output_folder, exist_ok=True)
        print("[OK] PDF Service inicializado")
    
    def generate_pdf(self, data: Dict) -> Dict:
        """
        Generar PDF con el resumen estructurado
        
        Args:
            data: Dict con transcription y summary
            
        Returns:
            Dict con path del PDF generado
        """
        try:
            # Extraer datos
            transcription = data.get('transcription', {})
            summary = data.get('summary', {})
            
            # Generar nombre de archivo
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"voicenotes_{timestamp}.pdf"
            filepath = os.path.join(self.output_folder, filename)
            
            # Crear documento PDF
            doc = SimpleDocTemplate(
                filepath,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=18
            )
            
            # Contenido del PDF
            story = []
            styles = getSampleStyleSheet()
            
            # Crear estilos personalizados
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#0072ff'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=16,
                textColor=colors.HexColor('#0072ff'),
                spaceAfter=12,
                spaceBefore=12
            )
            
            body_style = ParagraphStyle(
                'CustomBody',
                parent=styles['BodyText'],
                fontSize=11,
                alignment=TA_JUSTIFY,
                spaceAfter=12
            )
            
            # TÍTULO PRINCIPAL
            titulo = summary.get('titulo', 'Análisis de Audio')
            story.append(Paragraph(titulo, title_style))
            story.append(Spacer(1, 0.2*inch))
            
            # METADATA
            metadata_data = [
                ['Idioma:', transcription.get('language', 'N/A')],
                ['Duración:', f"{transcription.get('duration', 0):.2f} segundos"],
                ['Fecha:', datetime.now().strftime("%d/%m/%Y %H:%M")]
            ]
            
            metadata_table = Table(metadata_data, colWidths=[2*inch, 4*inch])
            metadata_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey)
            ]))
            
            story.append(metadata_table)
            story.append(Spacer(1, 0.3*inch))
            
            # RESUMEN EJECUTIVO
            story.append(Paragraph("Resumen Ejecutivo", heading_style))
            resumen_text = summary.get('resumen', 'No disponible')
            story.append(Paragraph(resumen_text, body_style))
            story.append(Spacer(1, 0.2*inch))
            
            # PUNTOS CLAVE
            story.append(Paragraph("Puntos Clave", heading_style))
            puntos = summary.get('puntos_clave', [])
            
            for i, punto in enumerate(puntos, 1):
                punto_text = f"{i}. {punto}"
                story.append(Paragraph(punto_text, body_style))
            
            story.append(Spacer(1, 0.2*inch))
            
            # PALABRAS CLAVE
            story.append(Paragraph("Palabras Clave", heading_style))
            palabras = summary.get('palabras_clave', [])
            palabras_text = ", ".join(palabras)
            
            palabras_table = Table([[palabras_text]], colWidths=[6.5*inch])
            palabras_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e3f2fd')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#0072ff')),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#0072ff'))
            ]))
            
            story.append(palabras_table)
            story.append(Spacer(1, 0.3*inch))
            
            # TRANSCRIPCIÓN COMPLETA
            story.append(Paragraph("Transcripción Completa", heading_style))
            transcription_text = transcription.get('text', 'No disponible')
            story.append(Paragraph(transcription_text, body_style))
            
            # FOOTER
            story.append(Spacer(1, 0.5*inch))
            footer_style = ParagraphStyle(
                'Footer',
                parent=styles['Normal'],
                fontSize=9,
                textColor=colors.grey,
                alignment=TA_CENTER
            )
            story.append(Paragraph("Generado por VoiceNotes.AI", footer_style))
            
            # Construir PDF
            doc.build(story)
            
            print(f"[OK] PDF generado: {filepath}")
            
            return {
                "success": True,
                "filename": filename,
                "filepath": filepath
            }
            
        except Exception as e:
            print(f"[ERROR] Error generando PDF: {str(e)}")
            return {
                "success": False,
                "error": f"Error generando PDF: {str(e)}"
            }