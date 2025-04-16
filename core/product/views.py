from rest_framework import status
from rest_framework.views import APIView, Response
from django.db.models import F, Q
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings

from .models import Product, Banner, Brand, Favorite
from .serializers import BannerListSerializer, BrandListSerializer, ProductListSerializer, ProductDetailListSerializer, \
    FavoriteListSerializer
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import certifi
print(certifi.where())


class IndexView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        banners = Banner.objects.filter(is_active=True)
        brands = Brand.objects.filter(is_active=True)

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

        data = {
            "product_detail": product_serializer.data,
            "similar_products": similar_products_serializer.data
        }
        return Response(data)


class FavoriteToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")
        product = get_object_or_404(Product, id=product_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

        if not created:
            favorite.delete()
            return Response({"detail": "Removed from favorites"}, status=status.HTTP_200_OK)
        return Response({"detail": "Added to favorites"}, status=status.HTTP_201_CREATED)


class FavoriteListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        favorites = Favorite.objects.filter(user=user)
        serializer = FavoriteListSerializer(favorites, many=True)

        return Response(serializer.data)