from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateCart, name="updatecart"),
    path('process_order/', views.processOrder, name="processorder"),
    path('carts/', views.cartsView, name="carts"),
    path('checkouts/', views.checkoutsView, name="checkouts"),
    path('update_items/', views.UpdateItem, name="updateitem"),
    path('process_view/', views.processDataView, name="processView"),
    
]