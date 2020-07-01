from django.urls import path

from . import views

urlpatterns = [

    path('awards-main', views.awards_main, name='awards-main'),
    path('awards-sub', views.awards_sub, name='awards-sub'),

]
