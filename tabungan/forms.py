from django import forms
from .models import Tabungan, HistoryTabungan
from anggota.models import Anggota
from django.forms.widgets import SelectDateWidget


class TabunganForm(forms.ModelForm):
    nip = forms.CharField(label="NIP", max_length=50)
    nama = forms.CharField(label="Nama", max_length=100)
    jenis = forms.ChoiceField(choices=Tabungan.jenis_choices)
    jumlah = forms.DecimalField(label="Jumlah", max_digits=12, decimal_places=2)
    tanggal = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Tabungan
        fields = ['nip', 'nama', 'jenis', 'jumlah', 'tanggal']
