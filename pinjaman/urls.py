from django.urls import path
from . import views

app_name = 'pinjaman'

urlpatterns = [
    path('', views.daftar_pinjaman, name='daftar'),
    path('bayar/<int:pinjaman_id>/', views.bayar_cicilan, name='bayar_cicilan'),
]
