import requests
from datetime import datetime
import json
import os

import io
from django.http import FileResponse
import pdfkit

from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def load(request):
    if request.method == 'POST' and request.FILES.get('xml-file'):
        file = request.FILES['xml-file']
        
        files = {"file" : file}
        response = requests.post('http://127.0.0.1:5000/api/v1/Procesar', files = files)
        
        if response.status_code == 200:
            response_info = requests.get('http://127.0.0.1:5000/api/v1/ConsultaDatos')
            file.seek(0)
            file_readed = file.read().decode()
            context = {
                'salida' : response_info.json()['data'],
                'entrada' : file_readed
            }
    return render(request, 'home.html', context = context)

def iva_graphic(request):
    context = {}
    if request.method == 'POST':
        date_picked = request.POST.get('date').replace("/", "-")
        date_formated = date_picked.split("-")[1] + "-" + date_picked.split("-")[0] + "-" + date_picked.split("-")[2]
        response = requests.get('http://127.0.0.1:5000/api/v1/ResumenIva/' + date_formated)
        data = response.json()
        print(data)
        context = {
            'graph' : data
        }

    return render(request, 'iva_graphics.html', context = context)

def iva_range(request):
    context = {}
    if request.method == 'POST':
        has_iva = request.POST.get('has_iva')
        date_picked_1 = request.POST.get('date_1').replace("/", "-")
        date_picked_2 = request.POST.get('date_2').replace("/", "-")
        date_formated_1 = date_picked_1.split("-")[1] + "-" + date_picked_1.split("-")[0] + "-" + date_picked_1.split("-")[2]
        date_formated_2 = date_picked_2.split("-")[1] + "-" + date_picked_2.split("-")[0] + "-" + date_picked_2.split("-")[2]
        response = requests.get('http://127.0.0.1:5000/api/v1/ResumenRango/' + date_formated_1 + "/" + date_formated_2)
        data = response.json()
        print(data)
        context = {
            'graph' : data,
            'has_iva' : has_iva
        }

    return render(request, 'range.html', context = context)

def download(request):
    # Create a file-like buffer to receive PDF data.
    data = request.POST.get('peticion')
    
    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': 'UTF-8'
    }
    data_string = str(data)
    print(data_string)
    pdf = pdfkit.from_string(data_string, False, options = options)
    if pdf:
        response = HttpResponse(pdf, content_type='attachment;application/pdf')
        response['Content-Disposition'] = 'attachment;filename="peticion.pdf"'
    return response 