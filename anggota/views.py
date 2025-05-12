from django.shortcuts import render, redirect, get_object_or_404
from admin_koperasi.models import Admin
from .models import Anggota
from .forms import AdminForm, AnggotaForm


def kelola_akun(request):
    admins = Admin.objects.all()
    anggotas = Anggota.objects.all()

    context = {
        'admins': admins,
        'anggotas': anggotas
    }
    return render(request, 'anggota/kelola_akun.html', context)


# ======================== ADMIN ========================
def tambah_admin(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kelola_akun')
    else:
        form = AdminForm()
    return render(request, 'anggota/form_admin.html', {'form': form, 'judul': 'Tambah Admin'})

def edit_admin(request, id_anggota):
    admin = get_object_or_404(Admin, id_anggota=id_anggota)
    form = AdminForm(request.POST or None, instance=admin)
    if form.is_valid():
        form.save()
        return redirect('kelola_akun')
    return render(request, 'anggota/form_admin.html', {'form': form, 'judul': 'Edit Admin'})

def hapus_admin(request, id_anggota):
    admin = get_object_or_404(Admin, id_anggota=id_anggota)
    admin.delete()
    return redirect('kelola_akun')

# ======================== ANGGOTA ========================


def tambah_anggota(request):
    if request.method == 'POST':
        form = AnggotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kelola_akun')
    else:
        form = AnggotaForm()
    return render(request, 'anggota/form_anggota.html', {'form': form, 'judul': 'Tambah Anggota'})


def edit_anggota(request, id_anggota):
    anggota = get_object_or_404(Anggota, id_anggota=id_anggota)
    form = AnggotaForm(request.POST or None, instance=anggota)
    if form.is_valid():
        form.save()
        return redirect('kelola_akun')
    return render(request, 'anggota/form_anggota.html', {'form': form, 'judul': 'Edit Anggota'})


def hapus_anggota(request, id_anggota):
    anggota = get_object_or_404(Anggota, id_anggota=id_anggota)
    anggota.delete()
    return redirect('kelola_akun')