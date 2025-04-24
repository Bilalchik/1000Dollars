from rest_framework.views import APIView, Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from django.db.models import F, Q
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema


from .models import OrderRequest
from .serializers import OrderRequestCreateSerializer
from django.db.models import Count
from product.models import Product, Order
from product.serializers import ProductListSerializer, OrderQrListSerializer, OrderBulkCreateSerializer
from .models import Product, Banner, Brand, Image, Favorite
from .serializers import BannerListSerializer, BrandListSerializer, ProductListSerializer, ProductDetailListSerializer, \
    BasketCreateSerializer, FavoriteListSerializer
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import certifi
print(certifi.where())


class IndexView(APIView):
    # permission_classes = [IsAuthenticated]
    @swagger_auto_schema(responses={200: ProductListSerializer()})
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
    @swagger_auto_schema(responses={200: ProductDetailListSerializer()})
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


class BasketCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: BasketCreateSerializer()})
    def post(self, request):
        serializer = BasketCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(status.HTTP_400_BAD_REQUEST)


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

    @swagger_auto_schema(responses={200: FavoriteListSerializer()})
    def get(self, request):
        user = request.user
        favorites = Favorite.objects.filter(user=user)
        serializer = FavoriteListSerializer(favorites, many=True)

        return Response(serializer.data)




class ProductListView(APIView):
    @swagger_auto_schema(responses={200: ProductListSerializer()})
    def get(self, request):
        products = Product.objects.all()

        # Фильтрация по категории
        category_id = request.query_params.get('category')
        if category_id:
            products = products.filter(category_id=category_id)

        # Фильтрация по бренду
        brand_id = request.query_params.get('brand')
        if brand_id:
            products = products.filter(brand_id=brand_id)

        # Сортировка
        sort_param = request.query_params.get('sort')
        if sort_param == 'newly':
            products = products.order_by('-created_date')
        elif sort_param == 'popular':
            products = products.annotate(likes=Count('favorited_by')).order_by('-likes')
        elif sort_param == 'cheap':
            products = products.order_by('price')
        elif sort_param == 'expensive':
            products = products.order_by('-price')

        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


class OrderBulkCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: OrderBulkCreateSerializer()})
    def post(self, request):
        serializer = OrderBulkCreateSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(status.HTTP_400_BAD_REQUEST)


class OrderQrView(APIView):
    @swagger_auto_schema(responses={200: OrderQrListSerializer()})
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)

        serializer = OrderQrListSerializer(order)

        return Response(serializer.data)


class OrderRequestCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: OrderRequestCreateSerializer()})
    def post(self, request):
        serializer = OrderRequestCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
