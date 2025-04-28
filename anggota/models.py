from django.db import models

class Anggota(models.Model):
    jk_choices = [('Laki-laki', 'Laki-laki'), ('Perempuan', 'Perempuan')]
    status_choices = [('aktif', 'Aktif'), ('tidak aktif', 'Tidak Aktif')]

    id_anggota = models.AutoField(primary_key=True)
    nip = models.CharField(max_length=30, unique=True, null=True)
    nama = models.CharField(max_length=100)
    jenis_kelamin = models.CharField(max_length=15, choices=jk_choices)
    email = models.EmailField(max_length=50, blank=True, null=True)
    alamat = models.CharField(max_length=255, blank=True, null=True)
    no_tlp = models.CharField(max_length=20, blank=True, null=True)
    tgl_daftar = models.DateField()
    status = models.CharField(max_length=15, choices=status_choices, default='aktif')
    alasan_tidak_aktif = models.TextField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.nama