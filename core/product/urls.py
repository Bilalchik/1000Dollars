from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.IndexView.as_view()),
    path('index/<int:product_id>/', views.ProductDetailView.as_view()),

    path('favorites/create/', views.FavoriteCreateView.as_view(), name='favorite-create'),
    path('favorites/', views.FavoriteListView.as_view(), name='favorite-list'),

    path('basket/create/', views.BasketCreateView.as_view()),

    path('order/bulk_create/', views.OrderBulkCreateView.as_view()),
    path('order/qr_list/<int:order_id>/', views.OrderQrView.as_view()),
    path('orders/', views.OrderListView.as_view(), name='order-list'),  # Список заказов
    path('orders/<int:order_id>/', views.OrderDetailView.as_view(), name='order-detail'),
]
