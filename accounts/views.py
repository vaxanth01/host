from django.shortcuts import render, redirect,get_object_or_404
from .forms import *
from app.models import Account, UserProfile
from django.http import JsonResponse

from orders.models import Order, OrderProduct
from cart.models import Cart, CartItem
from cart.views import _cart_id
import requests
import base64
import binascii
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import *
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
"""verification email"""
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            
            email = form.cleaned_data['email']
            username = email.split('@')[0]
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.phone_number = phone_number
            user.is_active = True
            user.save()

            #creating a user profile

            profile = UserProfile()
            profile.user_id = user.id
            profile.profile_pic = 'default/default-user.png'
            profile.save()

            return redirect('login')
    else:
        form = RegistrationForm()        
    
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html',context)



def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)

                    for item in cart_item:
                        item.user = user
                        item.save()


            except:
                pass    
            auth.login(request, user)
            messages.success(request, 'you are now loged in')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
                
            except:
                return redirect('home')
                  
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')     
    return render(request, 'accounts/login.html')



@login_required(login_url= login)
def logout(request):
    auth.logout(request)
    
    return redirect('login')



def activate(request, uidb64,token):
     try:
         uid = urlsafe_base64_decode(uidb64).decode()
         user = Account._default_manager.get(pk=uid)
     except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
         user = None
     if user is not None and default_token_generator.check_token(user, token):
         user.is_active = True
         user.save()
         messages.success(request, 'congratulations your account is actived')
         return redirect('login')
     else:
         messages.error(request,'invalid activation link')
         return redirect('register')   
          
@login_required(login_url='login')
def dashbord(request):
    orders = Order.objects.order_by('created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    context ={
        'orders':orders,
        'orders_count': orders_count
    }
    return render(request, 'accounts/dashbord.html', context)





def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = Account.objects.get(email=email)
        except Account.DoesNotExist:
            user = None
        
        if user:
            current_site = get_current_site(request)
            mail_subject = "Reset Your Password"
            message = render_to_string('accounts/reset_password.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'If an account exists with this email, a password reset link has been sent.')
            return redirect('login')
        else:
            messages.error(request, 'No account found with this email address.')
            return redirect('forgot-password')

    return render(request, 'accounts/forgotpassword.html')

from django.utils.encoding import force_bytes, force_str  # Update the import statement

def reset_password_validate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))  # Update force_text to force_str
        user = Account.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password.')
        return redirect('reset-password')
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('login')


def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        uid = request.session.get('uid')

        if password == confirm_password and uid:
            try:
                user = Account.objects.get(pk=uid)
                user.set_password(password)
                user.save()
                del request.session['uid']  # Remove UID from session
                messages.success(request, 'Your password has been successfully reset. You can now log in with your new password.')
                return redirect('login')
            except Account.DoesNotExist:
                pass

        messages.error(request, 'There was an error resetting your password. Please try again.')
        return redirect('reset-password')
    else:
        return render(request, 'accounts/reset_password.html')

        


def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('created_at')
    context = {
        'orders': orders
    }
    return render(request, 'accounts/my_orders.html', context)



def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('edit_profile')
    else:
       user_form =  UserProfileForm(instance=request.user)
       profile_form = UserProfileForm(instance=userprofile)
    
    context ={
        'user_form': user_form,
        'profile_form':profile_form,
        'userprofile':userprofile
    }
    return render(request, 'accounts/edit_profile.html',context)




def add_address(request):
    # This view function handles the submission of the modal form.
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            # The form is valid, so we can save the address data.
            # Attach the user to the form
            new_address = form.save(commit=False)
            new_address.user = request.user
            new_address.save()
            
            # Return a JSON response to indicate success.
            return JsonResponse({'success': True, 'message': 'Address added successfully.'})
        else:
            # If the form is invalid, return the errors.
            return JsonResponse({'success': False, 'errors': form.errors})

    # If the request method is GET, you can return a 405 Method Not Allowed error.
    return JsonResponse({'success': False, 'message': 'Method not allowed.'}, status=405)

@login_required(login_url='login')
def order_detail(request, order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail':order_detail,
        'order' :order,
        'subtotal':subtotal,
    }
    return render(request, 'accounts/order_detail.html',context)

from decimal import Decimal

def address(request):
   

    # Retrieve existing billing addresses
    billing_addresses = Address.objects.filter(user=request.user)


    # Initialize the form
    billing_form = AddressForm(request.POST or None, prefix='billing_')
    
    # Handle form submission
    if request.method == 'POST':
        if billing_form.is_valid():
            billing_address = billing_form.save(commit=False)
            billing_address.user = request.user  # Associate address with current user
            billing_address.save()
            messages.success(request, 'billing addresses address saved successfully.')
            return redirect('address')
        
       
            
    context = {
      
        'billing_addresses': billing_addresses,
        'billing_form': billing_form,

    }
    return render(request, 'accounts/address.html',context)



from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Updating the user's session to avoid logging out after password change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')  # Redirect to the same page after successful password change
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/changepassword.html', {'form': form})




from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST


def get_addresses(request):
    addresses = Address.objects.all()
    serialized_addresses = [{'id': address.id, 'street_name': address.street_name, 'city': address.city, 'state': address.state, 'zip_code': address.zip_code, 'is_default': address.is_default} for address in addresses]
    return JsonResponse({'success': True, 'addresses': serialized_addresses})

@require_POST
def set_default_address(request):
    address_id = request.POST.get('address_id')
    address = get_object_or_404(Address, id=address_id)
    Address.objects.exclude(id=address.id).update(is_default=False)  # Reset all other addresses to non-default
    address.is_default = True
    address.save()
    return JsonResponse({'success': True})

@require_POST
def delete_address(request):
    address_id = request.POST.get('address_id')
    address = get_object_or_404(Address, id=address_id)
    address.delete()
    return JsonResponse({'success': True})


@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user  # Associate address with the current user
            address.save()
            return JsonResponse({'success': True})
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': errors})
