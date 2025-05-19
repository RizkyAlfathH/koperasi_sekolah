from django import forms
from decimal import Decimal 
from .models import Pinjaman, HistoryPembayaran

class PinjamanForm(forms.ModelForm):
    JENIS_CHOICES = [
        ('reguler', 'Reguler'),
        ('usaha', 'Usaha'),
        ('barang', 'Barang'),
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

    jasa = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        label='Jasa (Otomatis)',
        required=False,
        widget=forms.NumberInput(attrs={'readonly': 'readonly', 'style': 'background:#eee;'})
    )

    class Meta:
        model = Pinjaman
        fields = [
            'id_anggota',
            'tanggal_pinjaman',
            'jenis_pinjaman',
            'jumlah',
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

        # Reset semua kategori
        cleaned_data['jumlah_reguler'] = Decimal('0')
        cleaned_data['jumlah_usaha'] = Decimal('0')
        cleaned_data['jumlah_barang'] = Decimal('0')

        jasa = Decimal('0')
        if jenis == 'reguler':
            cleaned_data['jumlah_reguler'] = jumlah
            jasa = jumlah * Decimal('0.02')  # 2%
        elif jenis == 'usaha':
            cleaned_data['jumlah_usaha'] = jumlah
            jasa = jumlah * Decimal('0.02')  # 2%
        elif jenis == 'barang':
            cleaned_data['jumlah_barang'] = jumlah
            jasa = jumlah * Decimal('0.01')  # 1%

        cleaned_data['jasa'] = jasa.quantize(Decimal('0.01'))  # Pembulatan 2 desimal

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)

        instance.jumlah_reguler = self.cleaned_data.get('jumlah_reguler', Decimal('0'))
        instance.jumlah_usaha = self.cleaned_data.get('jumlah_usaha', Decimal('0'))
        instance.jumlah_barang = self.cleaned_data.get('jumlah_barang', Decimal('0'))

        # Total bayar = pokok + jasa
        instance.jumlah_bayar = (
            instance.jumlah_reguler +
            instance.jumlah_usaha +
            instance.jumlah_barang +
            self.cleaned_data.get('jasa', Decimal('0'))
        )

        if commit:
            instance.save()
        return instance


class HistoryPembayaranForm(forms.ModelForm):
    class Meta:
        model = HistoryPembayaran
        fields = ['id_pinjaman', 'tanggal_bayar', 'jumlah_bayar']
        widgets = {
            'tanggal_bayar': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'id_pinjaman': 'Pinjaman',
            'tanggal_bayar': 'Tanggal Pembayaran',
            'jumlah_bayar': 'Jumlah Dibayar',
        }
