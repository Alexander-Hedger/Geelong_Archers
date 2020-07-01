from django.urls import path

from . import views

urlpatterns = [

    path('admin', views.events_admin, name='events-admin'),
    path('upcoming_events', views.events_main, name='events-main'),
    path('<slug:event_type>:<int:event_id>',
         views.events_listing, name='events-listing'),
    path('create-<slug:event_type>',
         views.events_create, name='events-create'),
]
