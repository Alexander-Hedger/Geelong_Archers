from django.urls import path

from . import views

urlpatterns = [

    path('dashboard', views.dashboard, name='dashboard'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('account_update', views.account_update, name='account_update'),
]
