from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="اختر الفئة"
    )
    
    class Meta:
        model = Product
        fields = ['name', 'category', 'description', 'price', 'stock', 'condition', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم المنتج'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'وصف المنتج'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'السعر'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'الكمية المتوفرة'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'اسم المنتج',
            'category': 'الفئة',
            'description': 'الوصف',
            'price': 'السعر (دج)',
            'stock': 'الكمية المتوفرة',
            'condition': 'حالة المنتج',
            'image': 'صورة المنتج'
        }
