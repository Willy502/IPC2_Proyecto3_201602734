import requests

from django.http import HttpResponse

from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def load(request):
    if request.method == 'POST' and request.FILES['xml-file']:
        file = request.FILES['xml-file']
        
        files = {"file" : file}
        response = requests.post('http://127.0.0.1:5000/api/v1/Procesar', files = files)
        print(response.json())
    return render(request, 'home.html')
