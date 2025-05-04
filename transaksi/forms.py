from django import forms
from .models import TransaksiTabungan

class TransaksiForm(forms.ModelForm):
    class Meta:
        model = TransaksiTabungan
        fields = '__all__'
