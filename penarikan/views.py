from django.shortcuts import render

def daftar_penarikan(request):
    return render(request, 'penarikan/daftar.html')

def form_penarikan(request):
    return render(request, 'penarikan/form.html')
