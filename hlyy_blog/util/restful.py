from django.http import JsonResponse

class HttpCode:
    ok = 200
    paramserror = 400
    unauth = 401
    methoderror = 405
    servererror = 500

def result(code=HttpCode.ok, message='', data=None, kwargs=None):
    json_dict = {
        'code': code    ,
        'message': message,
        'data': data
    }
    if kwargs and isinstance(kwargs, dict) and kwargs.keys():
        json_dict.update(kwargs)

    return JsonResponse(json_dict)

def ok():
    return result()

def unauth(message='', data=None, kwargs=None):
    return result(code=HttpCode.unauth, message=message, data=data, kwargs=kwargs)

def paramserror(message='', data=None, kwargs=None):
    return result(code=HttpCode.paramserror, message=message, data=data, kwargs=kwargs)

def methoderror(message='', data=None, kwargs=None):
    return result(code=HttpCode.methoderror, message=message, data=data, kwargs=kwargs)

def servererror(message='', data=None, kwargs=None):
    return result(code=HttpCode.servererror, message=message, data=data, kwargs=kwargs)