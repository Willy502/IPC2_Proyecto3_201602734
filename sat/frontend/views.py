import requests
from datetime import datetime
import json

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
