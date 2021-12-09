from rest_framework import fields, serializers
from .models import Users


class UserProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'