from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime
from services.statistics_services import StatisticsService
from banco.models import TransferStatistics

class Command(BaseCommand):
    help = 'Actualiza las estadísticas de transferencias para una fecha específica'

    def add_arguments(self, parser):
        parser.add_argument('--date', type=str, help='Fecha en formato YYYY-MM-DD')

    def handle(self, *args, **options):
        try:
            date_str = options.get('date')
            if date_str:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
            else:
                date = timezone.now().date()
            
            # Actualizar estadísticas para la fecha específica
            TransferStatistics.update_statistics(date)
            
            self.stdout.write(
                self.style.SUCCESS(f'Estadísticas actualizadas correctamente para la fecha {date}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error al actualizar estadísticas: {str(e)}')
            ) 