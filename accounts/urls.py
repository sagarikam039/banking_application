from django.urls import path
from django.contrib import admin
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('account/', views.account_details, name='account'),
    path('deposit/', views.deposit_money, name='deposit'),
    path('withdraw/', views.withdraw_money, name='withdraw'),
    path('api/transactions/', views.transaction_api, name='transaction_api'),
    path('transfer/', views.transfer_money, name='transfer'),
    path('api/accounts/', views.account_api, name='account_api'),
    path('api/deposit/', views.deposit_api, name='deposit_api'),
    path('api/withdraw/', views.withdraw_api, name='withdraw_api'),
    path('api/transfer/', views.transfer_api, name='transfer_api'),
    path('api/register/', views.register_api, name='register_api'),
    path('api/profile/', views.profile_api, name='profile_api'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/risk-analyzer/', views.risk_analyzer_api, name='risk_analyzer_api'),

]