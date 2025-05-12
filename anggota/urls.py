# anggota/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Halaman utama kelola akun
    path('', views.kelola_akun, name='kelola_akun'),
    path('kelola-akun/', views.kelola_akun, name='kelola_akun'),

    # --- Admin ---
    path('tambah-admin/', views.tambah_admin, name='tambah_admin'),
    path('edit-admin/<int:id_anggota>/', views.edit_admin, name='edit_admin'),
    path('hapus-admin/<int:id_anggota>/', views.hapus_admin, name='hapus_admin'),

    # --- Anggota ---
    path('tambah-anggota/', views.tambah_anggota, name='tambah_anggota'),
    path('edit-anggota/<int:id_anggota>/', views.edit_anggota, name='edit_anggota'),
    path('hapus-anggota/<int:id_anggota>/', views.hapus_anggota, name='hapus_anggota'),
]