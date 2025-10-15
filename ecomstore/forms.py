# ecomstore/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from checkout.models import Address

class CustomUserCreationForm(UserCreationForm):
    # No extra fields for now, just using the default username/password
    pass

class UserProfileEditForm(UserChangeForm):
    password = None # Exclude password field; users change password separately

    class Meta:
        model = get_user_model() # Get the currently active User model
        fields = ('username', 'email', 'first_name', 'last_name') # Fields you want to allow editing


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        # Exclude 'user' as it will be automatically set by the view
        # Exclude 'created_at' and 'updated_at' as they are auto-fields
        exclude = ('user', 'created_at', 'updated_at',)

        # Optionally, you can list the fields explicitly if you prefer:
        # fields = ('street_address', 'apartment_address', 'city', 'state', 'zip_code', 'country', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap form-control class to all fields for consistent styling
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            # Make all fields required by default except apartment_address, zip_code, phone_number
            if field_name not in ['apartment_address', 'zip_code', 'phone_number']:
                 field.required = True
