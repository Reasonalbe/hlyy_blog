import uuid


USER_KEY = 'uid'
ONE_YEAR = 60 * 60 * 24 * 365

class UserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """为每个request绑定一个uid属性，用于统计文章的PV和UV"""
        uid = self.gen_uid(request)
        request.uid = uid
        response = self.get_response(request)
        response.set_cookie(USER_KEY, uid, max_age=ONE_YEAR, httponly=True)
        return response

    def gen_uid(self, request):
        """返回session中的uid或者生成新的uid"""
        try:
            uid = request.COOKIES[USER_KEY]
        except KeyError:
            uid = uuid.uuid4().hex
        return uid