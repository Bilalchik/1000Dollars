from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.IndexView.as_view()),
    path('index/<int:product_id>/', views.ProductDetailView.as_view()),
    path('favorites/create/', views.FavoriteCreateView.as_view(), name='favorite-create'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorite-list'),
    path('basket/create/', views.BasketCreateView.as_view())
]
