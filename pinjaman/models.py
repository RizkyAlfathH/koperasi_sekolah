from django.db import models
from anggota.models import Anggota

class Pinjaman(models.Model):
    id_anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE)
    tanggal_pinjaman = models.DateField()
    
    jumlah_reguler = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    jumlah_usaha = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    jumlah_barang = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    jumlah_bayar = models.DecimalField(max_digits=12, decimal_places=2)
    jatuh_tempo = models.DateField()
    status = models.CharField(max_length=10, default='belum')

    def __str__(self):
        return f"Pinjaman {self.id_anggota}"

    def save(self, *args, **kwargs):
        self.jumlah_bayar = (self.jumlah_reguler or 0) + (self.jumlah_usaha or 0) + (self.jumlah_barang or 0)
        super().save(*args, **kwargs)

class HistoryPembayaran(models.Model):
    id_pinjaman = models.ForeignKey(Pinjaman, on_delete=models.CASCADE)
    tanggal_bayar = models.DateField()
    jumlah_bayar = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Bayar {self.id_pinjaman}"
