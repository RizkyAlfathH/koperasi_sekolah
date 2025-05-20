from django.shortcuts import render, get_object_or_404, redirect
from .models import Tabungan
from anggota.models import Anggota
from .models import Tabungan, HistoryTabungan
from django.utils.dateparse import parse_date
from django.db.models import Max
from django.http import JsonResponse
from .forms import PenarikanForm
from django.utils import timezone

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

def form_penarikan_view(request):
    form = PenarikanForm()
    return render(request, 'tabungan/form_penarikan.html', {'form': form})


def get_data_by_nip(request):
    nip = request.GET.get('nip')
    try:
        anggota = Anggota.objects.get(nip=nip)
        tabungan = Tabungan.objects.get(id_anggota=anggota)
        return JsonResponse({
            'nama': anggota.nama,
            'pokok': float(tabungan.jumlah_pokok),
            'wajib': float(tabungan.jumlah_wajib),
            'sukarela': float(tabungan.jumlah_sukarela)
        })
    except Anggota.DoesNotExist:
        return JsonResponse({'error': 'Anggota tidak ditemukan'}, status=404)
    except Tabungan.DoesNotExist:
        return JsonResponse({'error': 'Tabungan tidak ditemukan'}, status=404)
    
def get_data_by_nama(request):
    nama = request.GET.get('nama')
    try:
        anggota = Anggota.objects.get(nama__iexact=nama)
        tabungan = Tabungan.objects.get(id_anggota=anggota)
        return JsonResponse({
            'nip': anggota.nip,
            'pokok': float(tabungan.jumlah_pokok),
            'wajib': float(tabungan.jumlah_wajib),
            'sukarela': float(tabungan.jumlah_sukarela)
        })
    except Anggota.DoesNotExist:
        return JsonResponse({'error': 'Anggota tidak ditemukan'}, status=404)
    except Tabungan.DoesNotExist:
        return JsonResponse({'error': 'Tabungan tidak ditemukan'}, status=404)
    
def form_penarikan_view(request):
    if request.method == 'POST':
        form = PenarikanForm(request.POST)
        if form.is_valid():
            nip = form.cleaned_data['nip']
            jumlah = form.cleaned_data['jumlah']

            try:
                anggota = Anggota.objects.get(nip=nip)
                tabungan = Tabungan.objects.get(id_anggota=anggota)

                if jumlah > tabungan.jumlah_sukarela:
                    form.add_error('jumlah', 'Saldo sukarela tidak mencukupi.')
                else:
                    # Update saldo
                    tabungan.jumlah_sukarela -= jumlah
                    tabungan.save()

                    # Simpan ke HistoryTabungan
                    HistoryTabungan.objects.create(
                        id_tabungan=tabungan,
                        tanggal=timezone.now().date(),
                        jenis='penarikan',
                        jumlah=jumlah
                    )

                    return redirect('tabungan:daftar_tabungan')

            except Anggota.DoesNotExist:
                form.add_error('nip', 'Anggota tidak ditemukan.')
            except Tabungan.DoesNotExist:
                form.add_error(None, 'Data tabungan tidak ditemukan.')

    else:
        form = PenarikanForm()

    anggota_list = Anggota.objects.all()
    return render(request, 'tabungan/form_penarikan.html', {
        'form': form,
        'anggota_list': anggota_list
    })

