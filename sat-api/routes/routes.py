from flask import Blueprint, Response, request
from config import API_BASE_ROUTE
from controllers.ResponseController import onError, onSuccess

application = Blueprint('route', __name__)

@application.route(f'{API_BASE_ROUTE}/')
def hello():
    return onSuccess({
        'success' : True
    })

@application.route('/', defaults={'path': ''})
@application.route('/<path:path>')
def catch_all(path):
    return onError('Route not found', 404)