from django.db import models

class Anggota(models.Model):
    nama = models.CharField(max_length=100)

    def __str__(self):
        return self.nama

class Pinjaman(models.Model):
    anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)
    tanggal_pinjaman = models.DateField()

    def __str__(self):
        return f"Pinjaman {self.anggota.nama} - {self.jumlah}"

class Tabungan(models.Model):
    anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)
    tanggal_simpanan = models.DateField()

    def __str__(self):
        return f"Tabungan {self.anggota.nama} - {self.jumlah}"
