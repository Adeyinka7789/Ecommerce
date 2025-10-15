# wishlist/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST # For secure deletion/addition
# from django.contrib import messages # Uncomment if you want to use Django messages framework

from products.models import Product # Import the Product model
from .models import Wishlist # Import your Wishlist model

@login_required
def wishlist_view(request):
    # Get all wishlist items for the current logged-in user
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    context = {
        'wishlist_items': wishlist_items
    }
    return render(request, 'wishlist/wishlist.html', context) # We'll create this template next

@login_required
@require_POST
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    wishlist_item, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if created:
        # messages.success(request, f"{product.name} has been added to your wishlist.")
        pass
    else:
        # messages.info(request, f"{product.name} is already in your wishlist.")
        pass

    # FIX IS HERE: Redirect using product.slug instead of product_id
    return redirect('products:product_detail', slug=product.slug) # <--- CHANGED THIS LINE
    # Alternatively, to redirect to the page they came from:
    # return redirect(request.META.get('HTTP_REFERER', 'products:product_list'))


@login_required
@require_POST
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    wishlist_item = get_object_or_404(Wishlist, user=request.user, product=product)
    wishlist_item.delete()

    # messages.success(request, f"{product.name} has been removed from your wishlist.")
    return redirect('wishlist:wishlist_view')
