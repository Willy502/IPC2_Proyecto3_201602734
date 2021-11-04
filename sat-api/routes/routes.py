from flask import Blueprint, Response, request
from config import API_BASE_ROUTE
from controllers.response_controller import onError, onSuccess
from controllers.process_controller import *
from controllers.xml_controller import *
from controllers.select_controller import *

application = Blueprint('routes', __name__)

@application.route(f'{API_BASE_ROUTE}/ConsultaDatos')
def consulta_datos():
    return XmlController().read_all_file()

@application.route(f'{API_BASE_ROUTE}/Reset', methods = ['DELETE'])
def reset_data():
    return XmlController().reset_data()

@application.route(f'{API_BASE_ROUTE}/ResumenIva/<fecha>')
def resumen_iva(fecha):
    return SelectController().select_iva_by_date_and_nit(date = fecha)

@application.route(f'{API_BASE_ROUTE}/ResumenRango/<fecha_start>/<fecha_end>')
def resumen_rango(fecha_start, fecha_end):
    return SelectController().select_iva_by_date_range_and_nit(date_start = fecha_start, date_end = fecha_end)

@application.route(f'{API_BASE_ROUTE}/Procesar', methods = ['POST'])
def procesar():
    return ProcessController().process(request=request)

@application.route('/', defaults={'path': ''})
@application.route('/<path:path>')
def catch_all(path):
    return onError('Route not found', 404)