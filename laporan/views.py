from django.shortcuts import render
from .utils import (
    laporan_bulanan_pinjaman, laporan_tahunan_pinjaman,
    laporan_bulanan_simpanan, laporan_tahunan_simpanan,
    total_pinjaman, total_simpanan,
)

def laporan_koperasi(request):
    context = {
        'laporan_bulanan_pinjaman': laporan_bulanan_pinjaman(),
        'laporan_tahunan_pinjaman': laporan_tahunan_pinjaman(),
        'laporan_bulanan_simpanan': laporan_bulanan_simpanan(),
        'laporan_tahunan_simpanan': laporan_tahunan_simpanan(),
        'total_pinjaman': total_pinjaman(),
        'total_simpanan': total_simpanan(),
    }
    return render(request, 'laporan_koperasi.html', context)
