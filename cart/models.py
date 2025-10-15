# ecomstore/cart/models.py
from django.db import models
from django.conf import settings
from products.models import ProductVariant # <-- NEW IMPORT: ProductVariant

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart of {self.user.username}"
        return f"Anonymous Cart {self.session_key or 'N/A'}"

    def get_total_price(self):
        # Calculate total price of all items in the cart
        return sum(item.get_total() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    # CHANGE: Link to ProductVariant instead of Product
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    # Store price at time of add, in case variant price changes later
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        # Ensures that a specific variant can only appear once in a cart
        unique_together = ('cart', 'product_variant')

    def __str__(self):
        # Display product name and its attributes for clarity
        return f"{self.quantity} x {self.product_variant.product.name} ({self.product_variant.display_attributes()})"

    def get_total(self):
        return self.quantity * self.price