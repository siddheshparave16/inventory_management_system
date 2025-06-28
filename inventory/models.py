from django.db import models
from django.forms import ValidationError
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.db import transaction


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
    sku = models.CharField(max_length=20, unique=True,help_text="Stock Keeping Unit")
    description = models.TextField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='products')

    def save(self, *args, **kwargs):
        # First save the product to get an ID
        created = not self.pk       # Check if this is a new product being created
        super().save(*args, **kwargs)

        if created:
            Stock.objects.get_or_create(product=self,
                defaults={
                    'current_qty': 0,
                    'min_qty': 10,
                    'max_qty': 100,
                    'is_active': True
                })

        return self
    

    def __str__(self):
        return f"{self.name} (SKU: {self.sku})"


class Stock(models.Model):
    stock_id = models.BigAutoField(primary_key=True)
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock')
    current_qty = models.PositiveIntegerField()
    min_qty = models.PositiveIntegerField(default=10, help_text="Minimum quantity")
    max_qty = models.PositiveIntegerField(default=100, help_text="maximum quantity to store")
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} (Current: {self.current_qty})"

    class Meta:
        ordering = ['stock_id']
    


def default_delivery_date():
    """ set default delivery date for Purchase Order."""
    return datetime.now().date() + timedelta(days=3)

class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETE', 'Complete'),
        ('CANCEL', 'Cancel')
    ]

    purchase_order_id = models.BigAutoField(primary_key=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateField(auto_now_add=True)
    expected_delivery_date = models.DateField(default=default_delivery_date, auto_now_add=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    qty = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-order_date']
        indexes = [
            models.Index(fields=['vendor', 'status']),
            models.Index(fields=['product', 'order_date']),
        ]

    def clean(self):
        """Additional validation before saving"""
        if 100 >= self.qty <= 0:
            raise ValidationError("Purchasse Quantity should be greter that 0 and Max Stock capacity is 100.")
        
        if not self.product:
            raise ValidationError("Product not mention.")
            
        if not hasattr(self, 'product'):
            raise ValidationError("Product is required.")

    def save(self, *args, **kwargs):
        """Handle complete save operation atomically"""
        with transaction.atomic():
            # Runs clean() and other validations
            self.full_clean()

            # calculate price
            self.unit_price = self.product.price
            self.total_cost = self.qty * self.unit_price

            old_instance = None
            fields_to_check = ['expected_delivery_date', 'status', 'qty']
            changes_detected = False

            if self.pk:
                old_instance = PurchaseOrder.objects.get(pk=self.pk)
                for field in fields_to_check:
                    if getattr(old_instance, field) != getattr(self, field):
                        changes_detected =True
                        break

            super().save(*args, **kwargs)

            # Process stock changes if product exists
            if old_instance:
                self._update_stock(old_status=old_instance.status)

            # create history record only if monitored fields changed
            if changes_detected or not self.pk: # Always create for new records
                self._create_history_record()

    def _update_stock(self, old_status):
        # Stock Management
        if self.product:
            stock = Stock.objects.select_for_update().get(product=self.product)
            #case1: was complete, and now its change in status
            if old_status == "COMPLETE" and self.status != "COMPLETE":
                stock.current_qty -= self.qty

            #case2: now complete
            if self.status == "COMPLETE" and old_status != "COMPLETE":
                stock.current_qty += self.qty

                if stock.current_qty > stock.max_qty:
                    raise ValidationError(f"Maximum stock capacity is {stock.max_qty}.")

            # Validate stock levels
            if stock.current_qty < 0:
                raise ValidationError("Stock cannot be negative.")

            if stock.current_qty > stock.max_qty:
                raise ValidationError(f"Exceeds max stock of {stock.max_qty}")
            
            stock.save()

    def _create_history_record(self):
        # Purchase History Record
        PurchaseHistory.objects.create(
            purchase_order=self,
            product=self.product,
            qty=self.qty,
            unit_price=self.unit_price,
            total_price=self.total_cost,
            status=self.status
        )


    def __str__(self):
        return f"PO-{self.purchase_order_id} | {self.qty}x {self.product.name if self.product else 'No Product'} | ${self.unit_price}"
    
    

class PurchaseHistory(models.Model):
    purchase_id = models.BigAutoField(primary_key=True)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='histories',  db_column='purchase_order_id')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now_add=True)
    qty = models.IntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=PurchaseOrder.STATUS_CHOICES, default="PENDING")

    class Meta:
        ordering = ['-purchase_date']
        verbose_name = 'Purchase History'
        verbose_name_plural = 'Purchase Histories'
        indexes = [
            models.Index(fields=['purchase_order']),
            models.Index(fields=['product', 'purchase_date']),
            models.Index(fields=['status', 'purchase_date']),
        ]

    def __str__(self):
        return f"Purchase History #{self.purchase_id} | {self.product.name} | {self.status}"

    @property
    def vendor(self):
        "Quick access to vendor info"
        self.purchase_order.vendor