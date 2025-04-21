from django.urls import path
from . import views

app_name = 'shu'

urlpatterns = [
    path('', views.hasil_shu, name='hasil_shu'),
]
