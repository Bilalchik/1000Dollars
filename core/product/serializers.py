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
    main_cover = serializers.ImageField(use_url=True)
    brand = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = '__all__'

    def get_brand(self, obj):
        return obj.brand.title  

    def get_category(self, obj):
        return obj.category.title
    
    def get_status(self, obj):
        return obj.get_status_display()
    
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Стоимость не может быть отрицательной.")
        return value

    def validate_discount_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Стоимость с учетом скидки не может быть отрицательной.")
        return value

    def validate(self, attrs):
        price = attrs.get('price')
        discount_price = attrs.get('discount_price')

        if discount_price > price:
            raise serializers.ValidationError("Стоимость с учетом скидки не может быть больше основной стоимости.")
        
        return attrs

