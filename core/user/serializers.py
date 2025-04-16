import random
from rest_framework import serializers
from django.conf import settings

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail

from .models import MyUser, OTP
from django.utils import timezone
from datetime import timedelta

# serializers.ModelSerializer
class MyUserRegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=223, required=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(max_length=14, required=True)
    password = serializers.CharField(min_length=8, required=True,  write_only=True)
    confirm_password = serializers.CharField(min_length=8, required=True, write_only=True)

# { "username": "Admin", "email": "bb@ggggggg.com", "phone_number": "996770770550", "password": "123456789"}

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Пароли не совпадают@"})
        return attrs

    def validate_email(self, value):
        if MyUser.objects.filter(email=value).exists():
            raise serializers.ValidationError({"email": "такая почта есть!"})
        return value


    def create(self, validated_data):
        user = MyUser(
            username=validated_data['username'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email'],
            password=make_password(validated_data['password'])
        )
        user.save()
        return user


class UserResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)

    def validate_email(self, value):
        if not MyUser.objects.filter(email=value).exists():
            raise serializers.ValidationError({"email": "Такой почты нету!"})
        return value

    def create(self, validated_data):
        user = MyUser.objects.filter(email=validated_data['email']).first()
        code = self.get_generate_otp_code()
        otp = OTP(
            user=user,
            code=code
        )
        otp.save()
        self.send_user_email(email=validated_data['email'], code=code)
        return otp

    @staticmethod
    def get_generate_otp_code():
        random_code = random.randint(100000, 999999)

        return random_code

    @staticmethod
    def send_user_email(email, code):
        send_mail(
            "OTP",
            f"Ваш одноразовый код.\n{code}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )


class OTPConfirmSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)

    def validate(self, attrs):
        user_id = self.context['user_id']
        code = attrs.get('code')

        try:
            user = MyUser.objects.get(id=user_id)
        except MyUser.DoesNotExist:
            raise serializers.ValidationError({"user": "Пользователь не найден"})

        try:
            otp = OTP.objects.filter(user=user, code=code, if_used=False).latest('created_date')
        except OTP.DoesNotExist:
            raise serializers.ValidationError({"code": "Неверный или уже использованный код"})

        if timezone.now() - otp.created_date > timedelta(minutes=10):
            raise serializers.ValidationError({"code": "Код устарел"})

        otp.if_used = True
        otp.save()
        attrs['user'] = user
        return attrs


class MyUserRestorePasswordSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, trim_whitespace=False)
    confirm_new_password = serializers.CharField(required=True, write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        user = MyUser.objects.filter(id=attrs['user_id']).first()

        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({'password': 'Не похожи'})
        elif not user:
            raise serializers.ValidationError({'user_id': 'Такой id нет'})

        return attrs

    def create(self, validated_data):
        user = MyUser.objects.filter(id=validated_data['user_id']).first()
        user.set_password(validated_data['new_password'])
        user.save()

        return user