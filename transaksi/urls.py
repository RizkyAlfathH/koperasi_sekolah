from django.urls import path
from . import views

app_name = 'transaksi'

urlpatterns = [
    path('', views.histori_transaksi, name='histori'),
]
