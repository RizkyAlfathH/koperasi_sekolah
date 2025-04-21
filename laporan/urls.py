from django.urls import path
from . import views

app_name = 'laporan'

urlpatterns = [
    # path('', views.ringkasan_laporan, name='ringkasan'),
    path('export/', views.export_pdf, name='export_pdf'),
]
