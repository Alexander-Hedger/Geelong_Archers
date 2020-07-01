from django.urls import path

from . import views

urlpatterns = [

    path('rankings-main', views.rankings_main, name='rankings-main'),

]
