from django.shortcuts import render, get_object_or_404, redirect
from .models import TransaksiTabungan
from .forms import TransaksiForm

def transaksi_list(request):
    transaksis = TransaksiTabungan.objects.all()
    return render(request, 'transaksi/transaksi_list.html', {'transaksi_list': transaksi_list})

def transaksi_create(request):
    if request.method == 'POST':
        form = TransaksiForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaksi_list')
    else:
        form = TransaksiForm()
    return render(request, 'transaksi/form.html', {'form': form, 'form_title': 'Tambah Transaksi'})

def transaksi_update(request, pk):
    transaksi = get_object_or_404(TransaksiTabungan, pk=pk)
    if request.method == 'POST':
        form = TransaksiForm(request.POST, instance=transaksi)
        if form.is_valid():
            form.save()
            return redirect('transaksi_list')
    else:
        form = TransaksiForm(instance=transaksi)
    return render(request, 'transaksi/form.html', {'form': form, 'form_title': 'Edit Transaksi'})

def transaksi_delete(request, pk):
    transaksi = get_object_or_404(TransaksiTabungan, pk=pk)
    if request.method == 'POST':
        transaksi.delete()
        return redirect('transaksi_list')
    return render(request, 'transaksi/confirm_delete.html', {'transaksi': transaksi})
