# pinjaman/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Pinjaman, HistoryPembayaran
from .forms import PinjamanForm, HistoryPembayaranForm
from decimal import Decimal


def pinjaman_list(request):
    pinjaman_qs = Pinjaman.objects.all()

    pinjaman_list = []
    for p in pinjaman_qs:
        total_pokok = (p.jumlah_reguler or Decimal('0')) + (p.jumlah_usaha or Decimal('0')) + (p.jumlah_barang or Decimal('0'))
        
        # Hitung jasa 10% dari total pokok
        jasa = total_pokok * Decimal('0.1')

        p.jasa = jasa
        p.total = total_pokok + jasa

        pinjaman_list.append(p)

    context = {
        'pinjaman_list': pinjaman_list,
    }
    return render(request, 'pinjaman/pinjaman_list.html', context)

def pinjaman_detail(request, pk):
    pinjaman = get_object_or_404(Pinjaman, pk=pk)
    history = HistoryPembayaran.objects.filter(id_pinjaman=pinjaman)
    return render(request, 'pinjaman/pinjaman_detail.html', {
        'pinjaman': pinjaman,
        'history': history
    })

def tambah_pinjaman(request):
    if request.method == 'POST':
        form = PinjamanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pinjaman:list')
    else:
        form = PinjamanForm()
    return render(request, 'pinjaman/pinjaman_form.html', {'form': form})

def bayar_pinjaman(request, pk):
    pinjaman = get_object_or_404(Pinjaman, pk=pk)
    if request.method == 'POST':
        form = HistoryPembayaranForm(request.POST)
        if form.is_valid():
            pembayaran = form.save(commit=False)
            pembayaran.id_pinjaman = pinjaman
            pembayaran.save()
            return redirect('pinjaman:detail', pk=pk)
    else:
        form = HistoryPembayaranForm(initial={'id_pinjaman': pinjaman})
    return render(request, 'pinjaman/bayar_pinjaman.html', {'form': form, 'pinjaman': pinjaman})
