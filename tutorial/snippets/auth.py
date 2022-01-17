import datetime
# from django.utils.translation import ugettext_lazy
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework.authtoken.models import Token
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
            raise exceptions.AuthenticationFailed('认证失败')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('用户被禁用')

        if (datetime.datetime.now() - token.created) > datetime.timedelta(hours=0.1*1):
            raise exceptions.AuthenticationFailed('认证信息已过期')

        if token:
            token_cache = 'token_' + key
            cache.set(token_cache, token.user, 600)

        return token.user, token

    def authenticate_header(self, request):
        print(4)
        return 'Token'
