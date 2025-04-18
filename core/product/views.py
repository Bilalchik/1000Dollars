from rest_framework.views import APIView, Response
from rest_framework import status
from django.db.models import F, Q, Count
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings

from .models import Product, Banner, Brand, Image,Favorite
from .serializers import (BannerListSerializer, BrandListSerializer, ProductListSerializer,
                          ProductDetailListSerializer,BasketCreateSerializer, FavoriteCreateSerializer,
                          FavoriteListSerializer)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import certifi
print(certifi.where())


class IndexView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        banners = Banner.objects.filter(is_active=True)
        brands = Brand.objects.filter(is_active=True)

        print(request.query_params)
        if 'sort' in request.query_params:

            if request.query_params['sort'] == 'newly':
                banners.order_by('-created_date')

        # TODO: Фильтрация пол самым продаваемым
        best_sellers_products = Product.objects.filter(is_active=True)
        promo_products = Product.objects.filter(discount_price__lt=F('price'), discount_price__gt=0)

        banners_serializer = BannerListSerializer(banners, many=True)
        brands_serializer = BrandListSerializer(brands, many=True)
        best_sellers_products_serializer = ProductListSerializer(best_sellers_products, many=True)
        promo_products_serializer = ProductListSerializer(promo_products, many=True)

        data = {
            "banners": banners_serializer.data,
            "brands": brands_serializer.data,
            "best_sellers_products": best_sellers_products_serializer.data,
            "promo_products": promo_products_serializer.data
        }

        return Response(data)



class ProductDetailView(APIView):
    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        similar_products = Product.objects.filter(category=product.category).exclude(id=product_id)

        product_serializer = ProductDetailListSerializer(product)
        similar_products_serializer = ProductListSerializer(similar_products, many=True)


        # Image.objects.filter(product=product)
        # product.images

        data = {
            "product_detail": product_serializer.data,
            "similar_products": similar_products_serializer.data
        }
        return Response(data)


class FavoriteCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FavoriteCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Продукт добавлен в избранное!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoriteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user)
        serializer = FavoriteListSerializer(favorites, many=True)
        return Response(serializer.data)


class BasketCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BasketCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(status.HTTP_400_BAD_REQUEST)

class ProductListView(APIView):
    def get(self, request):
        sort = request.query_params.get('sort')

        # аннотируем количество лайков (избранных)
        products = Product.objects.annotate(
            likes_count=Count('favorites')  # name of related_name (по умолчанию modelname_set)
        )

        if sort == 'popular':
            products = products.order_by('-likes_count')
        elif sort == 'new':
            products = products.order_by('-created_at')
        elif sort == 'cheap':
            products = products.order_by('price')
        elif sort == 'expensive':
            products = products.order_by('-price')

        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)