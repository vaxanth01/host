from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import Profile
from .forms import *



@login_required
def addProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  
            return redirect('home')  
    else:
        form = ProductForm()
    context = {
        'form': form
    }
    return render(request, 'addProduct.html', context)


def addCategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('addCategory')  # Redirect to add product page after adding category
    else:
        form = CategoryForm()
    return render(request, 'addCategory.html', {'form': form})


def addProductGallery(request, product_id):
    product = Product.objects.get(pk=product_id)
    if request.method == 'POST':
        form = ProductGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            product_gallery = form.save(commit=False)
            product_gallery.product = product  # Assign the product to the product_gallery
            product_gallery.save()
            return redirect('product_gallery')  # Redirect to product gallery page after adding image
    else:
        form = ProductGalleryForm()
    return render(request, 'addProductGallery.html', {'form': form})

# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm

def editProduct(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('edit_product', product_id=product.id)  # Redirect to product detail page after editing
    else:
        form = ProductForm(instance=product)
    return render(request, 'edit_Product.html', {'form': form})


def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('home')  # Redirect to the home page after deletion
    return redirect('product_detail', product_id=product_id) 


from django.shortcuts import render
from .models import Notification

def notification(request):
    user_notifications = Notification.objects.filter(user=request.user)
    notification_count = user_notifications.count()
    return render(request, 'notification.html', {'notifications': user_notifications, 'notification_count': notification_count})
