# wishlist/models.py
from django.db import models
from django.contrib.auth import get_user_model # Best way to get the User model
from products.models import Product # Import your Product model
# REMOVE THIS LINE: from django.core.validators import UniqueTogetherValidator # For unique constraint

class Wishlist(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='wishlist_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # NEW WAY: Use UniqueConstraint within the 'constraints' list
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_user_product_in_wishlist')
        ]
        verbose_name = 'Wishlist Item'
        verbose_name_plural = 'Wishlist Items'
        ordering = ['-added_at'] # Order by most recently added

    def __str__(self):
        return f"{self.user.username}'s wishlist: {self.product.name}"