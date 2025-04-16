from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import MyUserRegisterSerializer, UserResetPasswordSerializer, MyUserRestorePasswordSerializer, \
    OTPConfirmSerializer


class MyUserRegisterView(APIView):
    def post(self, request):
        serializer = MyUserRegisterSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(status.HTTP_400_BAD_REQUEST)


class MyUserResetPasswordView(APIView):
    def post(self, request):
        serializer = UserResetPasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(status.HTTP_400_BAD_REQUEST)

class ConfirmOTPView(APIView):
    def post(self, request, user_id):
        serializer = OTPConfirmSerializer(data=request.data, context={'user_id': user_id})

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Успешный вход'
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyUserRestorePasswordView(APIView):
    def post(self, request):
        serializer = MyUserRestorePasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(status.HTTP_400_BAD_REQUEST)

class MyUserDeactivateView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user  # текущий юзер из токена
        user.is_active = False
        user.save()
        return Response({'message': 'Пользователь успешно деактивирован'}, status=status.HTTP_200_OK)