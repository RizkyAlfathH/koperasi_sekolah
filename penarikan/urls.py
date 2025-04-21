from django.urls import path
from . import views

app_name = 'penarikan'

urlpatterns = [
    path('', views.daftar_penarikan, name='daftar'),
    # path('tambah/', views.tambah_penarikan, name='tambah'),
]
