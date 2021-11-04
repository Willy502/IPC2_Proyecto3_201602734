import xml.etree.cElementTree as ET
from xml.dom import minidom
from datetime import datetime
import os
from config import XML_DATABASE, XML_TEMP_DATA, BASEDIR, XML_DATABASE_INFO
from models.dte import *
from controllers.response_controller import onError, onSuccess

class XmlController:

    def reset_data(self):
        auth_route = BASEDIR + XML_DATABASE
        info_route = BASEDIR + XML_DATABASE_INFO
        if os.path.isfile(auth_route) == True:
            os.remove(auth_route)

        if os.path.isfile(info_route) == True:
            os.remove(info_route)

        return onSuccess(message = 'The database has been deleted')

    def create_authorizations_file(self):
        auth_route = BASEDIR + XML_DATABASE
        info_route = BASEDIR + XML_DATABASE_INFO
        if os.path.isfile(auth_route) == False:
            root = ET.Element("LISTAAUTORIZACIONES")

            tree = ET.ElementTree(root)
            tree.write(auth_route)

        if os.path.isfile(info_route) == False:
            root_info = ET.Element("AUTORIZADAS")

            tree_info = ET.ElementTree(root_info)
            tree_info.write(info_route)

    def read_all_file(self):
        auth_route = BASEDIR + XML_DATABASE
        if os.path.isfile(auth_route) == False:
            return onError('No data available', 404)

        data = ''
        with open(auth_route, 'r') as file:
            data = file.read().split("\n",1)[1]

        return onSuccess(data = data, message = 'Data retrieved successfully')

    def build_dte(self, file):
        
        tree = ET.parse(file)
        root = tree.getroot()
        dte_list = []
        for child in root:
            if child.tag.upper() == "DTE":
                dte = Dte()
                for element in child:
                    if element.tag.upper() == "TIEMPO":
                        dte.tiempo = element.text.strip()
                    elif element.tag.upper() == "REFERENCIA":
                        dte.referencia = element.text.strip()
                    elif element.tag.upper() == "NIT_EMISOR":
                        dte.nit_emisor = element.text.strip()
                    elif element.tag.upper() == "NIT_RECEPTOR":
                        dte.nit_receptor = element.text.strip()
                    elif element.tag.upper() == "VALOR":
                        dte.valor = element.text.strip()
                    elif element.tag.upper() == "IVA":
                        dte.iva = element.text.strip()
                    elif element.tag.upper() == "TOTAL":
                        dte.total = element.text.strip()
                dte.save_date(tiempo = dte.tiempo)
                dte_list.append(dte)
        return dte_list

    def write_authorization(self, counter_information):

        auth_route = BASEDIR + XML_DATABASE
        tree = ET.parse(auth_route)
        root = tree.getroot()
        correlativo = 1

        for dte_filt in counter_information:
            auth = ET.SubElement(root, "AUTORIZACION")

            ET.SubElement(auth, "FECHA").text = str(dte_filt)
            ET.SubElement(auth, "FACTURAS_RECIBIDAS").text = str(counter_information[dte_filt]["info"]["total_dte"])
            errores = ET.SubElement(auth, "ERRORES")
            ET.SubElement(errores, "NIT_EMISOR").text = str(counter_information[dte_filt]["info"]["invalid_emisor"])
            ET.SubElement(errores, "NIT_RECEPTOR").text = str(counter_information[dte_filt]["info"]["invalid_receptor"])
            ET.SubElement(errores, "IVA").text = str(counter_information[dte_filt]["info"]["bad_iva"])
            ET.SubElement(errores, "TOTAL").text = str(counter_information[dte_filt]["info"]["bad_total"])
            ET.SubElement(auth, "FACTURAS_CORRECTAS").text = str(counter_information[dte_filt]["info"]["total_dte_no_errors"])
            ET.SubElement(auth, "CANTIDAD_EMISORES").text = str(counter_information[dte_filt]["info"]["emisores"])
            ET.SubElement(auth, "CANTIDAD_RECEPTORES").text = str(counter_information[dte_filt]["info"]["receptores"])
            autorizaciones = ET.SubElement(auth, "LISTADO_AUTORIZACIONES")
            for approved in counter_information[dte_filt]["info"]["dtes"]:
                aprob = ET.SubElement(autorizaciones, "APROBACION")
                ET.SubElement(aprob, "NIT_EMISOR", ref=approved.referencia).text = str(approved.nit_emisor)
                correlativo_str = str(correlativo).zfill(8)
                ET.SubElement(aprob, "CODIGO_APROBACION").text = str(datetime.today().strftime('%Y%m%d') + correlativo_str)
                correlativo += 1
            ET.SubElement(autorizaciones, "TOTAL_APROBACIONES").text = str(counter_information[dte_filt]["info"]["total_dte_no_errors"])

        tree = ET.ElementTree(root)
        data = minidom.parseString(ET.tostring(root))
        file = open(auth_route, "w")
        new_data = data.toprettyxml()
        file.write(new_data)
        file.close()

        # Remove empty lines
        with open(auth_route, "r") as xmlfile:
            lines = [line for line in xmlfile.readlines() if line.strip() is not ""]

        with open(auth_route, "w") as xmlfile:
            xmlfile.writelines(lines)
            file.close()

    def write_authorization_info(self, dtes_info):
        info_route = BASEDIR + XML_DATABASE_INFO
        tree = ET.parse(info_route)
        root = tree.getroot()

        for dte in dtes_info:
            dt = ET.SubElement(root, "DTE")
            ET.SubElement(dt, "FECHA").text = str(dte.fecha)
            ET.SubElement(dt, "TIEMPO").text = str(dte.tiempo)
            ET.SubElement(dt, "REFERENCIA").text = str(dte.referencia)
            ET.SubElement(dt, "NIT_EMISOR").text = str(dte.nit_emisor)
            ET.SubElement(dt, "NIT_RECEPTOR").text = str(dte.nit_receptor)
            ET.SubElement(dt, "VALOR").text = str(dte.valor)
            ET.SubElement(dt, "IVA").text = str(dte.iva)
            ET.SubElement(dt, "TOTAL").text = str(dte.total)

        tree = ET.ElementTree(root)
        data = minidom.parseString(ET.tostring(root))
        file = open(info_route, "w")
        new_data = data.toprettyxml()
        file.write(new_data)
        file.close()

        # Remove empty lines
        with open(info_route, "r") as xmlfile:
            lines = [line for line in xmlfile.readlines() if line.strip() is not ""]

        with open(info_route, "w") as xmlfile:
            xmlfile.writelines(lines)
            file.close()
