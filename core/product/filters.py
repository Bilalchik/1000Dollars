import django_filters
from django_filters import rest_framework as filters

from .models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ('brand', 'category', 'min_price', 'max_price')


