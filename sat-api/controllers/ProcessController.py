from config import XML_DATABASE, XML_TEMP_DATA, ALLOWED_EXTENSIONS, BASEDIR
from controllers.ResponseController import onError, onSuccess
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
            os.remove(saved_route)
            
        return onSuccess('It works', 200)
