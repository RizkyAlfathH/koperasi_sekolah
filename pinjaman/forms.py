from django import forms
from decimal import Decimal
from .models import Pinjaman, HistoryPembayaran
from datetime import timedelta

class PinjamanForm(forms.ModelForm):
    JENIS_CHOICES = [
        ('reguler', 'Reguler'),
        ('khusus', 'Khusus'),
        ('barang', 'Barang'),
    ]

    STATUS_CHOICES = [
        ('belum lunas', 'Belum Lunas'),
        ('lunas', 'Lunas'),
    ]
    jenis_pinjaman = forms.ChoiceField(
        choices=JENIS_CHOICES,
        label='Jenis Pinjaman'
    )
    jumlah = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label='Jumlah Pinjaman',
        min_value=0
    )
    jumlah_cicilan = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label='Jumlah Cicilan',
        min_value=0,
        required=True
    )
    jasa = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label='Jasa (Otomatis)',
        required=False,
        widget=forms.NumberInput(attrs={'readonly': 'readonly', 'style': 'background:#eee;'})
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        label='Status Pembayaran'
    )

    class Meta:
        model = Pinjaman
        fields = [
            'id_anggota',
            'tanggal_pinjaman',
            'jenis_pinjaman',
            'jumlah',
            'jumlah_cicilan',
            'jasa',
            'jatuh_tempo',
            'status'
        ]
        widgets = {
            'tanggal_pinjaman': forms.DateInput(attrs={'type': 'date'}),
            'jatuh_tempo': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'id_anggota': 'Nama Anggota',
            'tanggal_pinjaman': 'Tanggal Pinjam',
            'jenis_pinjaman': 'Jenis Pinjaman',
            'jumlah': 'Jumlah Pinjaman',
            'jasa': 'Jasa (Otomatis)',
            'jatuh_tempo': 'Jatuh Tempo',
            'status': 'Status Pembayaran',
        }

    def clean(self):
        cleaned_data = super().clean()
        jenis = cleaned_data.get('jenis_pinjaman')
        jumlah = cleaned_data.get('jumlah') or Decimal('0')
        tanggal_pinjaman = cleaned_data.get('tanggal_pinjaman')
        jatuh_tempo = cleaned_data.get('jatuh_tempo')

        cleaned_data['jumlah_reguler'] = Decimal('0')
        cleaned_data['jumlah_usaha'] = Decimal('0')
        cleaned_data['jumlah_barang'] = Decimal('0')

        jasa = Decimal('0')
        if jenis == 'reguler':
            cleaned_data['jumlah_reguler'] = jumlah
            jasa = jumlah * Decimal('0.02')
        elif jenis == 'khusus':
            cleaned_data['jumlah_usaha'] = jumlah
            jasa = jumlah * Decimal('0.015')
        elif jenis == 'barang':
            cleaned_data['jumlah_barang'] = jumlah
            jasa = jumlah * Decimal('0.02') 

        cleaned_data['jasa'] = jasa.quantize(Decimal('0.01'))

        # Validasi jatuh tempo maksimal 36 bulan
        if tanggal_pinjaman and jatuh_tempo:
            batas_jatuh_tempo = tanggal_pinjaman + timedelta(days=36*30)  # estimasi 36 bulan
            if jatuh_tempo > batas_jatuh_tempo:
                self.add_error('jatuh_tempo', "Jatuh tempo maksimal adalah 36 bulan dari tanggal pinjam.")

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Atur field jumlah berdasarkan jenis pinjaman
        instance.jumlah_reguler = self.cleaned_data.get('jumlah_reguler', Decimal('0'))
        instance.jumlah_usaha = self.cleaned_data.get('jumlah_usaha', Decimal('0'))
        instance.jumlah_barang = self.cleaned_data.get('jumlah_barang', Decimal('0'))

        # Cek pinjaman lama yang belum lunas
        if not instance.pk:
            pinjaman_lama = Pinjaman.objects.filter(
                id_anggota=instance.id_anggota,
                status='belum lunas'
            ).exclude(pk=instance.pk).first()

            if pinjaman_lama:
                sisa_lama = pinjaman_lama.sisa_pinjaman or Decimal('0')
                # Tambahkan sisa lama ke jumlah_reguler (atau sesuai logika)
                instance.jumlah_reguler += sisa_lama

                # Tandai pinjaman lama lunas dan sisa 0
                pinjaman_lama.status = 'lunas'
                pinjaman_lama.sisa_pinjaman = Decimal('0')
                pinjaman_lama.save()

            # Jika jumlah_cicilan belum diisi, isi dengan total pinjaman yang dihitung dari jumlah_reguler+usaha+barang
            if not instance.jumlah_cicilan or instance.jumlah_cicilan == 0:
                instance.jumlah_cicilan = instance.jumlah_pinjaman

            # Inisialisasi sisa_pinjaman = total pinjaman
            instance.sisa_pinjaman = instance.jumlah_pinjaman

        if commit:
            instance.save()

        return instance


class HistoryPembayaranForm(forms.ModelForm):
    class Meta:
        model = HistoryPembayaran
        fields = ['tanggal_bayar', 'jumlah_bayar']
        widgets = {
            'tanggal_bayar': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'tanggal_bayar': 'Tanggal Pembayaran',
            'jumlah_bayar': 'Jumlah Dibayar',
        }
