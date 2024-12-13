# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.user_register, name='register'),
    path('login/', views.user_login, name='login'),
    path('update-info/', views.update_user_info, name='update_user_info'),
    path('login-status/', views.get_login_status, name='get_login_status'),
    path('logout/', views.user_logout, name='user_logout'),
    path('user-info/', views.get_user_info, name='get_user_info'),
]
