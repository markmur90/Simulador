from django.utils import timezone
from django.db.models import Count, Sum, Avg
from django.contrib.auth.models import User
from banco.models import (
    SystemLog,
    TransferStatistics,
    UserActivity,
    Transfer
)

class StatisticsService:
    @staticmethod
    def log_system_event(level, action, user=None, ip_address=None, description="", additional_data=None):
        """
        Registra un evento en el sistema.
        """
        SystemLog.objects.create(
            level=level,
            action=action,
            user=user,
            ip_address=ip_address,
            description=description,
            additional_data=additional_data
        )

    @staticmethod
    def log_user_activity(user, activity_type, amount=None):
        """
        Registra actividad de usuario.
        """
        UserActivity.log_activity(user, activity_type, amount)

    @staticmethod
    def update_daily_statistics():
        """
        Actualiza las estadísticas del día actual.
        """
        today = timezone.now().date()
        TransferStatistics.update_statistics(today)

    @staticmethod
    def get_transfer_summary():
        """
        Obtiene un resumen general de transferencias, incluyendo estadísticas
        del día y acumuladas.
        """
        today = timezone.now().date()
        
        # Estadísticas del día
        today_transfers = Transfer.objects.filter(created_at__date=today)
        today_stats = today_transfers.aggregate(
            total_transfers=Count('id'),
            total_amount=Sum('instructed_amount'),
            avg_amount=Avg('instructed_amount')
        )

        # Estadísticas acumuladas
        all_transfers = Transfer.objects.all()
        total_stats = all_transfers.aggregate(
            total_transfers=Count('id'),
            total_amount=Sum('instructed_amount'),
            avg_amount=Avg('instructed_amount')
        )

        # Distribución de estados
        status_distribution = Transfer.objects.values('status').annotate(
            count=Count('id'),
            percentage=Count('id') * 100.0 / all_transfers.count()
        ).order_by('-count')

        return {
            'today': {
                'total_transfers': today_stats['total_transfers'] or 0,
                'total_amount': today_stats['total_amount'] or 0,
                'avg_amount': today_stats['avg_amount'] or 0,
            },
            'accumulated': {
                'total_transfers': total_stats['total_transfers'] or 0,
                'total_amount': total_stats['total_amount'] or 0,
                'avg_amount': total_stats['avg_amount'] or 0,
            },
            'status_distribution': status_distribution
        }

    @staticmethod
    def get_user_summary():
        """
        Obtiene un resumen de actividad de usuarios.
        """
        today = timezone.now().date()
        
        return {
            'active_today': UserActivity.objects.filter(date=today).count(),
            'total_users': User.objects.filter(is_active=True).count(),
            'top_users': UserActivity.objects.values('user__username').annotate(
                transfer_count=Sum('transfer_count'),
                total_transfer_amount=Sum('total_transfer_amount')
            ).order_by('-transfer_count')[:5]
        }

    @staticmethod
    def get_transfer_statistics(start_date=None, end_date=None):
        """
        Obtiene estadísticas de transferencias en un rango de fechas.
        """
        queryset = TransferStatistics.objects.all()
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
            
        return queryset

    @staticmethod
    def get_user_statistics(user, start_date=None, end_date=None):
        """
        Obtiene estadísticas de un usuario específico.
        """
        queryset = UserActivity.objects.filter(user=user)
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
            
        return queryset

    @staticmethod
    def get_system_logs(
        level=None,
        action=None,
        user=None,
        start_date=None,
        end_date=None,
        limit=100
    ):
        """
        Obtiene logs del sistema con filtros opcionales.
        """
        queryset = SystemLog.objects.all()
        
        if level:
            queryset = queryset.filter(level=level)
        if action:
            queryset = queryset.filter(action=action)
        if user:
            queryset = queryset.filter(user=user)
        if start_date:
            queryset = queryset.filter(timestamp__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__date__lte=end_date)
            
        return queryset[:limit]

    @staticmethod
    def get_system_logs(limit=10):
        """
        Obtiene los logs más recientes del sistema.
        """
        return SystemLog.objects.all()[:limit] 