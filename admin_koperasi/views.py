from django.shortcuts import render, redirect
from admin_koperasi.models import Admin
from anggota.models import Anggota

def dashboard_ketua(request):
    total_anggota = Anggota.objects.count()
    total_admin = Admin.objects.count()

    return render(request, 'admin_koperasi/dashboard_ketua.html', {
        'total_anggota': total_anggota,
        'total_admin': total_admin,
    })

def dashboard_sekertaris(request):
    return render(request, 'admin_koperasi/dashboard_sekertaris.html')

def dashboard_bendahara(request):
    return render(request, 'admin_koperasi/dashboard_bendahara.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Admin.objects.get(username=username)

            if user.check_password(password):
                request.session['admin_id'] = user.id
                request.session['admin_role'] = user.role

                if user.role == 'ketua':
                    return redirect('dashboard_ketua')
                elif user.role == 'sekretaris':
                    return redirect('dashboard_sekertaris')
                elif user.role == 'bendahara':
                    return redirect('dashboard_bendahara')
                else:
                    return redirect('default_dashboard')
            else:
                return render(request, 'admin_koperasi/login.html', {'error': 'Username atau password salah.'})

        except Admin.DoesNotExist:
            return render(request, 'admin_koperasi/login.html', {'error': 'Username atau password salah.'})

    return render(request, 'admin_koperasi/login.html')
