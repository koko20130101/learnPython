from snippets import serializers
from snippets.models import Snippet, User
from snippets.serializers import SnippetSerializer, UserSerializer
from rest_framework import viewsets, generics, permissions, renderers, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from snippets.permissions import IsOwnerOrReadOnly


# 用户接口视图集
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # 查询是否注册
    @action(methods=['POST'], detail=False)
    def checkRegister(self, request, *args, **kwargs):
        user = self.queryset.filter(id=2).first()
        return Response({
            'status': status.HTTP_200_OK,
            'msg': 'ok',
            'data': {'isRegister': True if user else False}
        }, status=status.HTTP_200_OK)

    # 登录
    @action(methods=['POST'], detail=False)
    def login(self, request, *args, **kwargs):
        user = self.queryset.filter(id=1).first()
        try:
            old_token = Token.objects.get(user=user)
            old_token.delete()
        except:
            pass
        if user:
            token = Token.objects.create(user=user)
            return Response({
                'status': status.HTTP_200_OK,
                'msg': '登录成功',
                'data': {'token': token.key}
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': status.HTTP_200_OK,
                'msg': '您还未注册',
            }, status=status.HTTP_200_OK)

    # 注册
    @action(methods=['POST'], detail=False)
    def register(self, request, *args, **kwargs):
        print(777, request.user)
        return Response({
            'status': status.HTTP_200_OK,
            'msg': 'ok',
            'data': 'haha'
        })

    # 用户信息
    @action(methods=['POST'], detail=False)
    def getUserInfo(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # token有效
            user = self.queryset.filter(id=request.user.id).first()
            serializer = UserSerializer(user)
            return Response({
                'status': status.HTTP_200_OK,
                'msg': 'ok',
                'data': serializer.data
            })
        else:
            return Response({'status': status.HTTP_401_UNAUTHORIZED,'msg':'登录超时'})


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
