from django.urls import path

from . import views

urlpatterns = [

    path('store-admin', views.store_admin, name='store-admin'),
    path('store-order-summary', views.store_order_summary,
         name='store-order-summary'),
    path('store-create', views.store_create, name='store-create'),
    path('store-item/<slug>', views.store_item, name='store-item'),
    path('store-main', views.store_main, name='store-main'),
    path('store-checkout', views.store_checkout, name='store-checkout'),
    path('add-to-cart/<slug>', views.add_to_cart, name='add-to-cart'),
    path('add-single-item-to-cart/<slug>',
         views.add_single_item_to_cart, name='add-single-item-to-cart'),
    path('remove-from-cart/<slug>',
         views.remove_from_cart, name='remove-from-cart'),
    path('remove-single-item-from-cart/<slug>',
         views.remove_single_item_from_cart, name='remove-single-item-from-cart'),
]
