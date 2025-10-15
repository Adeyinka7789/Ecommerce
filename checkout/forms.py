# checkout/forms.py

from django import forms

class CheckoutForm(forms.Form):
    """
    Form for collecting customer shipping and billing information during checkout.
    """
    # Customer Details
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    phone = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'Phone (Optional)'}))

    # Shipping Address
    shipping_address_line1 = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Address Line 1'}))
    shipping_address_line2 = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Address Line 2 (Optional)'}))
    shipping_city = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'City'}))
    shipping_state = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'State / Province'}))
    shipping_zip_code = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder': 'Zip / Postal Code'}))
    shipping_country = forms.CharField(max_length=100, initial='USA', widget=forms.TextInput(attrs={'placeholder': 'Country'}))

    # Billing Address (checkbox for "Same as Shipping")
    same_as_shipping = forms.BooleanField(required=False, initial=True,
                                          widget=forms.CheckboxInput(attrs={'id': 'same_as_shipping_checkbox'}))

    # Billing Address Fields (will be conditionally shown/hidden by JavaScript)
    billing_address_line1 = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Billing Address Line 1'}))
    billing_address_line2 = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Billing Address Line 2 (Optional)'}))
    billing_city = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Billing City'}))
    billing_state = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Billing State / Province'}))
    billing_zip_code = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder': 'Billing Zip / Postal Code'}))
    billing_country = forms.CharField(max_length=100, required=False, initial='USA', widget=forms.TextInput(attrs={'placeholder': 'Billing Country'}))

    # Payment Information (Placeholders for now, will integrate with payment gateway later)
    # NEVER collect raw credit card details directly in your Django form.
    # This will be handled by a secure payment gateway's JavaScript SDK (e.g., Stripe.js).
    # For now, we'll just have a placeholder message.
    # payment_method = forms.CharField(max_length=50, widget=forms.HiddenInput(), initial='credit_card')
    # token = forms.CharField(max_length=255, widget=forms.HiddenInput()) # Placeholder for payment token

    def clean(self):
        cleaned_data = super().clean()
        # If "Same as Shipping" is not checked, ensure billing address fields are provided
        if not cleaned_data.get('same_as_shipping'):
            required_billing_fields = [
                'billing_address_line1', 'billing_city', 'billing_state',
                'billing_zip_code', 'billing_country'
            ]
            for field_name in required_billing_fields:
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, "This field is required for billing address.")
        return cleaned_data