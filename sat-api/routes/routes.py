from flask import Blueprint, Response, request
from config import API_BASE_ROUTE
from controllers.ResponseController import onError, onSuccess
from controllers.ProcessController import *

application = Blueprint('routes', __name__)

@application.route(f'{API_BASE_ROUTE}/ConsultaDatos')
def consulta_datos():
    return onSuccess({
        'success' : True
    })

@application.route(f'{API_BASE_ROUTE}/ResumenIva')
def resumen_iva():
    return onSuccess({
        'success' : True
    })

@application.route(f'{API_BASE_ROUTE}/ResumenRango')
def resumen_rango():
    return onSuccess({
        'success' : True
    })

@application.route(f'{API_BASE_ROUTE}/Grafica')
def grafica():
    return onSuccess({
        'success' : True
    })

@application.route(f'{API_BASE_ROUTE}/Procesar', methods = ['POST'])
def procesar():
    return ProcessController().process(request=request)

@application.route('/', defaults={'path': ''})
@application.route('/<path:path>')
def catch_all(path):
    return onError('Route not found', 404)