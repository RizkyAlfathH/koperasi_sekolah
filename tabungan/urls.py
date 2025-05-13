from django.urls import path
from . import views

app_name = 'tabungan'

urlpatterns = [
    path('', views.daftar_tabungan, name='daftar_tabungan'),
    path('daftar/', views.daftar_tabungan, name='daftar_tabungan'),
    path('edit/<int:id>/', views.edit_tabungan, name='edit_tabungan'),
    path('hapus/<int:id>/', views.hapus_tabungan, name='hapus_tabungan'),
]
