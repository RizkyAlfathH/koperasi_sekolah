from django.urls import path
from . import views

app_name = 'transaksi'

urlpatterns = [
    path('', views.transaksi_list, name='transaksi_list'),
    path('tambah/', views.transaksi_create, name='transaksi_create'),
    path('edit/<int:pk>/', views.transaksi_update, name='transaksi_update'),
    path('hapus/<int:pk>/', views.transaksi_delete, name='transaksi_delete'),
]
