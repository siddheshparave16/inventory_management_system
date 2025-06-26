from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (
                    dashboard, products_list_view, product_detail_view,
                    create_product_view, update_product_view, delete_product_view,
                    vendor_list_view, vendor_details_view, create_vendor_view, update_vendor_view,
                    delete_vendor_view,

                    )

app_name = 'inventory'

urlpatterns = [
    path('', dashboard, name='home-dashboard'),
    # views for product
    path('product/', products_list_view, name='products-list'),
    path('product/<int:product_id>/', product_detail_view, name='product-details'),
    path('product/new/', create_product_view, name='product-create'),
    path('product/<int:product_id>/update/', update_product_view, name='product-update'),
    path('product/<int:product_id>/delete', delete_product_view, name="product-delete"),

    # views for vendor
    path('vendor/', vendor_list_view, name='vendors-list'),
    path('vendor/<int:vendor_id>/', vendor_details_view, name='vendor-details'),
    path('vendor/new/', create_vendor_view, name='vendor-create'),
    path('vendor/<int:vendor_id>/update/', update_vendor_view, name='vendor-update'),
    path('vendor/<int:vendor_id>/delete/', delete_vendor_view, name='vendor-delete')

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
