# backend/catalog/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.get_products),
    path('rfq/', views.submit_rfq),
]