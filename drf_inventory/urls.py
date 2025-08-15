from django.urls import path
from drf_inventory.views import VendorApiView, ProductApiView, get_product_in_price_range
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # jwt token endpoints
    path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),

    # API endpoints for vendor
    path('vendor/', VendorApiView.as_view()),
    path('vendor/<int:vendor_id>/', VendorApiView.as_view()),
    path('vendor/<int:vendor_id>/update', VendorApiView.as_view()),
    path('vendor/<int:vendor_id>/delete', VendorApiView.as_view()),

    # API endpoints for Product
    path('product/', ProductApiView.as_view()),
    path('product/<int:product_id>/', ProductApiView.as_view()),
    path('product/vendor/<int:vendor_id>/', ProductApiView.as_view()),

    path('product/price/', get_product_in_price_range),

]


