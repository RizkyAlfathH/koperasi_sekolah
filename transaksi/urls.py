# transaksi/urls.py
from django.urls import path
from . import views

app_name = 'transaksi'  # <--- INI WAJIB ADA

urlpatterns = [
    path('', views.transaksi_list, name='transaksi_list'),
    path('create/', views.transaksi_create, name='transaksi_create'),
    path('update/<int:pk>/', views.transaksi_update, name='transaksi_update'),
    path('delete/<int:pk>/', views.transaksi_delete, name='transaksi_delete'),
    path('get_nama_anggota/', views.get_nama_anggota, name='get_nama_anggota'),
]
