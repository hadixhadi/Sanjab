import redis
from config.envs import settings
def count_views_middleware(get_response):
    # One-time configuration and initialization.
    def middleware(request):
        response = get_response(request)

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = str(x_forwarded_for.split(',')[0])
        else:
            ip = str(request.META.get('REMOTE_ADDR'))

        if request.path not in ['/api/v1/account/login-register/','/api/v1/account/phone-verification/']:
            r=redis.Redis(host='redis',port='6379',db='0')
            r.set(ip,str(request.path))

        return response

    return middleware