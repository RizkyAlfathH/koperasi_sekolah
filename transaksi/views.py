from django.shortcuts import render

def histori_transaksi(request):
    return render(request, 'transaksi/histori.html')
