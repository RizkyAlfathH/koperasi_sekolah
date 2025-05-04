from django.urls import path
from . import views

app_name = 'pinjaman'

urlpatterns = [
    path('', views.pinjaman_list, name='pinjaman_list'),
    path('detail/<int:pinjaman_id>/', views.pinjaman_detail, name='pinjaman_detail'),
    path('bayar/<int:pinjaman_id>/', views.bayar_pinjaman, name='bayar_pinjaman'),
]
