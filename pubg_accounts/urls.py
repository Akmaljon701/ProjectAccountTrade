from django.urls import path
from .views import *

urlpatterns = [
    path('account_create/', PubgAccountCreateView.as_view(), name='account_create'),
    path('account_add_media/', PubgAccountAddMediaView.as_view(), name='account_create'),
    path('accounts/', PubgAccountsView.as_view(), name='accounts'),
    path('account/', PubgAccountView.as_view(), name='account'),
    path('admin_chack_accounts/', PubgAccountsUnderInvestigationView.as_view(), name='admin_chack_accounts'),
    path('admin_chack_account/', PubgAccountUnderInvestigationView.as_view(), name='admin_chack_account'),
    path('admin_account_change_type/', AdminPubgAccountUnderInvestigationView.as_view(), name='admin_account_change_type'),
]