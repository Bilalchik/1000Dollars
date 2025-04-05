from django.db import models

from .choices import ProductStatusEnum


class Category(models.Model):
    title = models.CharField(max_length=221, verbose_name='Название')

    def __str__(self):
        return self.title


class Image(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    file = models.ImageField(upload_to='media/products/detail_image')

    def __str__(self):
        return str(self.file)


#  TODO: Добавить связь с юзером
class Product(models.Model):
    # user = modes.(Fo....)
    title = models.CharField(max_length=221, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Стоимость', default=0)
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Cтоимость c учетом скидки', default=0)
    main_cover = models.ImageField(upload_to='media/products/main_cover', verbose_name='Главное фото')
    is_active = models.BooleanField(default=True)
    status = models.CharField(choices=ProductStatusEnum.choices, default=ProductStatusEnum.ON_SALE)

    def __str__(self):
        return self.title
