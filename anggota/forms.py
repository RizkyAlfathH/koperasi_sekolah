from django import forms
from admin_koperasi.models import Admin
from .models import Anggota

class AdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = Admin
        fields = ['username', 'password', 'role']

    def save(self, commit=True):
        admin = super().save(commit=False)
        if self.cleaned_data['password']:
            admin.set_password(self.cleaned_data['password'])  # Hash password saat simpan
        if commit:
            admin.save()
        return admin

class AnggotaForm(forms.ModelForm):
    class Meta:
        model = Anggota
        fields = '__all__'
