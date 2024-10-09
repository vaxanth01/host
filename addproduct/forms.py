# forms.py

from django import forms
from store.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'slug',
            'description',
            'price',
            'MRP',
            
            'stock',
            'category',
            'discount_types',
            'weight',
            'abbreviation',
            'uom',
            'work',
            'SGST',
            'CGST',
            'IGST',
            'CESS',
            'special_cess',
            'HSN_NUMBER',
            'is_available',
            'image',
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'MRP': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'discount_types': forms.SelectMultiple(attrs={'class': 'form-input',}),
            'weight': forms.NumberInput(attrs={'class': 'form-control'}),
            'abbreviation': forms.TextInput(attrs={'class': 'form-control'}),
            'uom': forms.Select(attrs={'class': 'form-control'}),
            'work': forms.Select(attrs={'class': 'form-control'}),
            'SGST': forms.NumberInput(attrs={'class': 'form-control'}),
            'CGST': forms.NumberInput(attrs={'class': 'form-control'}),
            'IGST': forms.NumberInput(attrs={'class': 'form-control'}),
            'CESS': forms.NumberInput(attrs={'class': 'form-control'}),
            'special_cess': forms.NumberInput(attrs={'class': 'form-control'}),
            'HSN_NUMBER': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),

        }



# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__' 



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name', 'slug', 'icon', 'parent']
        widgets = {
            'category_name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-control'}),
        }

class ProductGalleryForm(forms.ModelForm):
    class Meta:
        model = ProductGalary
        fields = ['image']