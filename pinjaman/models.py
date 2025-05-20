from decimal import Decimal
from django.db import models
from anggota.models import Anggota
from django.db.models import Sum

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
        # Bunga awal (berdasarkan jenis pinjaman dan pokok)
        jasa_reguler = (self.jumlah_reguler or Decimal('0')) * Decimal('0.02')
        jasa_usaha = (self.jumlah_usaha or Decimal('0')) * Decimal('0.02')
        jasa_barang = (self.jumlah_barang or Decimal('0')) * Decimal('0.01')
        return jasa_reguler + jasa_usaha + jasa_barang

    @property
    def jumlah_bayar(self):
        # Total awal yang harus dibayar: cicilan + bunga (awalnya)
        return (self.jumlah_cicilan or Decimal('0')) + (self.bunga or Decimal('0'))

    @property
    def jasa_terbaru(self):
        # Jasa berdasarkan sisa pokok pinjaman terkini
        sisa_pokok = self.sisa_pinjaman or Decimal('0')
        total_pokok = self.jumlah_pinjaman
        if total_pokok == 0 or sisa_pokok == 0:
            return Decimal('0.00')
        prop_reguler = (self.jumlah_reguler or Decimal('0')) / total_pokok
        prop_usaha = (self.jumlah_usaha or Decimal('0')) / total_pokok
        prop_barang = (self.jumlah_barang or Decimal('0')) / total_pokok
        bunga_reguler = sisa_pokok * prop_reguler * Decimal('0.02')
        bunga_usaha = sisa_pokok * prop_usaha * Decimal('0.02')
        bunga_barang = sisa_pokok * prop_barang * Decimal('0.01')
        total_bunga = bunga_reguler + bunga_usaha + bunga_barang
        return total_bunga.quantize(Decimal('0.01'))

    def save(self, *args, **kwargs):
        # Set jumlah_cicilan ke input user, default ke jumlah_pinjaman jika belum diisi
        if not self.jumlah_cicilan or self.jumlah_cicilan == 0:
            self.jumlah_cicilan = self.jumlah_pinjaman
        if not self.pk:
            self.sisa_pinjaman = self.jumlah_pinjaman  # sisa pokok awal
        super().save(*args, **kwargs)

    def get_jasa_from_sisa(self, sisa_pokok):
        total_pokok = self.jumlah_pinjaman
        if total_pokok == 0:
            return Decimal('0.00')
        prop_reguler = (self.jumlah_reguler or Decimal('0')) / total_pokok
        prop_usaha = (self.jumlah_usaha or Decimal('0')) / total_pokok
        prop_barang = (self.jumlah_barang or Decimal('0')) / total_pokok

        bunga_reguler = sisa_pokok * prop_reguler * Decimal('0.02')
        bunga_usaha = sisa_pokok * prop_usaha * Decimal('0.02')
        bunga_barang = sisa_pokok * prop_barang * Decimal('0.01')

        return (bunga_reguler + bunga_usaha + bunga_barang).quantize(Decimal('0.01'))


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

            # Hitung total cicilan yang sudah dibayar (jumlah pembayaran sebelumnya)
            total_cicilan_sebelumnya = HistoryPembayaran.objects.filter(
                id_pinjaman=pinjaman
            ).aggregate(total=Sum('jumlah_bayar'))['total'] or Decimal('0')

            # Total pokok pinjaman (jumlah_reguler + jumlah_usaha + jumlah_barang)
            total_pokok = pinjaman.jumlah_pinjaman

            # Hitung sisa pinjaman = total pokok pinjaman - total cicilan yang sudah dibayar + cicilan ini
            sisa_baru = total_pokok - (total_cicilan_sebelumnya + self.jumlah_bayar)

            if sisa_baru < 0:
                sisa_baru = Decimal('0')

            self.sisa_pinjaman = sisa_baru

            # Update sisa pinjaman di pinjaman
            pinjaman.sisa_pinjaman = sisa_baru

            # Update status jika lunas
            if sisa_baru == 0:
                pinjaman.status = 'lunas'

            pinjaman.save()

        super().save(*args, **kwargs)


    def __str__(self):
        return f"Pembayaran Rp{self.jumlah_bayar} - Sisa Rp{self.sisa_pinjaman} pada {self.tanggal_bayar}"