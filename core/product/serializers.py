from decimal import Decimal

import data
from django.contrib.admin.utils import model_ngettext
from rest_framework import serializers
from .models import Product, Banner, Brand, Category, Image, Favorite


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'file', 'created_date')


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','title')

class BannerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = ('id', 'title', 'description', 'image', 'position')


class BrandListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = '__all__'

    @staticmethod
    def get_status(self, obj):
        return obj.get_status_display()


class ProductListSerializer(serializers.ModelSerializer):
    category = CategoryListSerializer()
    status = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_discount_price(self, obj):
        percent = Decimal(obj.discount_rate) / Decimal('100')
        discount_price = obj.price * percent
        total_price = obj.price - discount_price
        return total_price

    def get_status(self, obj):
        return obj.get_status_display()


class ProductDetailListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'brand', 'description', 'category', 'description', 'main_cover', 'status', 'created_date',
                  'images')

    @staticmethod
    def get_images(obj):
        images = Image.objects.filter(product__id=obj.id)

        serializer = ImageListSerializer(images, many=True)

        return serializer.data

class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product_id', 'created_at']

class FavoriteListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer()

    class Meta:
        model = Favorite
        fields = ['id', 'product']