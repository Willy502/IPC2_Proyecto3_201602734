def onError(message, code = 500):
    return {
        'error' : {
            'code' : code,
            'message' : message
        }
    }, code

def onSuccess(data, code = 200):
    return {
        'data' : data
    }, code