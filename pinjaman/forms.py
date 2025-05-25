from django import forms
from decimal import Decimal
from .models import Pinjaman, HistoryPembayaran

class PinjamanForm(forms.ModelForm):
    JENIS_CHOICES = [
        ('reguler', 'Reguler'),
        ('khusus', 'Khusus'),
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
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.jumlah_reguler = self.cleaned_data.get('jumlah_reguler', Decimal('0'))
        instance.jumlah_usaha = self.cleaned_data.get('jumlah_usaha', Decimal('0'))
        instance.jumlah_barang = self.cleaned_data.get('jumlah_barang', Decimal('0'))
        # Jumlah cicilan dari input user, **JANGAN** diubah ke jumlah_pinjaman!
        instance.jumlah_cicilan = self.cleaned_data.get('jumlah_cicilan', Decimal('0'))
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
