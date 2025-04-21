from django.db import models
from anggota.models import Anggota

class Pinjaman(models.Model):
    kategori_choices = [('harian', 'Harian'), ('bulanan', 'Bulanan'), ('besar', 'Besar')]

    id_anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE)
    tanggal_pinjaman = models.DateField()
    kategori = models.CharField(max_length=20, choices=kategori_choices)
    jumlah_pinjaman = models.DecimalField(max_digits=12, decimal_places=2)
    bunga = models.DecimalField(max_digits=5, decimal_places=2)
    jumlah_bayar = models.DecimalField(max_digits=12, decimal_places=2)
    jatuh_tempo = models.DateField()
    status = models.CharField(max_length=10, default='belum')  # belum/lunas

    def __str__(self):
        return f"Pinjaman {self.id_anggota}"

class HistoryPembayaran(models.Model):
    id_pinjaman = models.ForeignKey(Pinjaman, on_delete=models.CASCADE)
    tanggal_bayar = models.DateField()
    jumlah_bayar = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Bayar {self.id_pinjaman}"
