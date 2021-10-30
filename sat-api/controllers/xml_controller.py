import xml.etree.cElementTree as ET
from xml.dom import minidom
import os
from config import XML_DATABASE, XML_TEMP_DATA, BASEDIR
from models.dte import *

class XmlController:

    def create_authorizations_file(self):
        auth_route = BASEDIR + XML_DATABASE
        if os.path.isfile(auth_route) == False:
            root = ET.Element("LISTAAUTORIZACIONES")

            tree = ET.ElementTree(root)
            tree.write(auth_route)

    def build_dte(self, file):
        
        tree = ET.parse(file)
        root = tree.getroot()
        dte_list = []
        for child in root:
            if child.tag.upper() == "DTE":
                dte = Dte()
                for element in child:

                    if element.tag.upper() == "TIEMPO":
                        dte.tiempo = element.text.lstrip().rstrip()
                    elif element.tag.upper() == "REFERENCIA":
                        dte.referencia = element.text.lstrip().rstrip()
                    elif element.tag.upper() == "NIT_EMISOR":
                        dte.nit_emisor = element.text.lstrip().rstrip()
                    elif element.tag.upper() == "NIT_RECEPTOR":
                        dte.nit_receptor = element.text.lstrip().rstrip()
                    elif element.tag.upper() == "VALOR":
                        dte.valor = element.text.lstrip().rstrip()
                    elif element.tag.upper() == "IVA":
                        dte.iva = element.text.lstrip().rstrip()
                    elif element.tag.upper() == "TOTAL":
                        dte.total = element.text.lstrip().rstrip()

                dte_list.append(dte)
        return dte_list

    def write_authorization(self, counter_information):
        auth_route = BASEDIR + XML_DATABASE
        tree = ET.parse(auth_route)
        root = tree.getroot()
        auth = ET.SubElement(root, "AUTORIZACION")

        ET.SubElement(auth, "FACTURAS_RECIBIDAS").text = str(counter_information["total_dte"])
        errores = ET.SubElement(auth, "ERRORES")
        ET.SubElement(errores, "NIT_EMISOR").text = str(counter_information["invalid_emisor"])
        ET.SubElement(errores, "NIT_RECEPTOR").text = str(counter_information["invalid_receptor"])
        ET.SubElement(errores, "IVA").text = str(counter_information["bad_iva"])
        ET.SubElement(errores, "TOTAL").text = str(counter_information["bad_total"])
        ET.SubElement(auth, "FACTURAS_CORRECTAS").text = str(counter_information["total_dte_no_errors"])

        tree = ET.ElementTree(root)
        data = minidom.parseString(ET.tostring(root))
        file = open(auth_route, "w")
        new_data = data.toprettyxml()
        file.write(new_data)

        # Remove empty lines
        with open(auth_route) as xmlfile:
            lines = [line for line in xmlfile if line.strip() is not ""]

        with open(auth_route, "w") as xmlfile:
            xmlfile.writelines(lines)