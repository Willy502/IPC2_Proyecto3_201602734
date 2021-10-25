from flask import Blueprint, Response, request
from config import API_BASE_ROUTE
from controllers.ResponseController import onError, onSuccess

application = Blueprint('routes', __name__)

@application.route(f'{API_BASE_ROUTE}/ConsultaDatos')
def consulta_datos():
    if request.method == 'GET':
        return onSuccess({
            'success' : True
        })
    else:
        return onError('The method is not allowed for the requested URL.', 405)

@application.route(f'{API_BASE_ROUTE}/ResumenIva')
def resumen_iva():
    if request.method == 'GET':
        return onSuccess({
            'success' : True
        })
    else:
        return onError('The method is not allowed for the requested URL.', 405)

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
    return onSuccess({
        'success' : True
    })

@application.route('/', defaults={'path': ''})
@application.route('/<path:path>')
def catch_all(path):
    return onError('Route not found', 404)