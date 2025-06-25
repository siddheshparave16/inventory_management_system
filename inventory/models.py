from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField 


# Create your models here.

class Vendor(models.Model):
    vendor_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    contact_person = models.CharField(max_length=255)
    phone_number = PhoneNumberField(unique=True, region='IN')
    email = models.EmailField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=20, unique=True,help_text="Stock Keeping Unit is a unique, alphanumeric code for product to identify and track its inventory")
    description = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.IntegerField(help_text="Product Quantity")
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f"{self.name} (SKU: {self.sku})"

    def get_absolute_url(self):
        return reverse('inventory:product-details', kwargs={'product_id': self.product_id})

class Stock(models.Model):
    stock_id = models.BigAutoField(primary_key=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock')
    current_qty = models.IntegerField()
    min_qty = models.IntegerField()
    max_qty = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Stock for {self.product.name}"


class PurchaseOrder(models.Model):

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETE', 'Complete'),
        ('CANCEL', 'Cancel')
    ]

    purchase_order_id = models.BigAutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateField(auto_now_add=True)
    expected_delivery_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"PO-{self.purchase_order_id} ({self.status})"


class PurchaseOrderDetails(models.Model):
    id = models.BigAutoField(primary_key=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='order_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.qty} x {self.product.name} @ {self.unit_price}"
    
    class Meta:
        verbose_name = "Purchase Order Detail"


class PurchaseHistory(models.Model):
    purchase_id = models.BigAutoField(primary_key=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='history')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)
    qty = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Purchase #{self.purchase_id} - {self.product.name}"
