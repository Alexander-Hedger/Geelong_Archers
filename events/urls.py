from django.urls import path

from . import views

urlpatterns = [

    path('admin', views.events_admin, name='events-admin'),
    path('upcoming_events', views.events_main, name='events-main'),
    path('comp-<int:event_id>', views.comp_listing, name='comp-listing'),
    path('intro-<int:event_id>', views.intro_listing, name='intro-listing'),
    path('create-<slug:event_type>',
         views.events_create, name='events-create'),
]
