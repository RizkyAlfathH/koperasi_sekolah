from django.shortcuts import render, get_object_or_404, redirect
from .models import Pinjaman, HistoryPembayaran
from django.http import HttpResponse

def pinjaman_list(request):
    pinjaman_list = Pinjaman.objects.all()
    return render(request, 'pinjaman/pinjaman_list.html', {'pinjaman_list': pinjaman_list})

def pinjaman_detail(request, pinjaman_id):
    pinjaman = get_object_or_404(Pinjaman, id=pinjaman_id)
    return render(request, 'pinjaman/pinjaman_detail.html', {'pinjaman': pinjaman})

def bayar_pinjaman(request, pinjaman_id):
    pinjaman = get_object_or_404(Pinjaman, id=pinjaman_id)
    
    if request.method == 'POST':
        jumlah_bayar = request.POST['jumlah_bayar']
        metode_pembayaran = request.POST['metode_pembayaran']
        
        # Simpan riwayat pembayaran
        pembayaran = HistoryPembayaran(
            id_pinjaman=pinjaman,
            tanggal_bayar=request.POST.get('tanggal_bayar', pinjaman.tanggal_pinjaman),
            jumlah_bayar=jumlah_bayar,
            metode_pembayaran=metode_pembayaran
        )
        pembayaran.save()

        # Update status pinjaman jika sudah lunas
        if pinjaman.jumlah_bayar <= pinjaman.jumlah_pinjaman:
            pinjaman.status = 'lunas'
            pinjaman.save()

        return redirect('pinjaman_detail', pinjaman_id=pinjaman.id)
    
    return render(request, 'pinjaman/bayar_pinjaman.html', {'pinjaman': pinjaman})
