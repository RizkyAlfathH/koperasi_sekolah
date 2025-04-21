from django.shortcuts import render

def daftar_pinjaman(request):
    return render(request, 'pinjaman/daftar_pinjaman.html')

def bayar_cicilan(request):
    return render(request, 'pinjaman/bayar_cicilan.html')
