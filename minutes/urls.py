from django.urls import path

from . import views

urlpatterns = [

    path('minutes-admin', views.minutes_admin, name='minutes-admin'),
    path('minutes-main', views.minutes_main, name='minutes-main'),
    path('minutes/<slug:minutes_type>/<int:pk>',
         views.minutes_delete, name='minutes_delete'),
    path('minutes/upload',
         views.minutes_upload, name='minutes_upload')
]
