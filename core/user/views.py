from django.shortcuts import render


class UserView(APIView):


@api_view(['POST'])
def product_create_view(request):
    serializer = UserRegisterSerializer(data=request.data, context={'request': request})

    if serializer.is_valid(raise_exception=True):
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)