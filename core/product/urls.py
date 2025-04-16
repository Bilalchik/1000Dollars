from django.urls import path
from . import views
from .views import FavoriteToggleView, FavoriteListView

urlpatterns = [
    path('index/', views.IndexView.as_view()),
    path('index/<int:product_id>/', views.ProductDetailView.as_view()),
    path('favorite/', FavoriteToggleView.as_view(), name='favorite-toggle'),
path('favorites/', FavoriteListView.as_view(), name='favorite-list'),
]
