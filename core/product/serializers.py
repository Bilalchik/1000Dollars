<<<<<<< HEAD
=======
from decimal import Decimal

from django.contrib.admin.utils import model_ngettext
>>>>>>> 1c5eea1514c38f1a14ff1ae02f88800ffd4fc008
from rest_framework import serializers
from .models import Product, Banner, Brand, Category, Image


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
    class Meta:
        model = Brand
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    brand = serializers.SlugRelatedField(read_only=True, slug_field='title')
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
