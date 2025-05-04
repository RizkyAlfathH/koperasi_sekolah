from django.shortcuts import render, get_object_or_404, redirect
from .models import Tabungan
from anggota.models import Anggota

def daftar_tabungan(request):
    daftar_tabungan = Tabungan.objects.select_related('id_anggota').all()
    return render(request, 'tabungan/daftar_tabungan.html', {'daftar_tabungan': daftar_tabungan})

def edit_tabungan(request, id):
    tabungan = get_object_or_404(Tabungan, id=id)
    if request.method == 'POST':
        tabungan.jenis = request.POST.get('jenis')
        tabungan.jumlah_pokok = request.POST.get('jumlah_pokok')
        tabungan.jumlah_wajib = request.POST.get('jumlah_wajib')
        tabungan.jumlah_sukarela = request.POST.get('jumlah_sukarela')
        tabungan.save()
        return redirect('tabungan:data_tabungan')
    
    return render(request, 'tabungan/edit_tabungan.html', {'tabungan': tabungan})

def hapus_tabungan(request, id):
    tabungan = get_object_or_404(Tabungan, id=id)
    if request.method == 'POST':
        tabungan.delete()
        return redirect('tabungan:data_tabungan')
    
    return render(request, 'tabungan/hapus_tabungan.html', {'tabungan': tabungan})
