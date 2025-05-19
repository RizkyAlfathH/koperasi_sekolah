# pinjaman/urls.py
from django.urls import path
from . import views

app_name = 'pinjaman'

urlpatterns = [
    path('', views.pinjaman_list, name='list'),
    path('tambah/', views.tambah_pinjaman, name='tambah'),
    path('<int:pk>/', views.pinjaman_detail, name='detail'),
    path('<int:pk>/bayar/', views.bayar_pinjaman, name='bayar'),
]
