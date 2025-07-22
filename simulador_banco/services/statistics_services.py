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
    def get_transfer_summary():
        """
        Obtiene un resumen general de transferencias.
        """
        today = timezone.now().date()
        
        return {
            'today': TransferStatistics.objects.filter(date=today).first(),
            'total_transfers': Transfer.objects.count(),
            'total_amount': Transfer.objects.aggregate(total=Sum('instructed_amount'))['total'] or 0,
            'avg_amount': Transfer.objects.aggregate(avg=Avg('instructed_amount'))['avg'] or 0,
            'status_distribution': Transfer.objects.values('status').annotate(
                count=Count('id')
            ).order_by('-count')
        }

    @staticmethod
    def get_user_summary():
        """
        Obtiene un resumen de actividad de usuarios.
        """
        today = timezone.now().date()
        
        return {
            'total_users': User.objects.count(),
            'active_today': UserActivity.objects.filter(date=today).count(),
            'top_users': UserActivity.objects.filter(date=today).order_by(
                '-transfer_count'
            )[:5],
            'recent_activities': UserActivity.objects.select_related('user').order_by(
                '-last_activity'
            )[:10]
        } 