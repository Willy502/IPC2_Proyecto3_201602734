from flask import Flask
from config import XML_TEMP_DATA
from routes.routes import application
from controllers.response_controller import onError

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = XML_TEMP_DATA
app.register_blueprint(application)

@app.errorhandler(405)
def method_not_allowed(e):
    return onError('The method is not allowed for the requested URL.', 405)

@app.errorhandler(500)
def method_not_allowed(e):
    return onError('Internal server error.', 500)


app.run()