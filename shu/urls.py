from django.urls import path
from . import views

app_name = 'shu'

urlpatterns = [
    path('', views.list_shu, name='list_shu'),
    path('add/', views.add_shu, name='add_shu'),
    path('edit/<int:id>/', views.edit_shu, name='edit_shu'),
    path('delete/<int:id>/', views.delete_shu, name='delete_shu'),
]
