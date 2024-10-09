from django.shortcuts import render, get_object_or_404, redirect
from store.models import Product, ReviewRating
from category.models import Category
from .forms import ReviewForms
from django.contrib import messages
from django.db.models import Q


from django.db.models import F
from django.db.models import F, Value, FloatField
from django.db.models.functions import Coalesce

def store(request):
    categories = Category.objects.filter(parent=None)
    products = Product.objects.filter(is_available=True)
    products_count = products.count()
    category_queries = request.GET.getlist('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    search_query = request.GET.get('q')

    if category_queries:
        selected_categories = Category.objects.filter(category_name__in=category_queries)
        products = products.filter(category__in=selected_categories)

    if min_price and max_price:
        try:
            min_price = int(min_price)
            max_price = int(max_price)
            products = products.filter(price__range=(min_price, max_price))
        except ValueError:
            pass

    if search_query:
        products = products.filter(
            Q(product_name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    # Annotate each product with available discounts if 'discount' field exists
    if 'discount' in [field.name for field in Product._meta.get_fields()]:
        products = products.annotate(
            available_discount=F('price') * F('discount') / 100
        )
    else:
        # Otherwise, annotate with a default value of 0
        products = products.annotate(
            available_discount=Value(0, output_field=FloatField())
        )

    context = {
        'categories': categories,
        'products': products,
        'products_count': products_count,
        'selected_categories': category_queries,
        'min_price': min_price,
        'max_price': max_price,
        'search_query': search_query
    }
    return render(request, 'store/store.html', context)


def submit_reviews(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForms(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you, your Review has been updated')
            return redirect(url)


        except ReviewRating.DoesNotExist:
            form = ReviewForms(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you, your Review has been submitted')
                return redirect(url)
            



from app.models import *
from accounts.forms import *





def edit_billing_address(request):
    billing_address_id = request.POST.get("billing_address_id")

    if request.method == "POST":
        try:
            billing_address = Address.objects.get(id=billing_address_id, user=request.user)
        except Address.DoesNotExist:
            messages.error(request, "Invalid billing address selected.")
            return redirect("address")

        billing_form = AddressForm(request.POST, instance=billing_address)

        if billing_form.is_valid():
            billing_form.save()
            messages.success(request, "Billing address updated successfully.")
            return redirect("address")
        else:
            messages.error(request, "Failed to update billing address. Please check the form for errors.")
    else:
        messages.error(request, "Invalid request method.")

    return redirect("address")




def edit_delivery_address(request):
    # Get the delivery address ID from the POST request
    delivery_address_id = request.POST.get("delivery_address_id")

    if request.method == "POST":
        # Get the delivery address for the user, raise 404 if it doesn't exist
        delivery_address = get_object_or_404(Address, id=delivery_address_id, user=request.user)

        # Create an instance of the form for the delivery address
        delivery_form = AddressForm(request.POST, instance=delivery_address)

        # Validate and save the form data
        if delivery_form.is_valid():
            delivery_form.save()
            messages.success(request, "Delivery address updated successfully.")
            return redirect("checkout")
        else:
            messages.error(request, "Failed to update delivery address. Please check the form for errors.")
    else:
        messages.error(request, "Invalid request method.")

    # Redirect back to checkout if the request method is not POST or there are issues with the request
    return redirect("checkout")



from django.shortcuts import render, redirect
from django.contrib import messages
from decimal import Decimal
from cart.models import CartItem
import stripe

def payment(request):
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

    # Initialize Stripe payment
    stripe.api_key = "your_stripe_secret_key"

    if request.method == 'POST':
        token = request.POST.get('stripeToken')
        try:
            charge = stripe.Charge.create(
                amount=int(grand_total * 100),  # Amount in cents
                currency='usd',
                description='Example charge',
                source=token,
            )
            # Payment successful, redirect to success page
            return render(request, 'payment_success.html')
        except stripe.error.CardError as e:
            # Payment failed, render payment failure page with error message
            return render(request, 'payment_failure.html', {'error': e})

    return render(request, 'store/payment.html', {'total': total, 'quantity': quantity, 'grand_total': grand_total})



def process_payment_view(request):
    if request.method == 'POST':
        payment_status = 'Success'
        return render(request, 'store/process_payment.html', {'payment_status': payment_status})
    else:
        return render(request, 'store/error.html')
