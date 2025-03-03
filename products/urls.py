from django.urls import path, re_path
from .views import all_products

urlpatterns = [
    path('', all_products, name='products')
    ]