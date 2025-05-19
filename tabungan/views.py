from django.shortcuts import render, get_object_or_404, redirect
from .models import Tabungan
from anggota.models import Anggota
from .models import Tabungan, HistoryTabungan
from django.utils.dateparse import parse_date
from django.db.models import Max

def daftar_tabungan(request):
    daftar_tabungan = Tabungan.objects.select_related('id_anggota').all()
    return render(request, 'tabungan/daftar_tabungan.html', {'daftar_tabungan': daftar_tabungan})

def daftar_tabungan(request):
    urutan = request.GET.get('urut', 'nama')

    if urutan == 'transaksi':
        daftar_tabungan = (
            Tabungan.objects.select_related('id_anggota')
            .annotate(terakhir_transaksi=Max('tabungan__tanggal'))
            .order_by('-terakhir_transaksi')  # urut berdasarkan transaksi terbaru
        )
    elif urutan == 'terbaru':
        daftar_tabungan = Tabungan.objects.select_related('id_anggota').order_by('-id')
    else:
        daftar_tabungan = Tabungan.objects.select_related('id_anggota').order_by('id_anggota__nama')

    return render(request, 'tabungan/daftar_tabungan.html', {'daftar_tabungan': daftar_tabungan})

def edit_tabungan(request, id):
    tabungan = get_object_or_404(Tabungan, id=id)
    if request.method == 'POST':
        tabungan.jenis = request.POST.get('jenis')
        tabungan.jumlah_pokok = request.POST.get('jumlah_pokok')
        tabungan.jumlah_wajib = request.POST.get('jumlah_wajib')
        tabungan.jumlah_sukarela = request.POST.get('jumlah_sukarela')
        tabungan.save()
        return redirect('tabungan:daftar_tabungan')    
    return render(request, 'tabungan/edit_tabungan.html', {'tabungan': tabungan})

def hapus_tabungan(request, id):
    tabungan = get_object_or_404(Tabungan, id=id)
    if request.method == 'POST':
        tabungan.delete()
        return redirect('tabungan:daftar_tabungan')   
    return render(request, 'tabungan/hapus_tabungan.html', {'tabungan': tabungan})

from decimal import Decimal  # Tambahkan ini di atas

def tambah_tabungan(request):
    anggota_list = Anggota.objects.all()

    if request.method == 'POST':
        nip = request.POST.get('nip')
        jenis = request.POST.get('jenis')
        jumlah = request.POST.get('jumlah')
        tanggal = parse_date(request.POST.get('tanggal'))

        anggota = get_object_or_404(Anggota, nip=nip)
        jumlah_decimal = Decimal(jumlah)  # Ganti float ke Decimal

        # get_or_create dengan nilai default jika objek baru
        tabungan, created = Tabungan.objects.get_or_create(
            id_anggota=anggota,
            defaults={
                'jumlah_pokok': 0,
                'jumlah_wajib': 0,
                'jumlah_sukarela': 0
            }
        )

        # Tambah saldo sesuai jenis
        if jenis == 'pokok':
            tabungan.jumlah_pokok += jumlah_decimal
        elif jenis == 'wajib':
            tabungan.jumlah_wajib += jumlah_decimal
        elif jenis == 'sukarela':
            tabungan.jumlah_sukarela += jumlah_decimal

        tabungan.save()

        # Catat ke history
        HistoryTabungan.objects.create(
            id_tabungan=tabungan,
            tanggal=tanggal,
            jenis=jenis,
            jumlah=jumlah_decimal
        )

        return redirect('tabungan:daftar_tabungan')

    return render(request, 'tabungan/form_tabungan.html', {'anggota_list': anggota_list})

