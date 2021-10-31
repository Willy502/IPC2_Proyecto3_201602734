def onError(message, code = 500):
    return {
        'error' : {
            'code' : code,
            'message' : message
        }
    }, code

def onSuccess(data = None, message = '', code = 200):

    response = {
        'data' : data,
        'message' : message
    }
    
    if data is None:
        response = {
            'message' : message
        }

    return response, code