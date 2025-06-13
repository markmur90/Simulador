
from django.urls import path

from banco.api_login import login_api_simulador

from . import views
from . import gpt_views

urlpatterns = [
    path('api/transferencia/', views.recibir_transferencia, name='api_transferencia'),
    path('/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('transferencia/', views.transferencia_view, name='transferencia'),
    path('registro/', views.registro_view, name='registro'),
    path('api/token', views.generar_token),

    path('api/login/', login_api_simulador),
    path('api/challenge', views.api_challenge),
    path('api/transferencias/entrantes/', views.api_transfer_incoming),
    path('api/send-transfer', views.api_send_transfer),
    path('api/status-transfer', views.api_status_transfer),
    path('frontend/transfer', views.transfer_simulator_frontend, name='transfer_simulator_frontend'),

    # GPT4 CRUD
    path('gpt4/deudores/', gpt_views.DebtorListView.as_view(), name='list_debtorsGPT4'),
    path('gpt4/deudores/nuevo/', gpt_views.DebtorCreateView.as_view(), name='create_debtorGPT4'),
    path('gpt4/cuentas-deudor/', gpt_views.DebtorAccountListView.as_view(), name='list_debtor_accountsGPT4'),
    path('gpt4/cuentas-deudor/nuevo/', gpt_views.DebtorAccountCreateView.as_view(), name='create_debtor_accountGPT4'),
    path('gpt4/acreedores/', gpt_views.CreditorListView.as_view(), name='list_creditorsGPT4'),
    path('gpt4/acreedores/nuevo/', gpt_views.CreditorCreateView.as_view(), name='create_creditorGPT4'),
    path('gpt4/cuentas-acreedor/', gpt_views.CreditorAccountListView.as_view(), name='list_creditor_accountsGPT4'),
    path('gpt4/cuentas-acreedor/nuevo/', gpt_views.CreditorAccountCreateView.as_view(), name='create_creditor_accountGPT4'),
    path('gpt4/agentes-acreedor/', gpt_views.CreditorAgentListView.as_view(), name='list_creditor_agentsGPT4'),
    path('gpt4/agentes-acreedor/nuevo/', gpt_views.CreditorAgentCreateView.as_view(), name='create_creditor_agentGPT4'),
    path('gpt4/clientid/nuevo/', gpt_views.ClientIDCreateView.as_view(), name='create_clientidGPT4'),
    path('gpt4/kid/nuevo/', gpt_views.KidCreateView.as_view(), name='create_kidGPT4'),
    path('gpt4/transferencias/', gpt_views.TransferListView.as_view(), name='list_transferGPT4'),
    path('gpt4/transferencias/nuevo/', gpt_views.TransferCreateView.as_view(), name='create_transferGPT4'),
    path('gpt4/transferencias/<str:payment_id>/', gpt_views.TransferDetailView.as_view(), name='transfer_detailGPT4'),
    path('gpt4/transferencias/<str:payment_id>/editar/', gpt_views.TransferUpdateView.as_view(), name='edit_transferGPT4'),
]
