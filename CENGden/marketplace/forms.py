from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Item, CustomUser, Phone, Computer, Vehicle, PrivateLesson  # Import the CustomUser model

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    phone_number = forms.CharField(max_length=15, required=True)  # Add phone_number field
    
    class Meta:
        model = CustomUser  # Use CustomUser model instead of User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')  # Include phone_number field

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose a different one.")
        return username

class UserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser  # Use CustomUser model instead of User
        fields = ['username', 'password']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'price', 'category', 'image_url', 'active']

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'onchange': 'showHideFields();'})


class ComputerForm(forms.ModelForm):
    class Meta:
        model = Computer
        fields = ['type', 'brand', 'model', 'year', 'processor', 'ram', 'storage', 'graphics_card', 'operating_system']

class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        fields = ['brand', 'model', 'year', 'operating_system', 'processor', 'ram', 'storage', 'camera_specifications', 'battery_capacity']

class VehicleForm(forms.ModelForm):
    year = forms.CharField(max_length=50, required=False)
    type = forms.CharField(max_length=50, required=False)
    brand = forms.CharField(max_length=50, required=False)
    model = forms.CharField(max_length=50, required=False)
    color = forms.CharField(max_length=50, required=False)
    engine_displacement = forms.CharField(max_length=50, required=False)
    fuel_type = forms.CharField(max_length=50, required=False)
    transmission_type = forms.CharField(max_length=50, required=False)
    mileage = forms.CharField(max_length=50, required=False)

    class Meta:
        model = Vehicle
        fields = ['type', 'brand', 'model', 'year', 'color', 'engine_displacement', 'fuel_type', 'transmission_type', 'mileage']

class PrivateLessonForm(forms.ModelForm):
    class Meta:
        model = PrivateLesson
        fields = ['tutor_name', 'lessons', 'location', 'duration']

class UserUpdateForm(forms.ModelForm):  # Modify UserUpdateForm to include phone_number field
    class Meta:
        model = CustomUser  # Use CustomUser model instead of User
        fields = ('username', 'email', 'phone_number')  # Include phone_number field

class VerificationForm(forms.Form):
    verification_code = forms.CharField(label='Verification Code', max_length=6)