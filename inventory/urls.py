from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
                    dashboard, products_list_view, product_detail_view,
                    create_product_view, update_product_view, delete_product_view
                    )

app_name = 'inventory'

urlpatterns = [
    path('', dashboard, name='home-dashboard'),
    path('product/', products_list_view, name='products-list'),
    path('product/<int:product_id>/', product_detail_view, name='product-details'),
    path('product/new/', create_product_view, name='product-create'),
    path('product/<int:product_id>/update/', update_product_view, name='product-update'),
    path('product/<int:product_id>/delete', delete_product_view, name="product-delete"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
