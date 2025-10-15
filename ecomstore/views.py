# ecomstore/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import login # Import the login function
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, UserProfileEditForm, AddressForm # Import the form we just created
from checkout.models import Order, Address
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home') # Redirect to home page after successful signup
    template_name = 'registration/signup.html' # Template to render

    def form_valid(self, form):
        response = super().form_valid(form)
        # Log the user in immediately after successful registration
        login(self.request, self.object)
        return response
    

@login_required # This decorator ensures only logged-in users can access this view
def profile_view(request):
    # The user object is available via request.user thanks to the login_required decorator
    return render(request, 'user_profile/profile.html', {'user': request.user})

@login_required # Only logged-in users can see their order history
def order_history_view(request):
    # Fetch all orders for the currently logged-in user
    # We also use select_related('user') and prefetch_related('items__product') for efficiency
    # This will fetch related user data and all order items (and their products) in fewer database queries
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'orders': orders
    }
    return render(request, 'user_profile/order_history.html', context)

@login_required # Only logged-in users can see their order details
def order_detail_view(request, order_id):
    # Get the specific order, ensuring it belongs to the current user
    # get_object_or_404 will raise a 404 error if the order doesn't exist or doesn't belong to the user
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # We can directly access order.items.all() because of related_name='items' in OrderItem
    # If you want to optimize for many order items, you could prefetch:
    # order = get_object_or_404(Order.objects.prefetch_related('items__product'), id=order_id, user=request.user)
    context = {
        'order': order
    }
    return render(request, 'user_profile/order_detail.html', context)

@login_required # Only logged-in users can edit their profile
def profile_edit_view(request):
    if request.method == 'POST':
        form = UserProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            # You might want to add a success message here
            # messages.success(request, 'Your profile was updated successfully!')
            return redirect('profile') # Redirect back to the profile page
    else:
        form = UserProfileEditForm(instance=request.user) # Populate form with current user data

    context = {
        'form': form
    }
    return render(request, 'user_profile/profile_edit.html', context) # We'll create this template next

@login_required
def address_list_view(request):
    # Fetch all addresses belonging to the current user
    addresses = Address.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'addresses': addresses
    }
    return render(request, 'user_profile/address_list.html', context) # We'll create this template next

@login_required
def address_edit_view(request, address_id=None):
    # If address_id is provided, we are editing an existing address
    if address_id:
        # Ensure the address exists and belongs to the current user
        address = get_object_or_404(Address, id=address_id, user=request.user)
    else:
        # If no address_id, we are adding a new address
        address = None

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            new_address = form.save(commit=False) # Don't save to DB yet
            new_address.user = request.user # Assign the logged-in user
            new_address.save() # Now save
            # Optionally add a success message
            # messages.success(request, "Address saved successfully!")
            return redirect('address_list') # Redirect to the address list
    else:
        form = AddressForm(instance=address) # Pre-fill form if editing, or empty for new

    context = {
        'form': form,
        'address_id': address_id # Pass this to know if we're editing or adding
    }
    return render(request, 'user_profile/address_edit.html', context) # We'll create this template next

@login_required
@require_POST # <--- This decorator ensures the view only accepts POST requests
def address_delete_view(request, address_id):
    # Ensure the address exists and belongs to the current user before deleting
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    # Optionally add a success message
    # messages.success(request, "Address deleted successfully!")
    return redirect('address_list') # Redirect back to the address list

