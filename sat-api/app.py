from flask import Flask
from routes.routes import application

app = Flask(__name__)

app.register_blueprint(application)


app.run()