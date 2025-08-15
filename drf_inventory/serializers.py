from rest_framework import serializers
from inventory.models import Vendor, Product, PurchaseOrder, PurchaseHistory, Stock



class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'contact_person', 'phone_number', 'email', 'address']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'description', 'price', 'vendor_id']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['vendor', 'expected_delivery_date', 'status', 'notes', 'product', 'qty', 'unit_price', 'total_cost']
