from rest_framework import serializers
from .models import MyUser


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = MyUser
        fields = ['email', 'phone_number', 'username', 'password']

    def validate_email(self, value):

        if MyUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже зарегистрирован.")
        return value

    def validate_username(self, value):

        if MyUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Пользователь с таким именем уже зарегистрирован.")
        return value

    def validate_phone_number(self, value):

        if value and MyUser.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Пользователь с таким номером телефона уже зарегистрирован.")
        return value

    def create(self, validated_data):
        user = MyUser.objects.create_user(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user
