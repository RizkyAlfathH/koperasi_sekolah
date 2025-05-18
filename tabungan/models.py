from django.db import models
from anggota.models import Anggota


class Tabungan(models.Model):
    jenis_choices = [('pokok', 'Pokok'), ('wajib', 'Wajib'), ('sukarela', 'Sukarela')]

    id_anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE)
    jenis = models.CharField(max_length=20, choices=jenis_choices)
    jumlah_pokok = models.DecimalField(max_digits=12, decimal_places=2)
    jumlah_wajib = models.DecimalField(max_digits=12, decimal_places=2)
    jumlah_sukarela = models.DecimalField(max_digits=12, decimal_places=2, default=0)



    def __str__(self):
        return f"Tabungan {self.id_anggota}"
    
class HistoryTabungan(models.Model):
    id_tabungan = models.ForeignKey(Tabungan, on_delete=models.CASCADE)
    tanggal = models.DateField()
    jenis = models.CharField(max_length=20)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"History {self.id_tabungan}"

