# from django.urls import path
# from . import views

# app_name = 'anggota'

# urlpatterns = [
#     path('', views.daftar_anggota, name='daftar'),
#     path('tambah/', views.tambah_anggota, name='tambah'),
#     # path('edit/<int:id>/', views.edit_anggota, name='edit'),
#     # path('hapus/<int:id>/', views.hapus_anggota, name='hapus'),
# ]

# anggota/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.kelola_akun, name='kelola_akun'),  # ini yang penting
    path('kelola-akun/', views.kelola_akun, name='kelola_akun'),
#     path('hapus-admin/<int:id_anggota>/', views.hapus_admin, name='hapus_admin'),
#     path('hapus-anggota/<int:id_anggota>/', views.hapus_anggota, name='hapus_anggota'),
]

