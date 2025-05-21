from django.shortcuts import render, redirect
from admin_koperasi.models import Admin

def dashboard_ketua(request):
    return render(request, 'admin_koperasi/dashboard_ketua.html')

def dashboard_sekertaris(request):
    return render(request, 'admin_koperasi/dashboard_sekertaris.html')

def dashboard_bendahara(request):
    return render(request, 'admin_koperasi/dashboard_bendahara.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Cari user di database
            user = Admin.objects.get(username=username)

            # Cek password (pakai check_password dari model Admin)
            if user.check_password(password):
                # Simpan info login di session manual
                request.session['admin_id'] = user.id
                request.session['admin_role'] = user.role

                # Arahkan ke dashboard sesuai role
                if user.role == 'ketua':
                    return redirect('dashboard_ketua')
                elif user.role == 'sekretaris':
                    return redirect('dashboard_sekertaris')
                elif user.role == 'bendahara':
                    return redirect('dashboard_bendahara')
                else:
                    return redirect('default_dashboard')
            else:
                # Password salah
                return render(request, 'admin_koperasi/login.html', {'error': 'Username atau password salah.'})

        except Admin.DoesNotExist:
            # Username tidak ditemukan
            return render(request, 'admin_koperasi/login.html', {'error': 'Username atau password salah.'})

    return render(request, 'admin_koperasi/login.html')