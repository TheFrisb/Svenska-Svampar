from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
    path('', views.shop_home, name='shop-home'),
    path('login-customer/', views.login_customer, name='login-customer'),
    path('check-product-quantity/', views.check_product_quantity, name='check-product-quantity'),
    path('create-order/', views.create_order, name='create-order'),
]
