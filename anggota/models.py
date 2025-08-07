from django.db import models
from django.contrib.auth.models import User

class Anggota(models.Model):
    # Relasi ke user auth (untuk login)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    # Pilihan jenis kelamin dan status
    JK_CHOICES = [
        ('Laki-laki', 'Laki-laki'),
        ('Perempuan', 'Perempuan'),
    ]
    STATUS_CHOICES = [
        ('aktif', 'Aktif'),
        ('tidak aktif', 'Tidak Aktif'),
    ]

    id_anggota = models.AutoField(primary_key=True)
    nip = models.CharField(max_length=30, unique=True, null=True)
    nama = models.CharField(max_length=100)
    jenis_kelamin = models.CharField(max_length=15, choices=JK_CHOICES)
    email = models.EmailField(max_length=50, blank=True, null=True)
    alamat = models.CharField(max_length=255, blank=True, null=True)
    no_tlp = models.CharField(max_length=20, blank=True, null=True)
    tgl_daftar = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='aktif')
    alasan_tidak_aktif = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.nama} ({self.nip})"
