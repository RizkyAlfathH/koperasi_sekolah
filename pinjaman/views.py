from django.shortcuts import render, get_object_or_404, redirect
from .models import Pinjaman, HistoryPembayaran
from .forms import PinjamanForm, HistoryPembayaranForm
from decimal import Decimal
from django.db.models import Sum

def pinjaman_list(request):
    pinjaman_qs = Pinjaman.objects.all()
    pinjaman_list = []
    for p in pinjaman_qs:
        total_pokok = p.jumlah_pinjaman
        bunga = p.bunga

        cicilan_dibayar = HistoryPembayaran.objects.filter(id_pinjaman=p).aggregate(
            total_cicilan=Sum('jumlah_bayar')
        )['total_cicilan'] or Decimal('0.00')

        p.jasa = bunga
        p.total = p.jumlah_cicilan + bunga

        p.total_pokok = total_pokok
        p.cicilan_dibayar = cicilan_dibayar

        pinjaman_list.append(p)

    return render(request, 'pinjaman/pinjaman_list.html', {
        'pinjaman_list': pinjaman_list,
    })


def pinjaman_detail(request, pk):
    pinjaman = get_object_or_404(Pinjaman, pk=pk)
    history = HistoryPembayaran.objects.filter(id_pinjaman=pinjaman).order_by('-tanggal_bayar')
    return render(request, 'pinjaman/pinjaman_detail.html', {
        'pinjaman': pinjaman,
        'history': history,
    })


def tambah_pinjaman(request):
    if request.method == 'POST':
        form = PinjamanForm(request.POST)
        if form.is_valid():
            pinjaman = form.save(commit=False)
            # Set sisa pinjaman sama dengan total bayar (cicilan + bunga)
            pinjaman.sisa_pinjaman = pinjaman.jumlah_bayar
            pinjaman.save()
            return redirect('pinjaman:list')
    else:
        form = PinjamanForm()
    return render(request, 'pinjaman/pinjaman_form.html', {'form': form})


def bayar_pinjaman(request, pk):
    pinjaman = get_object_or_404(Pinjaman, pk=pk)

    total_sudah_bayar = HistoryPembayaran.objects.filter(id_pinjaman=pinjaman).aggregate(
        total=Sum('jumlah_bayar')
    )['total'] or Decimal('0')

    sisa_bayar = pinjaman.jumlah_bayar - total_sudah_bayar
    if sisa_bayar < 0:
        sisa_bayar = Decimal('0')

    if request.method == 'POST':
        form = HistoryPembayaranForm(request.POST)
        if form.is_valid():
            pembayaran = form.save(commit=False)
            pembayaran.id_pinjaman = pinjaman
            pembayaran.save()
            return redirect('pinjaman:detail', pk=pk)
    else:
        form = HistoryPembayaranForm(initial={
            'id_pinjaman': pinjaman,
            'jumlah_bayar': sisa_bayar.quantize(Decimal('0.01')),
        })

    return render(request, 'pinjaman/bayar_pinjaman.html', {
        'form': form,
        'pinjaman': pinjaman,
    })
