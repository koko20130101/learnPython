from snippets import serializers
from snippets.models import Snippet, User
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import viewsets, generics, permissions, renderers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
# from django.contrib.auth.models import User
from snippets.permissions import IsOwnerOrReadOnly


# 用户接口视图集
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # 查询是否注册
    @action(detail=False)
    def checkRegister(self, request, *args, **kwargs):
        user = self.queryset.filter(id=1).first()
        return Response({
            'status': status.HTTP_200_OK,
            'msg': 'ok',
            'data': {'isRegister': True if user else False}
        }, status=status.HTTP_200_OK)

    # 登录
    @action(detail=False)
    def login(self, request, *args, **kwargs):
        user = self.queryset.filter(id=2).first()
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        else:
            return Response({
                'status': status.HTTP_200_OK,
                'msg': '您还注册',
            }, status=status.HTTP_200_OK)


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# class CheckRegister(generics.GenericAPIView):
    '''检查是否注册'''
    # renderer_class = [JSONRenderer]

    # def post(self, request):
    #     jsCode = request.data.get('jsCode')
    #     if jsCode:
    #         sessionInfo = getSessionInfo(jsCode)
    #         openId = sessionInfo['openid']
    #         if openId:
    #             wxuser = Users.objects.filter(openId=openId).first()
    #             return Response({
    #                 'status': status.HTTP_200_OK,
    #                 'msg': 'ok',
    #                 'data': {'isRegister': True if wxuser else False}
    #             }, status=status.HTTP_200_OK)
    #     else:
    #         return Response(status=status.HTTP_404_NOT_FOUND)


class Login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(id=1).first()
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            })
        else:
            return Response({
                'status': status.HTTP_200_OK,
                'token': ''
            })
