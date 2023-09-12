from django.contrib import admin
from django.urls import path, include
from user.views import *
from .swagger import schema_view

from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('user_create/', CustomUserCreateView.as_view(), name='user_create'),
    path('user_update/', CustomUserUpdateView.as_view(), name='user_update'),
    path('user_get/', CustomUserView.as_view(), name='get_users'),

    path('admin_all_users/', AllUsersView.as_view(), name='admin_all_users'),
    path('admin_one_user/<int:user_id>/', UserView.as_view(), name='admin_one_user'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('send_email/', SendEmailView.as_view(), name='send_email'),
    path('chack_verify_code/<int:verify_code>/', ChackEmailCodeView.as_view(), name='chack_verify_code'),
    path('user_update_password/<str:new_pass>/', UserUpdatePassword.as_view(), name='user_update_password'),

    path('send_support/', SupportPostView.as_view(), name='send_support'),
    path('admin_all_supports/<str:status>/', AllSupportsView.as_view(), name='all_supports'),
    path('admin_one_support/<int:support_id>/', SupportView.as_view(), name='admin_one_support'),
    path('admin_read_support/<int:support_id>/', ReadSupportView.as_view(), name='admin_read_support'),

    path('admin_category_create/', AddCategoryView.as_view(), name='admin_category_create'),
    path('admin_category_update/<int:category_id>/', CategoryUpdateView.as_view(), name='admin_category_update'),
    path('categories/', AllCategoryView.as_view(), name='categories'),

    path('pubg/', include('pubg_accounts.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
