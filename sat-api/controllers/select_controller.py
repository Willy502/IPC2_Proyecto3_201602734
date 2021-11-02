import xml.etree.cElementTree as ET
from datetime import datetime
import os
from config import XML_DATABASE, XML_TEMP_DATA, ALLOWED_EXTENSIONS, BASEDIR, XML_DATABASE_INFO
from controllers.response_controller import onError, onSuccess

class SelectController:

    def select_iva_by_date_and_nit(self, date):
        auth_route = BASEDIR + XML_DATABASE
        info_route = BASEDIR + XML_DATABASE_INFO
        if os.path.isfile(auth_route) == False or os.path.isfile(info_route) == False:
            return onError('No data available', 404)

        tree = ET.parse(auth_route)
        root = tree.getroot()

        info_tree = ET.parse(info_route)
        info_root = info_tree.getroot()

        data = {}
        found = False

        for lista_autorizaciones in root:
            fecha = lista_autorizaciones.find('FECHA')
            if fecha is None:
                continue

            if fecha.text != date.replace("-", "/"):
                continue

            facturas_correctas = int(lista_autorizaciones.find('FACTURAS_CORRECTAS').text)
            if facturas_correctas <= 0:
                return onError('No data available', 404)

            aprobacion_list = []
            for child in lista_autorizaciones.find('LISTADO_AUTORIZACIONES'):
                if child.tag.upper() == "APROBACION":
                    for element in child:
                        if element.tag.upper() == "NIT_EMISOR":
                            aprobacion_list.append(element.attrib['ref'])
            
            for dte_info in info_root:
                if dte_info.find("REFERENCIA").text in aprobacion_list and dte_info.find("FECHA").text == fecha.text:
                    for element in dte_info:
                        data[dte_info.find("NIT_EMISOR").text] = {
                            "iva_emitido" : 0,
                            "iva_recibido" : 0
                        }
                        data[dte_info.find("NIT_RECEPTOR").text] = {
                            "iva_emitido" : 0,
                            "iva_recibido" : 0
                        }
            
            for dte_info in info_root:
                if dte_info.find("REFERENCIA").text in aprobacion_list and dte_info.find("FECHA").text == fecha.text:
                    data[dte_info.find("NIT_EMISOR").text]["iva_emitido"] += float(dte_info.find("IVA").text)
                    data[dte_info.find("NIT_RECEPTOR").text]["iva_recibido"] += float(dte_info.find("IVA").text)

        if data != {}:
            found = True

        if found == False:
            return onError('No data available', 404)

        return onSuccess(data = data, message = 'Data retrieved successfully')

    def select_iva_by_date_range_and_nit(self, date_start, date_end):
        auth_route = BASEDIR + XML_DATABASE
        info_route = BASEDIR + XML_DATABASE_INFO
        if os.path.isfile(auth_route) == False or os.path.isfile(info_route) == False:
            return onError('No data available', 404)

        tree = ET.parse(auth_route)
        root = tree.getroot()

        info_tree = ET.parse(info_route)
        info_root = info_tree.getroot()

        data = {}
        found = False

        
        datetime_start = datetime.strptime(date_start.replace("-", "/"), '%d/%m/%Y')
        datetime_end = datetime.strptime(date_end.replace("-", "/"), '%d/%m/%Y')

        for lista_autorizaciones in root:
            fecha = lista_autorizaciones.find('FECHA')
            if fecha is None:
                continue
            
            if datetime.strptime(fecha.text, '%d/%m/%Y') < datetime_start or datetime.strptime(fecha.text, '%d/%m/%Y') > datetime_end:
                continue
            
            facturas_correctas = int(lista_autorizaciones.find('FACTURAS_CORRECTAS').text)
            if facturas_correctas <= 0:
                return onError('No data available', 404)

            aprobacion_list = []
            for child in lista_autorizaciones.find('LISTADO_AUTORIZACIONES'):
                if child.tag.upper() == "APROBACION":
                    for element in child:
                        if element.tag.upper() == "NIT_EMISOR":
                            aprobacion_list.append(element.attrib['ref'])
            
            for dte_info in info_root:
                if dte_info.find("REFERENCIA").text in aprobacion_list and (datetime.strptime(fecha.text, '%d/%m/%Y') >= datetime_start and datetime.strptime(fecha.text, '%d/%m/%Y') <= datetime_end):
                    for element in dte_info:
                        if dte_info.find("FECHA").text not in data:
                            data[dte_info.find("FECHA").text] = {
                                "total_iva" : 0,
                                "total_sin_iva" : 0
                            }
            
            for dte_info in info_root:
                if dte_info.find("REFERENCIA").text in aprobacion_list and ((datetime.strptime(fecha.text, '%d/%m/%Y') >= datetime_start and datetime.strptime(fecha.text, '%d/%m/%Y') <= datetime_end)):
                    data[dte_info.find("FECHA").text]["total_iva"] += float(dte_info.find("TOTAL").text)
                    data[dte_info.find("FECHA").text]["total_sin_iva"] += float(dte_info.find("VALOR").text)

        if data != {}:
            found = True

        if found == False:
            return onError('No data available', 404)

        return onSuccess(data = data, message = 'Data retrieved successfully')