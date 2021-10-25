from flask import Flask
from routes.routes import application
from controllers.ResponseController import onError

app = Flask(__name__)
app.register_blueprint(application)

@app.errorhandler(405)
def method_not_allowed(e):
    return onError('The method is not allowed for the requested URL.', 405)


app.run()