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

from django import forms

class PenarikanForm(forms.Form):
    nip = forms.CharField(
        label="NIP",
        max_length=30,
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'id': 'nip-field'
        })
    )
    nama = forms.CharField(
        label="Nama",
        max_length=100,
        widget=forms.TextInput(attrs={
            'autocomplete': 'off',
            'id': 'nama-field',
            'list': 'nama-list'
        })
    )
    jumlah_pokok = forms.DecimalField(
        label='Jumlah Pokok',
        max_digits=12, decimal_places=2,
        required=False,
        disabled=True,
        widget=forms.NumberInput(attrs={'id': 'jumlah-pokok'})
    )
    jumlah_wajib = forms.DecimalField(
        label='Jumlah Wajib',
        max_digits=12, decimal_places=2,
        required=False,
        disabled=True,
        widget=forms.NumberInput(attrs={'id': 'jumlah-wajib'})
    )
    jumlah_sukarela = forms.DecimalField(
        label='Jumlah Sukarela',
        max_digits=12, decimal_places=2,
        required=False,
        disabled=True,
        widget=forms.NumberInput(attrs={'id': 'jumlah-sukarela'})
    )
    jumlah = forms.DecimalField(
        label="Jumlah Penarikan",
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'id': 'jumlah-penarikan'})
    )
