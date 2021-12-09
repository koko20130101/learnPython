from django.shortcuts import render, HttpResponse
from FamilyOrigin.settings import APP_ID, SECRET
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from .serializers import UserProfileModelSerializer
from .models import Users
from datetime import datetime
import urllib.request
import hashlib
import time
import json


class Login(generics.GenericAPIView):
    '''登录'''
    renderer_class = [JSONRenderer]

    def post(self, request):
        jsCode = request.data.get('jsCode')
        if jsCode:
            url = "https://api.weixin.qq.com/sns/jscode2session?appid=" + APP_ID + \
                "&secret=" + SECRET + "&js_code=" + jsCode + "&grant_type=authorization_code"
            res = urllib.request.urlopen(url)
            content = res.read().decode()
            obj = json.loads(content)
            openid = obj["openid"]
            print(openid)
            if openid:
                # 生成token，加密
                i = int(time.time())
                s = str(i)
                sha = hashlib.sha1()
                sha.update((openid+s).encode('utf-8'))
                token = sha.hexdigest()
                wxuser = Users.objects.filter(openId=openid).first()
                if wxuser:
                    # 如果登录过，就将token值更新
                    wxuser.token = token
                    wxuser.last_login = datetime.now()
                    wxuser.save()

                return Response({
                    'status': status.HTTP_200_OK,
                    'msg': 'ok',
                    'data': {'token': token, 'isRegister': True if wxuser else False}
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': status.HTTP_401_UNAUTHORIZED,
                    'msg': 'jsCode不能为空',
                    'data': {}
                }, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Register(generics.GenericAPIView):
    '''注册'''

    def post(self, request):
        token = request.data.get('token')
        encryptedData = request.data.get('encryptedData')
        iv = request.data.get('iv')
        inviteUserId = request.data.get('inviteUserId')

        if token and encryptedData and iv:
            # wxuser = Users.objects.filter(openId=555).first()
            print(request.data)
            serializer = UserProfileModelSerializer(data={'realName':'8888'})
            # if serializer.is_valid():
            serializer.save()
            return Response({'token': token, 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
            # return Response({'msg': '该用户已注册', 'status': status.HTTP_401_UNAUTHORIZED}, status=status.HTTP_200_OK)
        else:
            msg = 'token' if not token else 'encryptedData' if not encryptedData else 'iv' if not iv else ''
            return Response({'status': status.HTTP_403_FORBIDDEN, 'msg': msg + '不能为空'}, status=status.HTTP_403_FORBIDDEN)
