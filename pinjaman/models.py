from decimal import Decimal
from django.db import models
from anggota.models import Anggota

class Pinjaman(models.Model):
    id_anggota = models.ForeignKey(Anggota, on_delete=models.CASCADE)
    tanggal_pinjaman = models.DateField()
    
    jumlah_reguler = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    jumlah_usaha = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    jumlah_barang = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    jumlah_cicilan = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    jatuh_tempo = models.DateField()
    status = models.CharField(max_length=10, default='belum')

    sisa_pinjaman = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    @property
    def jumlah_pinjaman(self):
        return (self.jumlah_reguler or Decimal('0')) + (self.jumlah_usaha or Decimal('0')) + (self.jumlah_barang or Decimal('0'))

    @property
    def bunga(self):
        jasa_reguler = (self.jumlah_reguler or Decimal('0')) * Decimal('0.02')
        jasa_usaha = (self.jumlah_usaha or Decimal('0')) * Decimal('0.02')
        jasa_barang = (self.jumlah_barang or Decimal('0')) * Decimal('0.01')
        return jasa_reguler + jasa_usaha + jasa_barang

    @property
    def jumlah_bayar(self):
        return (self.jumlah_cicilan or Decimal('0')) + (self.bunga or Decimal('0'))

    def save(self, *args, **kwargs):
        if not self.pk:
            self.sisa_pinjaman = self.jumlah_bayar
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pinjaman {self.id_anggota} - Sisa: {self.sisa_pinjaman:.2f}"

class HistoryPembayaran(models.Model):
    id_pinjaman = models.ForeignKey(Pinjaman, on_delete=models.CASCADE)
    tanggal_bayar = models.DateField()
    jumlah_bayar = models.DecimalField(max_digits=12, decimal_places=2)
    sisa_pinjaman = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00')) 

    def save(self, *args, **kwargs):
        if not self.pk:
            pinjaman = self.id_pinjaman
            sisa_sebelumnya = pinjaman.sisa_pinjaman or Decimal('0')
            print(f"Sisa sebelumnya: {sisa_sebelumnya}, Pembayaran: {self.jumlah_bayar}")
            sisa_baru = sisa_sebelumnya - self.jumlah_bayar
            if sisa_baru < 0:
                sisa_baru = Decimal('0')
            self.sisa_pinjaman = sisa_baru
            pinjaman.sisa_pinjaman = sisa_baru
            if sisa_baru == 0:
                pinjaman.status = 'lunas'
            pinjaman.save()
            print(f"Sisa baru: {sisa_baru}, Status: {pinjaman.status}")
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Pembayaran Rp{self.jumlah_bayar} - Sisa Rp{self.sisa_pinjaman} pada {self.tanggal_bayar}"
