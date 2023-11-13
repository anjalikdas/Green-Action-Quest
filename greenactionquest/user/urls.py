from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('home/', views.home, name='home'),
    path('carbon_calculator/', views.carbon_calculator, name='carbon_calculator'),
    path('challenges/', views.challenges_page, name='challenges_page')
]