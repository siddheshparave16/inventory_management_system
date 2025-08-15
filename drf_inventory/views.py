from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from inventory.models import Vendor, Product
from drf_inventory.serializers import VendorSerializer, ProductSerializer, PurchaseOrderSerializer
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class VendorApiView(APIView):
    """CRUD operations for Vendor"""

    def get(self, request, vendor_id=None):
        """
        Handles GET requests for Vendor:
        - If vendor_id is provided, fetch the specific vendor.
        - Otherwise, fetch all vendors.
        """
        if vendor_id:
            vendor = Vendor.objects.get(vendor_id=vendor_id)
            serializer = VendorSerializer(vendor)
        else:
            # Fetch all vendors from the database
            vendors_list = Vendor.objects.all()
            # Serialize the vendor list with pagination
            serializer = VendorSerializer(vendors_list, many=True)

        return Response(serializer.data)

    def post(self, request):
        """
        Handles POST requests to create a new Vendor.
        - Validates the data and saves the new Vendor object.
        """
        serializer = VendorSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_vendor(self, vendor_id):
        """
        Helper method to fetch a Vendor by its ID.
        - Raises Http404 if the Vendor does not exist.
        """
        try:
            return Vendor.objects.get(vendor_id=vendor_id)
        except Vendor.DoesNotExist:
            raise Http404("Vendor does not exist.")

    def put(self, request, vendor_id):
        """
        Handles PUT requests to update a Vendor's details.
        - Fetches the Vendor using vendor_id and updates it with the provided data.
        """
        vendor = self.get_vendor(vendor_id=vendor_id)
        serializer = VendorSerializer(vendor, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_id):
        """
        Handles DELETE requests to remove a Vendor by its ID.
        """
        vendor = self.get_vendor(vendor_id=vendor_id)
        vendor.delete()
        return Response(status=status.HTTP_200_OK)


class ProductApiView(APIView):
    """CRUD operations for Product"""
    authentication_classes = [JWTAuthentication]        # JWT Token Authentication required
    permission_classes = [IsAuthenticated]              # Requires an authenticated user

    def get_product(self, product_id):
        """
        Helper method to fetch a Product by its ID.
        - Raises Product.DoesNotExist if the product does not exist.
        """
        return Product.objects.get(product_id=product_id)

    def get(self, request, product_id=None, vendor_id=None):
        """
        Handles GET requests for Products:
        - Fetch all products if no product_id or vendor_id is provided.
        - Fetch a specific product by product_id.
        - Fetch all products associated with a specific vendor using vendor_id.
        """
        # Case: Fetch all Product list
        if product_id is None and vendor_id is None:
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

        # Fetch product by product_id
        if product_id is not None:
            try:
                product = self.get_product(product_id=product_id)
                serializer = ProductSerializer(product)
                return Response(serializer.data)
            except Product.DoesNotExist:
                return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        # Fetch products related to a specific vendor
        if vendor_id is not None:
            try:
                vendor = Vendor.objects.get(pk=vendor_id)
                products = Product.objects.filter(vendor=vendor)
                serializer = ProductSerializer(products, many=True)
                return Response(serializer.data)
            except Vendor.DoesNotExist:
                return Response({"detail": "Vendor not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@authentication_classes([JWTAuthentication])        # JWT Token Authentication
@permission_classes([IsAuthenticated])              # Requires an authenticated user
def get_product_in_price_range(request):
    """
    Fetches products within a specified price range.

    Query Parameters:
    - min_price (default: 0): The minimum price of products to fetch.
    - max_price (optional): The maximum price of products to fetch.

    Returns:
    - A list of products within the price range in JSON format.
    - If max_price is not provided, fetches all products above min_price.

    Example Request:
    GET /api/product/price/?min_price=5&max_price=10

    Response:
    - HTTP 200: List of products within the price range.
    - HTTP 400: Invalid price range input.
    """
    try:
        min_price = request.GET.get('min_price', 0)
        max_price = request.GET.get('max_price', None)

        min_price = float(min_price)
        max_price = float(max_price) if max_price else None

        # Filter products based on price range
        if max_price is not None:
            products = Product.objects.filter(price__gte=min_price, price__lte=max_price)
        else:
            products = Product.objects.filter(price__gte=min_price)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ValueError:
        return Response({"error": "Invalid Price range."}, status=status.HTTP_400_BAD_REQUEST)
