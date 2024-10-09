from django import forms
from app.models import *
from . models import *
from cart.models import *

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={   
        'class': 'form-control'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter First Name',
        'class': 'form-control',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Last Name',
        'class': 'form-control'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Enter Email Address',
        'class': 'form-control',
    }))
    phone_number = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter Phone Number',
        'class': 'form-control'
    }))
  
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
       
   

from django import forms
from app.models import *

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['last_name', 'first_name', 'email', 'alter_number', 'address_line', 'kilometer', 'street_name', 'profile_pic', 'city', 'phone_number', 'state', 'country', 'zip_code']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'alter_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),  # Corrected from forms.EmailField()
            'address_line': forms.TextInput(attrs={'class': 'form-control'}),  # Changed from 'address line'
            'street_name': forms.TextInput(attrs={'class': 'form-control'}),
            'kilometer': forms.NumberInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.NumberInput(attrs={'class': 'form-control'}),  # Changed from forms.TextInput()
        }



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'address_line',
            'street_name',
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'alter_number',
            'kilometer',
            'city',
            'state',
            'country',
            'zip_code',
        ]
        widgets = {
            'street_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'alter_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address_line': forms.TextInput(attrs={'class': 'form-control'}),
            'kilometer': forms.NumberInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.NumberInput(attrs={'class': 'form-control'}),
        }


from django import forms
from django.contrib.auth.forms import PasswordChangeForm as DjangoPasswordChangeForm

class PasswordChangeForm(DjangoPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Old Password'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'New Password'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm New Password'})
