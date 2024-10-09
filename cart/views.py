from django.shortcuts import render, redirect ,get_object_or_404
from store.models import Product
from .models import Cart ,CartItem
from app.models import *
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart 


def add_cart(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    if current_user.is_authenticated:
        try:
          pass
        except:
            pass 

        try:
          cart_item = CartItem.objects.get(user=current_user,product=product)
          cart_item.quantity +=1
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
            product = product,
            quantity =1,
            user = current_user
        )
         
        cart_item.save()

        return redirect('cart')
    else:
        try:
          cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id= _cart_id(request)
            )  
            cart.save()  
        try:
           cart_item = CartItem.objects.get(cart=cart, product=product)
           cart_item.quantity +=1
           cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product =product,
                cart = cart,
                quantity = 1
            )
            cart_item.save()  
        return redirect('store')      

from django.shortcuts import get_object_or_404, redirect
from .models import Product, CartItem, Cart

def remove_cart(request, product_id):
    current_user = request.user
    if current_user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, user=current_user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
        return redirect('cart')

def remove_cart_item(request, product_id):
    current_user = request.user
    if current_user.is_authenticated:
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, user=current_user)
        cart_item.delete()
        return redirect('cart')
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()
        return redirect('cart')

from decimal import Decimal

from decimal import Decimal
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from .models import CartItem
from django.db.models import DecimalField, F, Sum
def cart(request):
    total = Decimal('0')
    quantity = 0
    cart_items = None
    discount_percent = Decimal('0')  # Initialize discount percent
    discount_amount = Decimal('0')
    
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
       
        for cart_item in cart_items:
            # Check if the product has any associated discount types
            if cart_item.product.discount_types.exists():
                # Apply different discounts based on quantity ranges
                if 10 <= cart_item.quantity < 20:
                    discount = Decimal('0.05')  # 5% discount
                elif 20 <= cart_item.quantity < 40:
                    discount = Decimal('0.08')  # 8% discount
                elif 40 <= cart_item.quantity <= 100:
                    discount = Decimal('0.10')  # 10% discount
                else:
                    discount = Decimal('0')  # No discount
                
                # Calculate the discounted price
                discounted_price = Decimal(cart_item.product.price) * (Decimal('1') - discount)
                
                # Update the final price based on the updated quantity and discount
                cart_item.final_price = discounted_price * cart_item.quantity
                
                # Calculate discounted price per item
                cart_item.discounted_price = cart_item.final_price / cart_item.quantity
            else:
                # If no discount types are associated with the product, use the regular price
                cart_item.discounted_price = cart_item.product.price
                cart_item.final_price = cart_item.discounted_price * cart_item.quantity
                
            total += cart_item.final_price
            quantity += cart_item.quantity
        
        # Apply total price-based discount
        if total > Decimal('50000'):
            discount_percent = Decimal('0.10')  # 10% discount
        elif total > Decimal('20000'):
            discount_percent = Decimal('0.05')  # 5% discount
        elif total > Decimal('5000'):
            discount_percent = Decimal('0.03')  # 3% discount
        
        # Calculate the discount amount and final total price
        discount_amount = total * discount_percent
        final_total_price = total - discount_amount
    
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'discount_percent': discount_percent * 100,  # Convert to percentage format (e.g. 10% instead of 0.10)
        'discount_amount': discount_amount,
        'final_total_price': final_total_price,
    }
    return render(request, 'store/cart.html', context)


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

@login_required
def update_cart_item(request, product_id):
    # Ensure the user is logged in and filter by the current user and product_id
    cart_item = get_object_or_404(CartItem, product_id=product_id, user=request.user)

    if request.method == 'POST':
        # Get the new quantity from the POST data
        quantity = int(request.POST.get('quantity'))

        # Update the quantity of the cart item
        cart_item.quantity = quantity

        # Save the updated cart item
        cart_item.save()

    # Redirect the user back to the cart page
    return redirect('cart')
  # Assuming you have a URL pattern named 'cart' for the cart view

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from decimal import Decimal
from accounts.forms import *


@login_required(login_url='login')
def checkout(request):
    total = Decimal('0.00')
    quantity = 0
    discount_amount = Decimal('0.00')
    discount_percent = Decimal('0.00')
    grand_total = Decimal('0.00')

    # Retrieve cart items for the user
    cart_items = CartItem.objects.filter(user=request.user, is_active=True)
    for cart_item in cart_items:
        item_price = cart_item.final_price if hasattr(cart_item, 'final_price') else cart_item.product.price
        item_total_price = item_price * cart_item.quantity
        total += item_total_price
        quantity += cart_item.quantity

    # Calculate discount and grand total
    if total >= 50000:
        discount_percent = Decimal('0.10')
    elif total >= 20000:
        discount_percent = Decimal('0.05')
    elif total >= 5000:
        discount_percent = Decimal('0.03')
    discount_amount = total * discount_percent
    grand_total = total - discount_amount

    # Retrieve existing billing addresses
    billing_addresses = Address.objects.filter(user=request.user)
    delivery_addresses = Address.objects.filter(user=request.user)


    # Initialize the form
    billing_form = AddressForm(request.POST or None, prefix='billing_')
    delivery_form = AddressForm(request.POST or None, prefix='billing_')
    
    # Handle form submission
    if request.method == 'POST':
        if billing_form.is_valid():
            billing_address = billing_form.save(commit=False)
            billing_address.user = request.user  # Associate address with current user
            billing_address.save()
            messages.success(request, 'billing addresses address saved successfully.')
            return redirect('checkout')
        
        if delivery_addresses.is_valid():
            delivery_addresses = billing_form.save(commit=False)
            delivery_addresses.user = request.user  # Associate address with current user
            delivery_addresses.save()
            messages.success(request, 'delivery address saved successfully.')
            return redirect('checkout') 
        else:
            # Show error message
            messages.error(request, 'There was an error saving the delivery_addresses address.')
            
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'billing_addresses': billing_addresses,
        'delivery_addresses': delivery_addresses,
        'discount_amount': discount_amount,
        'grand_total': grand_total,
        'discount_percent': discount_percent * 100,
        'billing_form': billing_form,
        'delivery_form': delivery_form,

    }

    return render(request, 'store/checkout.html', context)

from django.http import JsonResponse


def set_default_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        
        if address_id:
            # Get the address object for the current user
            address = get_object_or_404(Address, id=address_id, user=request.user)
            
            # Set the address as default
            user_profile = request.user.profile
            user_profile.default_billing_address = address
            user_profile.save()
            
            # Return a JSON response indicating success
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid address ID'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required(login_url='login')
def delete_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        if address_id:
            # Get the address object for the current user
            address = get_object_or_404(Address, id=address_id, user=request.user)
            
            # Delete the address
            address.delete()
            
            # Return a JSON response indicating success
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid address ID'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

@login_required(login_url='login')
def get_addresses(request):
    addresses = Address.objects.filter(user=request.user)
    address_list = [{
        'id': address.id,
        'first_name': address.first_name,
        'last_name': address.last_name,
        'street_name': address.street_name,
        'city': address.city,
        'state': address.state,
        'zip_code': address.zip_code
    } for address in addresses]
    
    return JsonResponse({'success': True, 'addresses': address_list})
