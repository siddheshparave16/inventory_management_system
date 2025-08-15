from django.forms import ModelForm
from .models import Product, Vendor, PurchaseOrder

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sku', 'description', 'price', 'vendor']


class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'contact_person', 'phone_number', 'email', 'address']


class PurchaseOrderForm(ModelForm):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"
        exclude = ['order_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make these fields readonly and add special classes
        self.fields['unit_price'].widget.attrs.update({
            'readonly': True,
            'class': 'readonly-field'
        })
        self.fields['total_cost'].widget.attrs.update({
            'readonly': True,
            'class': 'readonly-field'
        })

        if self.instance and self.instance.pk and self.instance.product :
            self.fields['vendor'].disabled = True
            self.fields['vendor'].help_text = "Vendor cannot be changed after creation"

            self.initial['unit_price'] = self.instance.product.price
            if self.initial.get('unit_price') and self.initial.get('qty'):
                self.initial['total_cost'] = self.initial['qty'] * self.initial['unit_price']

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')

        if product:
            # Get current stock info
            stock = product.stock
            qty = self.cleaned_data.get('qty', 0)
            cleaned_data['unit_price'] = product.price
            cleaned_data['total_cost'] = qty * product.price
        
        return cleaned_data
