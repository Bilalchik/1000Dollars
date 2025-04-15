from rest_framework.views import APIView, Response
from rest_framework import status
from .serializers import MyUserRegisterSerializer, UserResetPasswordSerializer, OTPConfirmSerializer


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


class OTPConfirmView(APIView):
    def post(self, request, user_id):
        serializer = OTPConfirmSerializer(data=request.data, context={'user_id': user_id})
        if serializer.is_valid():
            result = serializer.save()
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
