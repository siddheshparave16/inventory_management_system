from django.contrib import admin
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import (
    Vendor, Product, Stock, PurchaseOrder, PurchaseHistory
    )


# Register your models here.

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['vendor_id', 'name', 'contact_person', 'phone_number', 'email']
    list_filter = ['name', 'created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'name', 'sku', 'price']
    exclude = ['vendor_id']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['stock_id', 'product', 'current_qty', 'last_updated']


@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['purchase_order_id', 'vendor', 'order_date', 'expected_delivery_date', 'status', 'total_cost', 'product', 'qty', 'unit_price']
    ordering = ['-order_date']


@admin.register(PurchaseHistory)
class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ['purchase_id', 'purchase_order', 'product', 'purchase_date', 'qty', 'unit_price', 'total_price', 'status']
    