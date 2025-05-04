from django.shortcuts import render, redirect
from .models import SHU
from anggota.models import Anggota

def list_shu(request):
    shu_list = SHU.objects.all()
    return render(request, 'shu/list_shu.html', {'shu_list': shu_list})

def add_shu(request):
    if request.method == 'POST':
        id_anggota = request.POST['id_anggota']
        tahun = request.POST['tahun']
        jumlah_shu_simpanan = request.POST['jumlah_shu_simpanan']
        jumlah_shu_pinjaman = request.POST['jumlah_shu_pinjaman']
        SHU.objects.create(id_anggota_id=id_anggota, tahun=tahun,
                           jumlah_shu_simpanan=jumlah_shu_simpanan,
                           jumlah_shu_pinjaman=jumlah_shu_pinjaman)
        return redirect('shu:list_shu')
    
    anggota_list = Anggota.objects.all()
    return render(request, 'shu/add_shu.html', {'anggota_list': anggota_list})

def edit_shu(request, id):
    shu = SHU.objects.get(id=id)
    if request.method == 'POST':
        shu.id_anggota_id = request.POST['id_anggota']
        shu.tahun = request.POST['tahun']
        shu.jumlah_shu_simpanan = request.POST['jumlah_shu_simpanan']
        shu.jumlah_shu_pinjaman = request.POST['jumlah_shu_pinjaman']
        shu.save()
        return redirect('shu:list_shu')
    
    anggota_list = Anggota.objects.all()
    return render(request, 'shu/edit_shu.html', {'shu': shu, 'anggota_list': anggota_list})

def delete_shu(request, id):
    SHU.objects.get(id=id).delete()
    return redirect('shu:list_shu')
