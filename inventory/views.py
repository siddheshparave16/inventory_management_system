from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Vendor
from .forms import ProductForm, VendorForm


@login_required
def dashboard(request):
    return render(request, 'inventory/home.html')


def products_list_view(request):
    products_list = Product.objects.all()
    return render(request, 'inventory/products_list.html', {"products_list":products_list})


def product_detail_view(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        raise ValueError("Product Does Not Exist.")
    
    return render(request, 'inventory/products_details.html', {"product": product})


def create_product_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            product = form.save()
            messages.success(request, f"New Product '{product.name}' is created.")
            return redirect("inventory:product-details", product_id= product.pk)
    else:
        form = ProductForm()

    return render(request, 'inventory/product_form.html', {"form":form})


def update_product_view(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)

        if form.is_valid():
            product = form.save()
            messages.success(request, "Product updated successfully.")
            return redirect('inventory:product-details', product_id=product.product_id)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'inventory/product_form.html', {'form':form, 'product':product})


def delete_product_view(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('inventory:products-list')
    
    return render(request, 'inventory/delete_product.html', {'product':product})


def vendor_list_view(request):
    vendors_list = Vendor.objects.all()
    return render(request, 'inventory/vendors_list.html', {'vendors_list':vendors_list})


def vendor_details_view(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)
    return render(request, 'inventory/vendor_details.html', {'vendor':vendor})


def create_vendor_view(request):
    if request.method=='POST':
        form = VendorForm(request.POST)

        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.email = form.cleaned_data['email']
            vendor.save()
            messages.success(request, "New Vendor Created Successfully.")
            return redirect('inventory:vendor-details', vendor_id=vendor.vendor_id)
    else:
        form = VendorForm()
    
    return render(request, 'inventory/vendor_form.html', {'form': form})


def update_vendor_view(request, vendor_id):
    vendor = get_object_or_404(Vendor, vendor_id=vendor_id)

    if request.method=='POST':
        form = VendorForm(request.POST, instance=vendor)

        if form.is_valid():
            vendor = form.save(commit=False)
            vendor.email = form.cleaned_data['email']
            vendor.save()
            messages.success(request, "Vendor Updated Successfully.")
            return redirect('inventory:vendor-details', vendor_id=vendor.vendor_id)
    else:
        form = VendorForm(instance=vendor)
    
    return render(request, 'inventory/vendor_form.html', {'form': form})

def delete_vendor_view(request, vendor_id):
    vendor = get_object_or_404(Vendor, vendor_id=vendor_id)

    if request.method == 'POST':
        vendor.delete()
        messages.success(request, "Vendor deleted successfully.")
        return redirect('inventory:vendors-list')

    return render(request, 'inventory/delete_vendor.html', {'vendor':vendor})

