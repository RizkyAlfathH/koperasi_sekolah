from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/ketua/', views.dashboard_ketua, name='dashboard_ketua'),
    path('dashboard/sekretaris/', views.dashboard_sekertaris, name='dashboard_sekertaris'),
    path('dashboard/bendahara/', views.dashboard_bendahara, name='dashboard_bendahara'),
    path('login/', views.login_view, name='login'),
]
