from django.db import models
from anggota.models import Anggota

class SHU(models.Model):
    id_anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE)
    tahun = models.PositiveIntegerField()
    jumlah_shu_simpanan = models.DecimalField(max_digits=12, decimal_places=2)
    jumlah_shu_pinjaman = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"SHU {self.id_anggota} - {self.tahun}"
