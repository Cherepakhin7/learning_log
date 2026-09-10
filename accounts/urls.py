"""Определяет схемы url для пользователей"""
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

app_name = "accounts"
urlpatterns = [
    #Добавить url авторизации по улолчанию
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('', include('django.contrib.auth.urls')),
    #Страница регистрации
    path("register/",views.register,name = "register"),
]