from django.db import models
from anggota.models import Anggota

class Penarikan(models.Model):
    jenis_choices = [('pokok', 'Pokok'), ('wajib', 'Wajib'), ('sukarela', 'Sukarela')]

    id_anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE)
    jenis = models.CharField(max_length=20, choices=jenis_choices)
    jumlah_penarikan = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.jenis} - {self.jumlah_penarikan}"
