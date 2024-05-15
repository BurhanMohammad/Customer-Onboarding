from django.urls import path
from . import views

urlpatterns = [
    path('create', views.create_customer, name='create_customer'),
    path('upload_document/<int:customer_id>/', views.upload_document, name='upload_document'),
    path('list', views.list_customers, name='list_customers'),
]
