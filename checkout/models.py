
# checkout/models.py
from django.db import models
from django.contrib.auth.models import User # For AUTH_USER_MODEL
from django.conf import settings # For AUTH_USER_MODEL
from products.models import Product # Import Product model
from decimal import Decimal # For precise decimal calculations

class Order(models.Model):
    """
    Represents a customer's order.
    Stores customer information, total price, and order status.
    """
    # Link to Django's built-in User model (optional, for logged-in users)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Don't delete order if user is deleted
        null=True, blank=True,
        related_name='orders',
        help_text="User who placed the order (if logged in)."
    )

    # Customer Information (for both logged-in and anonymous users)
    first_name = models.CharField(max_length=50, help_text="Customer's first name.")
    last_name = models.CharField(max_length=50, help_text="Customer's last name.")
    email = models.EmailField(help_text="Customer's email address.")
    phone = models.CharField(max_length=20, blank=True, help_text="Customer's phone number (optional).")

    # Shipping Address
    shipping_address_line1 = models.CharField(max_length=255, help_text="Shipping address line 1.")
    shipping_address_line2 = models.CharField(max_length=255, blank=True, help_text="Shipping address line 2 (optional).")
    shipping_city = models.CharField(max_length=100, help_text="Shipping city.")
    shipping_state = models.CharField(max_length=100, help_text="Shipping state (e.g., OH for Ohio).")
    shipping_zip_code = models.CharField(max_length=20, help_text="Shipping zip code.")
    shipping_country = models.CharField(max_length=100, default='USA', help_text="Shipping country.") # Default to USA

    # Billing Address (can be same as shipping)
    billing_address_line1 = models.CharField(max_length=255, help_text="Billing address line 1.")
    billing_address_line2 = models.CharField(max_length=255, blank=True, help_text="Billing address line 2 (optional).")
    billing_city = models.CharField(max_length=100, help_text="Billing city.")
    billing_state = models.CharField(max_length=100, help_text="Billing state.")
    billing_zip_code = models.CharField(max_length=20, help_text="Billing zip code.")
    billing_country = models.CharField(max_length=100, default='USA', help_text="Billing country.")

    # Order Details
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text="Total price of the order at the time of submission."
    )

    # Order Status (as per your requirements)
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending Payment'),
        ('submitted', 'Submitted (Payment Approved)'),
        ('processed', 'Processed (Shipped)'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    status = models.CharField(
        max_length=20,
        choices=ORDER_STATUS_CHOICES,
        default='pending',
        help_text="Current status of the order."
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, help_text="Date and time the order was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="Date and time the order was last updated.")

    # Transaction ID from payment gateway (will be added later when integrating payment)
    transaction_id = models.CharField(max_length=255, blank=True, null=True,
                                      help_text="Transaction ID from the payment gateway.")

    class Meta:
        ordering = ('-created_at',) # Order by most recent orders first
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f"Order {self.id} by {self.first_name} {self.last_name}"

    def get_total_price(self):
        """Calculates the sum of all order items."""
        return sum(item.get_total_price() for item in self.items.all())


class OrderItem(models.Model):
    """
    Represents a single product item within an order.
    Stores the product details at the time of order to preserve historical data.
    """
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE, # If order is deleted, its items are deleted
        related_name='items',     # Allows order.items.all()
        help_text="The order this item belongs to."
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL, # Don't delete order item if product is deleted
        null=True, blank=True,     # Allow product to be null if original product is removed
        help_text="The product that was ordered."
    )
    # Store product details at time of order to prevent changes in Product model affecting old orders
    product_name = models.CharField(max_length=255, help_text="Name of the product at time of order.")
    product_price = models.DecimalField(
        max_digits=10, decimal_places=2,
        help_text="Price of the product at time of order."
    )
    quantity = models.PositiveIntegerField(
        default=1,
        help_text="Quantity of the product ordered."
    )

    class Meta:
        verbose_name = 'order item'
        verbose_name_plural = 'order items'
        ordering = ('product_name',)

    def __str__(self):
        return f"{self.quantity} x {self.product_name} in Order {self.order.id}"

    def get_total_price(self):
        """Calculates the total price for this order item (quantity * product_price)."""
        return self.quantity * self.product_price
    
class Address(models.Model):
    # Link to the user who owns this address
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')

    # Address details
    street_address = models.CharField(max_length=255)
    apartment_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100) # Or region/province
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, default='Nigeria') # You can set a default country
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Optional: Flags for default addresses
    # We can implement this later if needed, e.g., is_default_shipping = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Addresses" # Makes "Addresses" plural in admin
        ordering = ['-created_at'] # Order most recently added first

    def __str__(self):
        return f"{self.street_address}, {self.city}, {self.state}"
