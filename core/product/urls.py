from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.IndexView.as_view()),
    path('index/<int:product_id>/', views.ProductDetailView.as_view()),
    path('basket/create/', views.BasketCreateView.as_view()),

    path('order/bulk_create/', views.OrderBulkCreateView.as_view()),
    path('order/qr_list/<int:order_id>/', views.OrderQrView.as_view())

]
