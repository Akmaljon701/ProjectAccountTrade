from django.contrib import admin
from django.urls import path, include
from .swagger import schema_view

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('api/', include('user.urls')),
    path('pubg/', include('pubg_accounts.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
