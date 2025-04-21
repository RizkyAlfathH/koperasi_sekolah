from django.shortcuts import render

def daftar_tabungan(request):
    return render(request, 'tabungan/daftar.html')

def setor_tabungan(request):
    return render(request, 'tabungan/form.html')
