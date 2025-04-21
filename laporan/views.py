from django.shortcuts import render

def ringkasan(request):
    return render(request, 'laporan/ringkasan.html')

def export_pdf(request):
    return render(request, 'laporan/export_pdf.html')
