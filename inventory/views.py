from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Product
from .forms import ProductForm


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

    return render(request, 'inventory/add_product.html', {"form":form})


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
    
    return render(request, 'inventory/add_product.html', {'form':form, 'product':product})


def delete_product_view(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('inventory:products-list')
    
    return render(request, 'inventory/delete_product.html', {'product':product})




