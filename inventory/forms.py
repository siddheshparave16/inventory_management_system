from django.forms import ModelForm
from .models import Product, Vendor

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'description', 'price', 'qty', 'vendor_id']


class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'contact_person', 'phone_number', 'email', 'address']
