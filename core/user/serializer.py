from rest_framework import serializers
from .models import MyUser


class UserRegisterSerializer(serializers.Serializer):
    class Meta:
        model = MyUser
        fields = '__all__'

        if