from django.db import models
from tabungan.models import Tabungan

class TransaksiTabungan(models.Model):
    id_tabungan = models.ForeignKey(Tabungan, on_delete=models.CASCADE)
    tanggal = models.DateField()
    jenis_transaksi = models.CharField(max_length=20)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)
    keterangan = models.TextField()

    def __str__(self):
        return f"Transaksi {self.id_tabungan} - {self.jenis_transaksi}"