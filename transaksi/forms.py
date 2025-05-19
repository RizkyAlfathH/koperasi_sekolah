from django import forms
from .models import TransaksiTabungan
from anggota.models import Anggota

class TransaksiForm(forms.ModelForm):
    anggota = forms.ModelChoiceField(
        queryset=Anggota.objects.all(),
        label="Pilih Anggota"
    )

    class Meta:
        model = TransaksiTabungan
        fields = ['anggota', 'jenis', 'tanggal', 'jumlah', 'keterangan']
        widgets = {
            'tanggal': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['anggota'].label_from_instance = lambda obj: f"{obj.nip} - {obj.nama}"
