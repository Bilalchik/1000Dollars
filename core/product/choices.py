from django.db import models


class ProductStatusEnum(models.TextChoices):
    SOON_ON_SALE = ('soon_on_sale', 'Скоро в продаже')
    ON_SALE = ('on_sale', 'В продаже')
    OUT_OF_STOCK = ('out_of_stock', 'Нет в наличии')
