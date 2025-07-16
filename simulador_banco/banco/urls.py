
from django.urls import path

from banco.api_login import login_api_simulador

from . import views
from . import gpt_views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('transferencia/', views.transfer_view, name='transfer'),
    path('registro/', views.registro_view, name='registro'),
    path('logout/', views.logout_view, name='logout'),
    
    # Gestión de usuarios
    path('usuarios/', views.user_list, name='user_list'),
    path('usuarios/nuevo/', views.user_create, name='user_create'),
    path('usuarios/<int:pk>/editar/', views.user_edit, name='user_edit'),
    path('usuarios/gestion/', views.user_management, name='user_management'),
    path('usuarios/<int:user_id>/toggle/', views.toggle_user_active, name='toggle_user'),
    path('usuarios/<int:user_id>/update_role/', views.update_user_role, name='update_user_role'),
    
    # APIs
    path('api/token', views.generar_token),
    path('oidc/token', views.generar_token),
    path('oidc/authorize', views.oauth2_authorize, name='oauth2_authorize'),
    path('auth/challenges', views.api_challenge),
    path('otp/single', views.api_send_transfer),
    path('payments', views.api_transfer_incoming),
    
    # Transferencias
    path('transferencias/nueva/', views.transfer_view, name='new_transfer'),
    path('transferencias/<str:payment_id>/estado/', views.transfer_status_view, name='transfer_status'),
    path('api/transferencias/estado/<str:payment_id>/', views.api_transfer_status, name='api_transfer_status'),
    
    # Movimientos y estados
    path('cuentas/<int:account_id>/deposito/', views.account_movement_create, {'tipo': 'DEPOSIT'}, name='deposito_cuenta'),
]

urlpatterns += [
    path('api/login/',            views.login_api_simulador,   name='login_api_simulador'),
    path('api/transferencia/',     views.api_send_transfer,     name='api_send_transfer'),
    path('api/transferencia/verify/', views.api_verify_otp,     name='api_verify_otp'),
]