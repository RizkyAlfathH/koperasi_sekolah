from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Anggota(models.Model):
    nip = models.CharField(max_length=20, unique=True)
    nama = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nip} - {self.nama}"

class Tabungan(models.Model):
    anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE)
    saldo = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Tabungan {self.anggota.nip}"

class TransaksiTabungan(models.Model):
    JENIS_TRANSAKSI = [
        ('simpan', 'Simpan'),
        ('pinjam', 'Pinjam'),
        ('penarikan', 'Penarikan'),
    ]

    tabungan = models.ForeignKey(Tabungan, on_delete=models.CASCADE)
    tanggal = models.DateField(default=timezone.now)
    jenis = models.CharField(max_length=10, choices=JENIS_TRANSAKSI, default='simpan')
    jumlah = models.PositiveIntegerField()
    keterangan = models.TextField(blank=True)

    def clean(self):
        # Validasi saldo cukup untuk pinjam dan penarikan
        if self.jenis in ['pinjam', 'penarikan'] and self.tabungan:
            if self.jumlah > self.tabungan.saldo:
                raise ValidationError("Saldo tidak mencukupi untuk transaksi ini.")

    def save(self, *args, **kwargs):
        self.clean()  # Pastikan validasi dijalankan sebelum save
        is_new = self.pk is None  # Cek apakah ini transaksi baru

        if is_new:
            if self.jenis == 'simpan':
                self.tabungan.saldo += self.jumlah
            elif self.jenis in ['pinjam', 'penarikan']:
                self.tabungan.saldo -= self.jumlah
            self.tabungan.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tanggal} - {self.jenis} - {self.jumlah}"
