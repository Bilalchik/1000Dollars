from django.db import models
from django.core.validators import MaxValueValidator

from .choices import ProductStatusEnum, BannerPositionEnum


class Category(models.Model):
    title = models.CharField(max_length=221, verbose_name='Название')
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
    discount_rate = models.PositiveSmallIntegerField(validators=[MaxValueValidator(100)])
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Cтоимость c учетом скидки', default=0)
    main_cover = models.ImageField(upload_to='media/products/main_cover', verbose_name='Главное фото')
    is_active = models.BooleanField(default=True)
    status = models.CharField(choices=ProductStatusEnum.choices, default=ProductStatusEnum.ON_SALE, max_length=13)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


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


class Size(models.Model):
    title = models.CharField(max_length=221, verbose_name='Название')
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title
