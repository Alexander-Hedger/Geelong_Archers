from django.urls import path

from . import views

urlpatterns = [

    path('store-admin', views.store_admin, name='store-admin'),
    path('store-create', views.store_create, name='store-create'),
    path('store-item/<slug>', views.store_item, name='store-item'),
    path('store-main', views.store_main, name='store-main'),
    path('add-to-cart/<slug>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>',
         views.remove_from_cart, name='remove-from-cart'),
]
