from django.db import models

class Anggota(models.Model):
    jk_choices = [('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')]
    tingkat_choices = [('X', 'X'), ('XI', 'XI'), ('XII', 'XII')]
    status_choices = [('aktif', 'Aktif'), ('nonaktif', 'Nonaktif')]

    nis = models.CharField(max_length=10, unique=True)
    nama = models.CharField(max_length=100)
    jenis_kelamin = models.CharField(max_length=15, choices=jk_choices)
    jurusan = models.CharField(max_length=50)
    kelas = models.CharField(max_length=20)
    tingkat = models.CharField(max_length=10, choices=tingkat_choices)
    telp = models.CharField(max_length=20)
    tgl_daftar = models.DateField()
    status = models.CharField(max_length=10, choices=status_choices, default='aktif')
    alasan_keluar = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nama
