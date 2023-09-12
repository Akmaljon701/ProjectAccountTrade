from django.urls import path
from .views import *

urlpatterns = [
    path('account_create/', PubgAccountCreateView.as_view(), name='account_create'),
    path('account_add_media/', PubgAccountAddMediaView.as_view(), name='account_create'),
    path('accounts/', PubgAccountsView.as_view(), name='accounts'),
    path('account/<int:account_id>/', PubgAccountView.as_view(), name='account'),
    path('admin_chack_accounts/', PubgAccountsUnderInvestigationView.as_view(), name='admin_chack_accounts'),
]