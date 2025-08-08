import os
import re
from datetime import datetime
from pathlib import Path
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Lee archivos de texto de una carpeta y los organiza en un documento general por fecha'

    def add_arguments(self, parser):
        parser.add_argument('input_folder', type=str, help='Ruta de la carpeta con los archivos de texto')
        parser.add_argument('output_file', type=str, help='Ruta del archivo de salida')

    def extract_date(self, text):
        """
        Extrae la fecha del texto usando diferentes patrones comunes
        Retorna: datetime object o None si no se encuentra fecha
        """
        date_patterns = [
            r'(\d{1,2}/\d{1,2}/\d{2,4})',  # dd/mm/yyyy o d/m/yy
            r'(\d{1,2}-\d{1,2}-\d{2,4})',  # dd-mm-yyyy o d-m-yy
            r'(\d{4}-\d{2}-\d{2})',        # yyyy-mm-dd
            r'(\d{1,2}\s+(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)\s+\d{4})'  # dd mes yyyy
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                date_str = match.group(1)
                try:
                    # Intenta diferentes formatos de fecha
                    for fmt in ['%d/%m/%Y', '%d/%m/%y', '%d-%m-%Y', '%d-%m-%y', '%Y-%m-%d', '%d %B %Y']:
                        try:
                            return datetime.strptime(date_str, fmt)
                        except ValueError:
                            continue
                except ValueError:
                    continue
        return None

    def process_file(self, file_path):
        """
        Procesa un archivo y retorna su contenido y fecha
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                date = self.extract_date(content)
                return {
                    'content': content,
                    'date': date,
                    'file_name': os.path.basename(file_path)
                }
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al procesar {file_path}: {str(e)}'))
            return None

    def handle(self, *args, **options):
        input_folder = options['input_folder']
        output_file = options['output_file']
        
        if not os.path.exists(input_folder):
            self.stdout.write(self.style.ERROR(f'La carpeta {input_folder} no existe'))
            return

        # Lista para almacenar la información de los archivos
        files_info = []
        
        # Procesar todos los archivos de texto
        for file_name in os.listdir(input_folder):
            if file_name.endswith(('.txt', '.md')):
                file_path = os.path.join(input_folder, file_name)
                file_info = self.process_file(file_path)
                if file_info:
                    files_info.append(file_info)

        # Ordenar por fecha (si existe) y nombre de archivo
        files_info.sort(key=lambda x: (x['date'] or datetime.max, x['file_name']))

        # Crear el documento general
        try:
            with open(output_file, 'w', encoding='utf-8') as out_file:
                out_file.write("# Documento General de Conversaciones\n\n")
                
                for file_info in files_info:
                    out_file.write(f"\n## {file_info['file_name']}\n")
                    if file_info['date']:
                        out_file.write(f"Fecha: {file_info['date'].strftime('%d/%m/%Y')}\n")
                    out_file.write("-" * 80 + "\n\n")
                    out_file.write(file_info['content'])
                    out_file.write("\n" + "=" * 80 + "\n")

            self.stdout.write(self.style.SUCCESS(
                f'Se ha creado exitosamente el documento general en {output_file}'
            ))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error al crear el documento general: {str(e)}')) 