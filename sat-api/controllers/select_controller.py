import xml.etree.cElementTree as ET
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

        data = None
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

            for child in lista_autorizaciones.find('LISTADO_AUTORIZACIONES'):
                if child.tag.upper() == "APROBACION":
                    for element in child:
                        print(element.tag)
                

        if found == False:
            return onError('No data available', 404)

        return onSuccess(data = data, message = 'Data retrieved successfully')