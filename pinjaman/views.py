from django.shortcuts import render, get_object_or_404, redirect
from .models import Pinjaman, HistoryPembayaran
from .forms import PinjamanForm, HistoryPembayaranForm
from decimal import Decimal
from django.db.models import Sum

def pinjaman_list(request):
    pinjaman_qs = Pinjaman.objects.all()
    pinjaman_list = []

    for p in pinjaman_qs:
        sisa_pokok = p.sisa_pinjaman or Decimal('0')
        bunga = p.jasa_terbaru

        cicilan_dibayar = HistoryPembayaran.objects.filter(id_pinjaman=p).aggregate(
            total_cicilan=Sum('jumlah_bayar')
        )['total_cicilan'] or Decimal('0.00')

        sisa_cicilan = p.jumlah_cicilan - cicilan_dibayar
        if sisa_cicilan < 0:
            sisa_cicilan = Decimal('0.00')

        p.jasa = bunga
        p.cicilan_dibayar = cicilan_dibayar
        p.total_pokok = sisa_pokok
        p.sisa_cicilan = sisa_cicilan
        p.total = p.jumlah_cicilan + bunga

        pinjaman_list.append(p)

    return render(request, 'pinjaman/pinjaman_list.html', {
        'pinjaman_list': pinjaman_list,
    })


def pinjaman_detail(request, pk):
    pinjaman = get_object_or_404(Pinjaman, pk=pk)
    history = HistoryPembayaran.objects.filter(id_pinjaman=pinjaman).order_by('-tanggal_bayar')

    cicilan_dibayar = history.aggregate(total=Sum('jumlah_bayar'))['total'] or Decimal('0.00')

    jasa_terbaru = pinjaman.jasa_terbaru

    total_bayar = cicilan_dibayar + jasa_terbaru 

    return render(request, 'pinjaman/pinjaman_detail.html', {
        'pinjaman': pinjaman,
        'history': history,
        'cicilan_dibayar': cicilan_dibayar,
        'jasa_terbaru': jasa_terbaru,
        'total_bayar': total_bayar,
    })


def tambah_pinjaman(request):
    if request.method == 'POST':
        form = PinjamanForm(request.POST)
        if form.is_valid():
            form.save()  # Gunakan save() dari form yang sudah mengatur semua logika
            return redirect('pinjaman:list')
        else:
            print("Form invalid:", form.errors)  # Debugging error
    else:
        form = PinjamanForm()

    return render(request, 'pinjaman/pinjaman_form.html', {
        'form': form
    })


def bayar_pinjaman(request, pk):
    pinjaman = get_object_or_404(Pinjaman, pk=pk)

    cicilan_per_bulan = Decimal('0')
    if pinjaman.lama_pinjaman:
        cicilan_per_bulan = (pinjaman.jumlah_cicilan / pinjaman.lama_pinjaman).quantize(Decimal('0.01'))

    jasa_terbaru = pinjaman.jasa_terbaru or Decimal('0')
    jumlah_bayar_default = (cicilan_per_bulan + jasa_terbaru).quantize(Decimal('0.01'))

    if request.method == 'POST':
        form = HistoryPembayaranForm(request.POST)
        if form.is_valid():
            pembayaran = form.save(commit=False)
            pembayaran.id_pinjaman = pinjaman
            pembayaran.save()
            return redirect('pinjaman:detail', pk=pk)
    else:
        form = HistoryPembayaranForm(initial={
            'jumlah_bayar': jumlah_bayar_default
        })

    return render(request, 'pinjaman/bayar_pinjaman.html', {
        'form': form,
        'pinjaman': pinjaman
    })
