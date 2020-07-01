from django.urls import path

from . import views

urlpatterns = [

    path('contact-admin', views.contact_admin, name='contact-admin'),
    path('contact-awards', views.contact_awards, name='contact-awards'),
    path('contact-<slug:contact_type>:<int:event_id>',
         views.contact_events, name='contact-events'),


]
