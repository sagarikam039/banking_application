from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('account/', views.account_details, name='account'),
    path('deposit/', views.deposit_money, name='deposit'),
    path('withdraw/', views.withdraw_money, name='withdraw'),
    path('transactions/', views.transaction_history, name='transactions'),
]