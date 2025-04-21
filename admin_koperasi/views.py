from django.shortcuts import render

def login_view(request):
    return render(request, 'admin_koperasi/login.html')

def dashboard_ketua(request):
    return render(request, 'admin_koperasi/dashboard_ketua.html')

def dashboard_sekretaris(request):
    return render(request, 'admin_koperasi/dashboard_sekretaris.html')

def dashboard_bendahara(request):
    return render(request, 'admin_koperasi/dashboard_bendahara.html')
