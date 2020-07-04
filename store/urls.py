from django.urls import path
from . import views

#Leave as empty string for base url
#urlpatterns extension from root url.py
urlpatterns = [
  path('', views.store, name="store"),
  path('cart/', views.cart, name="cart"),
  path('checkout/', views.checkout, name="checkout")
]