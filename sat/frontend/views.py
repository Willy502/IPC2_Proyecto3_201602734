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
