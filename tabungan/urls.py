from django.urls import path
from . import views

app_name = 'tabungan'

urlpatterns = [
    path('', views.daftar_tabungan, name='daftar_tabungan'),
    path('daftar/', views.daftar_tabungan, name='daftar_tabungan'),
    path('tambah/', views.tambah_tabungan, name='tambah_tabungan'),
    path('edit/<int:id>/', views.edit_tabungan, name='edit_tabungan'),
    path('hapus/<int:id>/', views.hapus_tabungan, name='hapus_tabungan'),
    path('form-penarikan/', views.form_penarikan_view, name='form_penarikan'),
    path('ajax/get-nip/', views.get_data_by_nip, name='get_data_by_nip'),
    path('ajax/get-nama/', views.get_data_by_nama, name='get_data_by_nama'),

    # path('history/<int:tabungan_id>/', views.history_tabungan, name='history_tabungan'),
]
