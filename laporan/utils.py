from django.db.models.functions import TruncMonth, TruncYear
from django.db.models import Sum
from .models import Pinjaman, Tabungan

def laporan_bulanan_pinjaman():
    return Pinjaman.objects.annotate(
        bulan=TruncMonth('tanggal_pinjaman')
    ).values('anggota__nama', 'bulan').annotate(
        total=Sum('jumlah')
    ).order_by('bulan')

def laporan_tahunan_pinjaman():
    return Pinjaman.objects.annotate(
        tahun=TruncYear('tanggal_pinjaman')
    ).values('anggota__nama', 'tahun').annotate(
        total=Sum('jumlah')
    ).order_by('tahun')

def laporan_bulanan_simpanan():
    return Tabungan.objects.annotate(
        bulan=TruncMonth('tanggal_simpanan')
    ).values('anggota__nama', 'bulan').annotate(
        total=Sum('jumlah')
    ).order_by('bulan')

def laporan_tahunan_simpanan():
    return Tabungan.objects.annotate(
        tahun=TruncYear('tanggal_simpanan')
    ).values('anggota__nama', 'tahun').annotate(
        total=Sum('jumlah')
    ).order_by('tahun')

def total_pinjaman():
    return Pinjaman.objects.aggregate(total=Sum('jumlah'))['total'] or 0

def total_simpanan():
    return Tabungan.objects.aggregate(total=Sum('jumlah'))['total'] or 0
