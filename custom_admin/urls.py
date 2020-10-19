from django.urls import path

from . import views

urlpatterns = [

    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('tinymce_image_handler', views.tinymce_image_handler,
         name='tinymce_image_handler'),
    path('page_editor/<slug:page>', views.page_editor, name='page_editor'),
    path('bulk_upload_main', views.bulk_upload_main, name='bulk_upload_main'),
    path('bulk_event_update', views.bulk_event_update, name='bulk_event_update'),
    path('bulk_upload_map', views.bulk_upload_map, name='bulk_upload_map'),
    path('bulk_upload_tool/<slug:data_type>',
         views.bulk_upload_tool, name='bulk_upload_tool'),

]
