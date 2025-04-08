from django.contrib.admin.utils import model_ngettext
from rest_framework import serializers
from .models import Product, Banner, Brand


class BannerListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = ('id', 'title', 'description', 'image', 'position')


class BrandListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

