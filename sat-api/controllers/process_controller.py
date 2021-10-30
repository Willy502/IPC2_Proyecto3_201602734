from config import XML_DATABASE, XML_TEMP_DATA, ALLOWED_EXTENSIONS, BASEDIR
from controllers.response_controller import onError, onSuccess
from controllers.xml_controller import *
from werkzeug.utils import secure_filename
import os

class ProcessController:

    def allowed_file(self, filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def process(self, request):
        if 'file' not in request.files:
            return onError('File is missing', 404)
        file = request.files['file']

        if file.filename == '':
            return onError('No selected file', 400)

        
        if file == None or self.allowed_file(filename=file.filename) == False:
            return onError('File extension not allowed', 400)
        
        filename = secure_filename(file.filename)
        saved_route = BASEDIR + XML_TEMP_DATA + filename
        file.save(saved_route) 

        if os.path.isfile(saved_route):
            
            self.xml_controller = XmlController()
            self.xml_controller.create_authorizations_file()
            dte_list = self.xml_controller.build_dte(saved_route)
            self.validate_dte(dte_list = dte_list)
            os.remove(saved_route)
            
        return onSuccess('It works', 200)

    def validate_dte(self, dte_list):

        counter = {
            "invalid_emisor" : 0,
            "invalid_receptor" : 0,
            "bad_iva" : 0,
            "bad_total" : 0,
            "double_reference" : 0,
            "total_dte" : 0,
            "total_dte_no_errors" : 0
        }

        for dte in dte_list:
            counter["total_dte"] += 1
            nit_emisor_valid = self.validate_nit(dte.nit_emisor)
            nit_receptor_valid = self.validate_nit(dte.nit_receptor)
            iva_valid = self.validate_iva(dte)
            total_valid = self.validate_total(dte)

            if nit_emisor_valid and nit_receptor_valid and iva_valid and total_valid:
                counter["total_dte_no_errors"] += 1
            else:
                if nit_emisor_valid == False:
                    counter["invalid_emisor"] += 1
                
                if nit_receptor_valid == False:
                    counter["invalid_receptor"] += 1

                if iva_valid == False:
                    counter["bad_iva"] += 1
                
                if total_valid == False:
                    counter["bad_total"] += 1

        self.xml_controller.write_authorization(counter_information = counter)

    def validate_nit(self, nit):
        valid = False
        nit.replace("-","").replace(" ", "")
        dig_validador = nit[-1]
        dig_nit = list(nit[0:-1])
        dig_nit_rev = list(reversed(dig_nit))
        suma = 0
        base = 1
        for n in dig_nit_rev:
            base += 1
            suma += int(n) * base

        result = suma % 11
        comp = 11 - result
        new_comp = comp % 11

        if new_comp == 10:
            if dig_validador == "k":
                valid = True
        else:
            if new_comp == int(dig_validador):
                valid = True
        
        return valid

    def validate_iva(self, dte):
        valid = False
        if float(dte.iva) == float(dte.valor) * 0.12:
            valid = True
        return valid

    def validate_total(self, dte):
        valid = False
        if (float(dte.valor) * 0.12) + float(dte.valor) == float(dte.total):
            valid = True
        return valid