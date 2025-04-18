from decimal import Decimal

from django.contrib.admin.utils import model_ngettext
from rest_framework import serializers
from user.models import MyUser
from .models import Product, Banner, Brand, Category, Image, Size, Storage, Basket, Favorite



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
    likes_count = serializers.IntegerField(read_only=True)

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

    def get_discount_price(self, obj):
        percent = Decimal(obj.discount_rate) / Decimal('100')
        discount_price = obj.price * percent
        total_price = obj.price - discount_price
        return total_price

    def get_status(self, obj):
        return obj.get_status_display()


class ProductDetailListSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    sizes = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'brand', 'description', 'category', 'description', 'main_cover', 'status', 'created_date',
                  'images', 'sizes')

    @staticmethod
    def get_images(obj):
        images = Image.objects.filter(product__id=obj.id)

        serializer = ImageListSerializer(images, many=True)

        return serializer.data

    def get_sizes(self, obj):
        all_sizes = Size.objects.all()

        result = {}
        for size in all_sizes:
            is_product_storage_in_stock = Storage.objects.filter(product=obj, size=size, quantity__gt=0).exists()

            result[size.title] = {'id': size.id, 'in_stock': is_product_storage_in_stock}

        return result

class FavoriteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ('product',)

    def create(self, validated_data):
        user = self.context['request'].user
        return Favorite.objects.create(user=user, **validated_data)

class BasketCreateSerializer(serializers.Serializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product')
    quantity = serializers.IntegerField(required=True)
    size = serializers.PrimaryKeyRelatedField(queryset=Size.objects.all())
    delivery_price = serializers.IntegerField(required=True)

    #  {'user': <MyUser: admin>, 'product': <Product: 123123>, 'quantity': 10, 'size': <Size: S>, 'delivery_price': 250}
    def validate(self, attrs):
        storage = Storage.objects.filter(product=attrs['product'], size=attrs['size']).first()

        if storage.quantity < attrs['quantity']:
            raise serializers.ValidationError({'quantity': 'В таком кол-во нету'})

        return attrs


    def create(self, validated_data):

        basket = Basket.objects.create(
            user=validated_data['user'],
            product=validated_data['product'],
            quantity=validated_data['quantity'],
            size=validated_data['size'],
            delivery_price=validated_data['delivery_price'],
        )

        return basket


class FavoriteListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'product', 'created_at')
