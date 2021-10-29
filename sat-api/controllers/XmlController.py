import xml.etree.cElementTree as ET
import os
from config import XML_DATABASE, XML_TEMP_DATA, BASEDIR

class XmlController:

    def create_authorizations_file(self):
        auth_route = BASEDIR + XML_DATABASE
        if os.path.isfile(auth_route) == False:
            root = ET.Element("LISTAAUTORIZACIONES")

            tree = ET.ElementTree(root)
            tree.write(auth_route)
