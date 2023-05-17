from django.urls import path

from . import views


app_name = 'shopmanager'
urlpatterns = [
    path('', views.shopmanager_home, name='shopmanager-home'),
    path('shopmanager-view-orders/<int:pk>/', views.shopmanager_view_orders, name='shopmanager-view-orders'),
    path('export-orders-as-pdf/<int:pk>/', views.export_orders_as_pdf, name='export-orders-as-pdf'),
    path('register-applicant/', views.register_applicant, name='register-applicant'),
    path('dismiss-applicant/', views.dismiss_applicant, name='dismiss-applicant'),
]
