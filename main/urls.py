from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('', views.index, name='index'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),
    path('buy/', views.buy, name='buy'),
    path('barter/', views.barter, name='barter'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('inbox/', views.inbox_view, name='inbox'),
]