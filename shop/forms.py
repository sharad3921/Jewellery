from django import forms
from django.contrib.auth.models import User
from .models import Product, Order, ContactMessage

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Choose Username'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
            
        username = cleaned_data.get("username")
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already taken.")
            
        email = cleaned_data.get("email")
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")
            
        return cleaned_data

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'image', 'description', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Product Name', 'class': 'form-input'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'price': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'form-input', 'step': '0.01'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'placeholder': 'Product Description...', 'class': 'form-input', 'rows': 4}),
            'stock': forms.NumberInput(attrs={'placeholder': '10', 'class': 'form-input'}),
        }

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'postal_code', 'country']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First', 'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Gmail@example.com', 'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Number', 'class': 'form-input'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-input'}),
            'city': forms.TextInput(attrs={'placeholder': 'City', 'class': 'form-input'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Pin', 'class': 'form-input'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country', 'class': 'form-input'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'form-input'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject', 'class': 'form-input'}),
            'message': forms.Textarea(attrs={'placeholder': 'How can we help you?', 'class': 'form-input', 'rows': 5}),
        }
