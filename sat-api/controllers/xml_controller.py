import xml.etree.cElementTree as ET
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
        print(file)
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
