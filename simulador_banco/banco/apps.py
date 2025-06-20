from django.apps import AppConfig
from django.contrib.auth.models import Group

class BancoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'banco'

    def ready(self):
        # Ensure default roles/groups exist
        roles = ['Oficial Bancario', 'Supervisor', 'Gerente', 'Administrador']
        for role in roles:
            Group.objects.get_or_create(name=role)