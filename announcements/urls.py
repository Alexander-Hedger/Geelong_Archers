from django.urls import path

from . import views

urlpatterns = [

    path('announcements-main', views.announcements_main, name='announcements-main'),
    path('announcements-create', views.announcements_create,
         name='announcements-create'),
    path('announcements-admin', views.announcements_admin,
         name='announcements-admin'),
    path('announcements-edit:<int:announcement_id>', views.announcements_edit,
         name='announcements-edit'),
    path('announcements-delete:<int:announcement_id>', views.announcements_delete,
         name='announcements-delete'),

]
