from django.urls import path, include
from user.views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user_create/', CustomUserCreateView.as_view(), name='user_create'),
    path('user_update/', CustomUserUpdateView.as_view(), name='user_update'),
    path('user_get/', CustomUserView.as_view(), name='get_users'),

    path('admin_all_users/', AllUsersView.as_view(), name='admin_all_users'),
    path('admin_one_user/', UserView.as_view(), name='admin_one_user'),

    path('send_email/', SendEmailView.as_view(), name='send_email'),
    path('chack_verify_code/', ChackEmailCodeView.as_view(), name='chack_verify_code'),
    path('user_update_password/', UserUpdatePassword.as_view(), name='user_update_password'),

    path('send_support/', SupportPostView.as_view(), name='send_support'),
    path('admin_all_supports/', AllSupportsView.as_view(), name='all_supports'),
    path('admin_one_support/', SupportView.as_view(), name='admin_one_support'),
    path('admin_read_support/', ReadSupportView.as_view(), name='admin_read_support'),

    path('admin_category_create/', AddCategoryView.as_view(), name='admin_category_create'),
    path('admin_category_update/', CategoryUpdateView.as_view(), name='admin_category_update'),
    path('admin_category_delete/', CategoryDeleteView.as_view(), name='admin_category_delete'),
    path('categories/', AllCategoryView.as_view(), name='categories'),

]
