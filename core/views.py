# ecomstore/core/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm # <--- NEW: Import the ContactForm
# ... existing imports ...

# ecomstore/core/views.py

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Construct the email body
            email_body = f"Name: {name}\n" \
                         f"Email: {email}\n" \
                         f"Subject: {subject}\n" \
                         f"Message:\n{message}"

            try:
                send_mail(
                    f"Contact Form Submission: {subject}", # Email subject
                    email_body,                             # Email message
                    settings.DEFAULT_FROM_EMAIL,            # From email (configured in settings)
                    [settings.CONTACT_EMAIL],               # To email(s) (configured in settings)
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully! We will get back to you soon.')
                return redirect('core:contact') # Redirect to clear the form
            except Exception as e:
                messages.error(request, f'There was an error sending your message. Please try again later. Error: {e}')
    else:
        form = ContactForm()

    context = {
        'form': form,
        'page_title': 'Contact Us',
        'site_name': 'Modern Fashion', # Adjust if your store name is different
    }
    return render(request, 'core/contact.html', context)

def privacy(request):
    return render(request, 'core/privacy.html', {'page_title': 'Privacy Policy'})
