from django.urls import path
from . import views

app_name = 'tabungan'

urlpatterns = [
    path('', views.daftar_tabungan, name='daftar'),
    # path('tambah/', views.tambah_tabungan, name='tambah'),
]
