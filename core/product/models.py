from django.core.validators import MaxValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError

from .choices import ProductStatusEnum, BannerPositionEnum, OrderStatusEnum
from user.models import MyUser


class Category(models.Model):
    title = models.CharField(max_length=221, verbose_name='Категория')
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    file = models.ImageField(upload_to='media/products/detail_image')
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.file)


class Brand(models.Model):
    logo = models.ImageField(upload_to='media/brands/logo')
    title = models.CharField(max_length=221, verbose_name='Название')
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.title


#  TODO: Добавить связь с юзером
class Product(models.Model):
    # user = modes.(Fo....)
    title = models.CharField(max_length=221, verbose_name='Название')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Стоимость', default=0)
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Cтоимость c учетом скидки',
                                         default=0)
    main_cover = models.ImageField(upload_to='media/products/main_cover', verbose_name='Главное фото')
    is_active = models.BooleanField(default=True)
    status = models.CharField(choices=ProductStatusEnum.choices, default=ProductStatusEnum.ON_SALE, max_length=13)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.discount_price > self.price:
            raise ValidationError({
                'discount_price': 'Цена со скидкой не может быть выше обычной цены.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title


class Banner(models.Model):
    title = models.CharField(max_length=221, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='media/banner')
    position = models.CharField(choices=BannerPositionEnum.choices, verbose_name='Расположение', max_length=18)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title



class Favorite(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Чтобы один и тот же юзер не мог лайкнуть продукт дважды

    def __str__(self):
        return f"{self.user} → {self.product}"


class Size(models.Model):
    title = models.CharField(max_length=221, verbose_name='Название')
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title


class Storage(models.Model):
    # user = models.ForeignKey(MyUser, )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='storages')
    quantity = models.PositiveSmallIntegerField()
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='storages')
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.product)


class Basket(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='baskets')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='baskets')
    quantity = models.PositiveSmallIntegerField()
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='baskets')
    delivery_price = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    total_price = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} --> {self.product}"


class Order(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='orders')
    baskets = models.ManyToManyField(Basket)
    order_number = models.PositiveBigIntegerField()
    total_price = models.DecimalField(decimal_places=2, max_digits=12, default=0)
    address = models.CharField(max_length=225)
    status = models.CharField(choices=OrderStatusEnum.choices, default=OrderStatusEnum.IN_PROGRESS, max_length=13)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class Qr(models.Model):
    qr_image = models.ImageField(upload_to='media/qr')


class OrderRequest(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='order_requests')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    paycheck = models.ImageField(upload_to='media/order_requests')
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)

