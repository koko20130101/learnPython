import datetime
import pytz
# from django.utils.translation import ugettext_lazy
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import HTTP_HEADER_ENCODING

# 获取请求头信息


def get_authorization_header(request):
    print(1)
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, type('')):
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class ExpiringTokenAuthentication(BaseAuthentication):
    model = Token

    def authenticate(self, request):
        auth = get_authorization_header(request)
        if not auth:
            print(2)
            return None
        try:
            token = auth.decode()
        except UnicodeError:
            msg = '无效的token，Token头不应包含无效字符'
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        print(3)
        token_cache = 'token_' + key
        cache_user = cache.get(token_cache)
        if cache_user:
            return cache_user, cache_user

        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                {'status': status.HTTP_503_SERVICE_UNAVAILABLE, 'msg': '认证失败'})

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(
                {'status': status.HTTP_403_FORBIDDEN, 'msg': '用户被禁用，请联系管理员'})

        if token.created < (datetime.datetime.now() - datetime.timedelta(hours=20)).replace(tzinfo=pytz.timezone('UTC')):
            raise exceptions.AuthenticationFailed(
                {'status': status.HTTP_401_UNAUTHORIZED, 'msg': '登录过期，请重新登录'})

        if token:
            token_cache = 'token_' + key
            cache.set(token_cache, token.user, 600)
        
        return token.user, token

    def authenticate_header(self, request):
        return 'Token'
