from django.contrib import admin
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from .models import (
    Vendor, Product, Stock, PurchaseOrder, PurchaseOrderDetails, PurchaseHistory
    )


# Register your models here.

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ['vendor_id', 'name', 'contact_person', 'phone_number', 'email']
    list_filter = ['name', 'created_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'name', 'sku', 'price', 'qty']
    exclude = ['vendor_id']


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['stock_id', 'product', 'current_qty', 'last_updated']
    ordering = ['-current_qty']

