from django.shortcuts import render, HttpResponse
from FamilyOrigin.settings import APP_ID, SECRET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from .serializers import UserProfileModelSerializer
from .models import UserProfile, Area
from datetime import datetime
import urllib.request
import hashlib
import time
import json


class LoginView(APIView):
    '''登录'''
    renderer_class = [JSONRenderer]

    def get(self, request):
        code = request.GET.get('code')
        aurl = request.GET.get('avatarUrl')
        nickname = request.GET.get('nickname')
        gender = request.GET.get('gender')
        longitude = request.GET.get('longitude')  # 经度
        latitude = request.GET.get('latitude')  # 纬度
        print(code, nickname, aurl, gender, latitude, longitude)
