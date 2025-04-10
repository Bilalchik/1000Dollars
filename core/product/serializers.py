import data
from django.contrib.admin.utils import model_ngettext
from rest_framework import serializers
from .models import Product, Banner, Brand, Category


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

    class Meta:
        model = Product
        fields = '__all__'

    def get_status(self, obj):
        return obj.get_status_display()


    @staticmethod
    def get_status(self, obj):
        return obj.get_status_display()

    def validate(self, data):
        price = data.get('price')
        discount_price = data.get('discount_price')

        if discount_price > price:
            raise serializers.ValidationError({
                'discount_price': 'Цена со скидкой не может быть выше обычной цены.'
            })

        return data
