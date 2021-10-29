import os

API_BASE_ROUTE = '/api/v1'
# Grabs the folder where the script runs.
BASEDIR = os.path.abspath(os.path.dirname(__file__))
# Connect to the xml database
XML_DATABASE = '/data/autorizaciones.xml'
XML_TEMP_DATA = '/temp/'
ALLOWED_EXTENSIONS = {'xml', 'XML'}