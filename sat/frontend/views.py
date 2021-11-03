import requests

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
