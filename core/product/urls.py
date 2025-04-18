from django.urls import path
from . import views
from .views import FavoriteToggleView, FavoriteListView, ProductListView

urlpatterns = [
    path('index/', views.IndexView.as_view()),
    path('index/<int:product_id>/', views.ProductDetailView.as_view()),

    path('favorite/', FavoriteToggleView.as_view(), name='favorite_toggle'),
    path('favorites/', FavoriteListView.as_view(), name='favorite_list'),

    path('products_filter/', ProductListView.as_view(), name='product_list'),

    path('basket/create/', views.BasketCreateView.as_view())
]
