from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from user.serializers import UserRegisterSerializer


class MyUserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Пользователь успешно зарегистрирован!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)