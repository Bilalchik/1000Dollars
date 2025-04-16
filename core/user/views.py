from rest_framework.views import APIView, Response
from rest_framework import status
from .serializers import MyUserRegisterSerializer, UserResetPasswordSerializer, MyUserRestorePasswordSerializer


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


class MyUserRestorePasswordView(APIView):
    def post(self, request):
        serializer = MyUserRestorePasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(status.HTTP_400_BAD_REQUEST)
