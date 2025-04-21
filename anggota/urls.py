# from django.urls import path
# from . import views

# app_name = 'anggota'

# urlpatterns = [
#     path('', views.daftar_anggota, name='daftar'),
#     path('tambah/', views.tambah_anggota, name='tambah'),
#     # path('edit/<int:id>/', views.edit_anggota, name='edit'),
#     # path('hapus/<int:id>/', views.hapus_anggota, name='hapus'),
# ]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='anggota_index'),
]
