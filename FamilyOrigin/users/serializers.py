from rest_framework import fields, serializers
from .models import UserProfile, Area


class UserProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class AreaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'
