from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from products.models import Product, ProductVariant
from .models import Cart, CartItem
from django.contrib import messages

def _get_or_create_cart(request):
    cart = None
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.save()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

@require_POST
def add_to_cart(request, product_id):
    # Get the product by product_id
    product = get_object_or_404(Product, id=product_id)

    # Pick the first variant of this product (customize this logic if needed)
    variant = product.variants.first()
    if not variant:
        messages.error(request, "Sorry, this product has no available variants to add.")
        return redirect('products:product_detail', product_id=product_id)

    quantity = int(request.POST.get('quantity', 1))
    cart = _get_or_create_cart(request)

    try:
        cart_item = CartItem.objects.get(cart=cart, product_variant=variant)
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f"Increased quantity of {variant.product.name} in your cart.")
    except CartItem.DoesNotExist:
        CartItem.objects.create(cart=cart, product_variant=variant, quantity=quantity, price=variant.price)
        messages.success(request, f"Added {variant.product.name} to your cart.")

    return redirect('cart:cart_detail')

@require_POST
def remove_from_cart(request, product_id):
    # Get the product by product_id
    product = get_object_or_404(Product, id=product_id)

    # Get the first variant (or handle if no variant exists)
    variant = product.variants.first()
    if not variant:
        messages.error(request, f"No variant found for product ID {product_id}.")
        return redirect('cart:cart_detail')

    cart = _get_or_create_cart(request)

    # Attempt to remove the cart item
    try:
        cart_item = CartItem.objects.get(cart=cart, product_variant=variant)
        product_name = cart_item.product_variant.product.name
        cart_item.delete()
        messages.info(request, f"Removed {product_name} from your cart.")
    except CartItem.DoesNotExist:
        messages.error(request, f"Item for product ID {product_id} not found in your cart.")

    return redirect('cart:cart_detail')

@require_POST
def update_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variant = product.variants.first()
    if not variant:
        messages.error(request, "Product variant not found.")
        return redirect('cart:cart_detail')

    new_quantity = int(request.POST.get('quantity', 1))
    if new_quantity <= 0:
        return remove_from_cart(request, product_id)

    cart = _get_or_create_cart(request)

    try:
        cart_item = CartItem.objects.get(cart=cart, product_variant=variant)
        cart_item.quantity = new_quantity
        cart_item.save()
        messages.success(request, f"Updated quantity of {variant.product.name} to {new_quantity}.")
    except CartItem.DoesNotExist:
        messages.error(request, "Product not found in your cart.")

    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = _get_or_create_cart(request)
    context = {
        'cart': cart,
        'site_name': 'Modern Fashion',
        'page_title': 'Your Shopping Cart',
    }
    return render(request, 'cart/cart_detail.html', context)