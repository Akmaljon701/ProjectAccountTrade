from django.urls import path
from .views import *

urlpatterns = [
    path('account_create/', PubgAccountCreateView.as_view(), name='account_create'),
    path('account_add_media/', PubgAccountAddMediaView.as_view(), name='account_create'),
]