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
<<<<<<< HEAD
    brand = serializers.SlugRelatedField(read_only=True, slug_field='title')
    category = serializers.SlugRelatedField(read_only=True, slug_field='title')
    status = serializers.SerializerMethodField()
=======
>>>>>>> 871fa30793a831446398473267ee95216ebe327a

    class Meta:
        model = Product
        fields = ('id', 'title', 'category', 'price', 'discount_price', 'main_cover', 'get_status_display')


    def get_status(self, obj):
        return obj.get_status_display()

