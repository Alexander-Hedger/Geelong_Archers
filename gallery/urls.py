from django.urls import path

from . import views

urlpatterns = [

    path('gallery-admin', views.gallery_admin, name='gallery-admin'),
    path('gallery-create', views.gallery_create, name='gallery-create'),
    path('gallery-delete/<slug:album_id>',
         views.gallery_delete, name='gallery-delete'),
    path('gallery-main', views.gallery_main, name='gallery-main'),
    path('gallery-edit/<int:album_id>',
         views.gallery_edit, name='gallery-edit'),
    path('gallery-album/<int:album_id>',
         views.gallery_album, name='gallery-album'),

]
