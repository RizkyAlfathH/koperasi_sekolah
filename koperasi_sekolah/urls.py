"""
URL configuration for koperasi_sekolah project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from admin_koperasi import views as admin_views  # Import views dari admin_koperasi

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', admin_views.login_view, name='login'),  # Langsung ke login_view
    path('admin-koperasi/', include('admin_koperasi.urls')),
    path('anggota/', include('anggota.urls')),
    path('tabungan/', include('tabungan.urls')),
    path('pinjaman/', include('pinjaman.urls')),
    path('transaksi/', include('transaksi.urls')),
    path('penarikan/', include('penarikan.urls')),
    path('shu/', include('shu.urls')),
    path('laporan/', include('laporan.urls')),
]



