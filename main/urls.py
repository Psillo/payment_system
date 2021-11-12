from django.urls import path
from django.contrib.auth import views

from .views import (
    register, bank_accounts, transfers, create_bank_account,
    bank_account_info, statistics_of_incoming_transfers,
    outbound_transfers_statistics
)


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('register/', register, name='register'),
    path('', bank_accounts, name='bank_accounts'),
    path('bank_account_info/<int:id>/',
         bank_account_info, name='bank_account_info'),
    path('create_bank_account/', create_bank_account,
         name='create_bank_account'),
    path('transfers/', transfers, name='transfers'),
    path('statistics_of_incoming_transfers/',
         statistics_of_incoming_transfers,
         name='statistics_of_incoming_transfers'),
    path('outbound_transfers_statistics/',
         outbound_transfers_statistics,
         name='outbound_transfers_statistics'),
]
