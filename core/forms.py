# ecomstore/core/forms.py
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Name',
            'class': 'form-control' # <--- MUST BE EXACTLY THIS
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your Email Address',
            'class': 'form-control' # <--- MUST BE EXACTLY THIS
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Subject',
            'class': 'form-control' # <--- MUST BE EXACTLY THIS
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Your Message',
            'rows': 5,
            'class': 'form-control' # <--- MUST BE EXACTLY THIS
        })
    )