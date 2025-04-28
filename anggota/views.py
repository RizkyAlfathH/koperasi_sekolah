from django.shortcuts import render, redirect, get_object_or_404
from admin_koperasi.models import Admin  
from .models import Anggota 

def kelola_akun(request):
    admins = Admin.objects.all()
    anggotas = Anggota.objects.all()

    context = {
        'admins': admins,
        'anggotas': anggotas
    }
    return render(request, 'anggota/kelola_akun.html', context)

def hapus_admin(request, id_anggota):
    admin = get_object_or_404(Admin, id_anggota=id_anggota)
    admin.delete()
    return redirect('kelola_akun')

def hapus_anggota(request, id_anggota):
    anggota = get_object_or_404(Anggota, id_anggota=id_anggota)
    anggota.delete()
    return redirect('kelola_akun')



