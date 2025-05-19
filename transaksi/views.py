from django.shortcuts import render, get_object_or_404, redirect
from .models import TransaksiTabungan
from .forms import TransaksiForm
from django.http import JsonResponse
from tabungan.models import Tabungan
from anggota.models import Anggota

def transaksi_list(request):
    transaksis = TransaksiTabungan.objects.all()
    return render(request, 'transaksi/transaksi_list.html', {'transaksi_list': transaksis})

def transaksi_create(request):
    if request.method == 'POST':
        form = TransaksiForm(request.POST)
        if form.is_valid():
            nip = form.cleaned_data['anggota']  # nip, bukan id
            try:
                anggota = Anggota.objects.get(nip=nip)
                tabungan = Tabungan.objects.get(id_anggota=anggota.id_anggota)
            except (Anggota.DoesNotExist, Tabungan.DoesNotExist):
                form.add_error('anggota', 'Anggota atau tabungan tidak ditemukan.')
                return render(request, 'transaksi/form.html', {'form': form, 'form_title': 'Tambah Transaksi'})

            transaksi = form.save(commit=False)
            transaksi.tabungan = tabungan
            transaksi.save()
            return redirect('transaksi_list')
    else:
        form = TransaksiForm()
    return render(request, 'transaksi/form.html', {'form': form, 'form_title': 'Tambah Transaksi'})

def transaksi_update(request, pk):
    transaksi = get_object_or_404(TransaksiTabungan, pk=pk)
    if request.method == 'POST':
        form = TransaksiForm(request.POST, instance=transaksi)
        if form.is_valid():
            form.save()
            return redirect('transaksi_list')
    else:
        form = TransaksiForm(instance=transaksi)
    return render(request, 'transaksi/form.html', {'form': form, 'form_title': 'Edit Transaksi'})

def transaksi_delete(request, pk):
    transaksi = get_object_or_404(TransaksiTabungan, pk=pk)
    if request.method == 'POST':
        transaksi.delete()
        return redirect('transaksi_list')
    return render(request, 'transaksi/confirm_delete.html', {'transaksi': transaksi})

def get_nama_anggota(request):
    anggota_id = request.GET.get('id')
    try:
        anggota = Anggota.objects.get(pk=anggota_id)
        return JsonResponse({'nama': anggota.nama})
    except Anggota.DoesNotExist:
        return JsonResponse({'nama': ''})

