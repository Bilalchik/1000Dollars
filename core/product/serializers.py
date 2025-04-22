from decimal import Decimal
from random import randint
from django.contrib.admin.utils import model_ngettext
from django.db.models import Sum

from rest_framework import serializers
from .serializers import BasketCreateSerializer
from user.models import MyUser
from .models import Product, Banner, Brand, Category, Image, Size, Storage, Basket, Order, Qr, Favorite


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

        product = validated_data['product']
        quantity = validated_data['quantity']

        total_price = product.price * quantity


        basket = Basket.objects.create(
            user=validated_data['user'],
            product=product,
            quantity=quantity,
            total_price=total_price,
            size=validated_data['size'],
            delivery_price=validated_data['delivery_price'],
        )

        return basket


class FavoriteListSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'product', 'created_at')

class OrderBulkCreateSerializer(serializers.Serializer):
    baskets_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)    # [1, 2, 3, 4]
    address = serializers.CharField()


    def create(self, validated_data):
        baskets_ids = validated_data['baskets_ids']   # [1, 2, 3, 4]

        baskets = Basket.objects.filter(id__in=baskets_ids)
        total_price = baskets.aggregate(totals=Sum('total_price'))['totals']

        order = Order.objects.create(
            user=self.context['request'].user,
            order_number=self.get_random_number_by_id(),
            total_price=total_price,
            address=validated_data['address']
        )
        order.baskets.set(baskets)
        order.save()

        return order

    def to_representation(self, instance):
        data = {
            "order_id": instance.id
        }

        return data

    @staticmethod
    def get_random_number_by_id():
        while True:
            random_number = randint(100000, 999999)

            if not Order.objects.filter(order_number=random_number).exists():
                return random_number


class QrListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Qr
        fields = ('id', 'qr_image')


class OrderQrListSerializer(serializers.ModelSerializer):
    qr_image = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ('total_price', 'qr_image')

    def get_qr_image(self, obj):
        qr = Qr.objects.all()
        serializer = QrListSerializer(qr, many=True)

        return serializer.data

class OrderListSerializer(serializers.ModelSerializer):
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    status = serializers.CharField()
    created_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Order
        fields = ('id', 'order_number', 'total_price', 'status', 'created_date')

class OrderDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    baskets = BasketCreateSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    status = serializers.CharField()
    address = serializers.CharField()

    class Meta:
        model = Order
        fields = ('id', 'user', 'order_number', 'total_price', 'status', 'address', 'baskets', 'created_date', 'update_date')
