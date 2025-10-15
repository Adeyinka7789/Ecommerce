# checkout/views.py
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from decouple import config
from cart.models import Cart, CartItem
from products.models import Product
from .models import Order, OrderItem
from .forms import CheckoutForm

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

@csrf_exempt
def create_paystack_payment(request):
    if request.method == "POST":
        order_id = request.session.get('order_id')
        if not order_id:
            return JsonResponse({'error': 'No order found'}, status=400)

        order = get_object_or_404(Order, id=order_id)
        amount = int(order.total_price * 100)  # Convert to kobo (Paystack uses smallest currency unit)

        url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {config('PAYSTACK_SECRET_KEY')}",
            "Content-Type": "application/json",
        }
        data = {
            "email": order.email,
            "amount": amount,
            "callback_url": request.build_absolute_uri(reverse('checkout:checkout_success')),
            "metadata": {"order_id": str(order.id)},
        }

        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 200:
            payment_data = response.json()
            return JsonResponse({'authorization_url': payment_data['data']['authorization_url']})
        return JsonResponse({'error': 'Failed to initialize payment'}, status=500)

def checkout_page(request):
    cart = _get_or_create_cart(request)

    if not cart.items.exists():
        messages.warning(request, "Your cart is empty. Please add items before checking out.")
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                    email=form.cleaned_data['email'],
                    phone=form.cleaned_data['phone'],
                    shipping_address_line1=form.cleaned_data['shipping_address_line1'],
                    shipping_address_line2=form.cleaned_data['shipping_address_line2'],
                    shipping_city=form.cleaned_data['shipping_city'],
                    shipping_state=form.cleaned_data['shipping_state'],
                    shipping_zip_code=form.cleaned_data['shipping_zip_code'],
                    shipping_country=form.cleaned_data['shipping_country'],
                    billing_address_line1=form.cleaned_data['shipping_address_line1'] if form.cleaned_data.get('same_as_shipping') else form.cleaned_data['billing_address_line1'],
                    billing_address_line2=form.cleaned_data['shipping_address_line2'] if form.cleaned_data.get('same_as_shipping') else form.cleaned_data['billing_address_line2'],
                    billing_city=form.cleaned_data['shipping_city'] if form.cleaned_data.get('same_as_shipping') else form.cleaned_data['billing_city'],
                    billing_state=form.cleaned_data['shipping_state'] if form.cleaned_data.get('same_as_shipping') else form.cleaned_data['billing_state'],
                    billing_zip_code=form.cleaned_data['shipping_zip_code'] if form.cleaned_data.get('same_as_shipping') else form.cleaned_data['billing_zip_code'],
                    billing_country=form.cleaned_data['shipping_country'] if form.cleaned_data.get('same_as_shipping') else form.cleaned_data['billing_country'],
                    total_price=cart.get_total_price(),
                    status='pending',
                )

                for cart_item in cart.items.all():
                    OrderItem.objects.create(
                        order=order,
                        product=cart_item.product_variant.product,
                        product_name=cart_item.product_variant.product.name,
                        product_price=cart_item.price,
                        quantity=cart_item.quantity,
                    )

                # Store order_id in session to use in payment
                request.session['order_id'] = order.id

                # Clear the cart after creating the order (post-payment will be handled in success view)
                cart.items.all().delete()
                cart.delete()

                return JsonResponse({'success': True, 'order_id': order.id})

        else:
            messages.error(request, "Please correct the errors in the form.")
            return render(request, 'checkout/checkout_page.html', {
                'cart': cart,
                'form': form,
                'site_name': 'Excellent Fashion Wares',
                'page_title': 'Checkout',
                'PAYSTACK_PUBLIC_KEY': config('PAYSTACK_PUBLIC_KEY'),
            })
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data['first_name'] = request.user.first_name if hasattr(request.user, 'first_name') else ''
            initial_data['last_name'] = request.user.last_name if hasattr(request.user, 'last_name') else ''
            initial_data['email'] = request.user.email
        form = CheckoutForm(initial=initial_data)

    context = {
        'cart': cart,
        'form': form,
        'site_name': 'Excellent Fashion Wares',
        'page_title': 'Checkout',
        'PAYSTACK_PUBLIC_KEY': config('PAYSTACK_PUBLIC_KEY'),
    }
    return render(request, 'checkout/checkout_page.html', context)

def checkout_success(request):
    order_id = request.session.get('order_id')
    if not order_id:
        messages.error(request, "No order found. Please try again.")
        return redirect('checkout:checkout_page')

    order = get_object_or_404(Order, id=order_id)
    reference = request.GET.get('reference')
    if reference:
        url = f"https://api.paystack.co/transaction/verify/{reference}"
        headers = {
            "Authorization": f"Bearer {config('PAYSTACK_SECRET_KEY')}",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            payment_data = response.json()
            if payment_data['data']['status'] == 'success':
                order.status = 'submitted'
                order.transaction_id = reference
                order.save()
                messages.success(request, f"Payment successful for Order #{order.id}!")
                # Clear the session
                request.session.pop('order_id', None)
                return redirect(reverse('checkout:order_confirmation', args=[order.id]))
    messages.error(request, "Payment was not successful. Please try again.")
    return redirect('checkout:checkout_page')

def checkout_cancel(request):
    messages.error(request, "Payment was cancelled. Please try again.")
    return redirect('checkout:checkout_page')

def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'checkout/order_confirmation.html', {'order': order})