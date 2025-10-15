# ecomstore/cart/admin.py
from django.contrib import admin
from .models import Cart, CartItem

# Admin for the Cart model
class CartItemInline(admin.TabularInline):
    model = CartItem
    # Make fields read-only that are set automatically or should not be changed directly
    fields = ('product_variant', 'quantity', 'price', 'get_product_name_display') # Add a custom display method
    readonly_fields = ('price', 'get_product_name_display') # Price is set on add
    extra = 0 # No empty forms by default

    def get_product_name_display(self, obj):
        # Custom method to display product name and variant attributes in the inline
        if obj.product_variant:
            return f"{obj.product_variant.product.name} ({obj.product_variant.display_attributes()})"
        return "N/A"
    get_product_name_display.short_description = "Product & Variant"


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key', 'created_at', 'updated_at', 'get_total_items', 'get_total_price')
    list_filter = ('created_at', 'updated_at', 'user',) # Filter by creation/update time and user
    search_fields = ('user__username', 'session_key',) # Search by username or session key
    inlines = [CartItemInline] # Show CartItems directly in the Cart admin page
    readonly_fields = ('created_at', 'updated_at', 'get_total_items', 'get_total_price') # These are calculated

    def get_total_items(self, obj):
        return obj.items.count()
    get_total_items.short_description = "Items in Cart"

    def get_total_price(self, obj):
        return f"${obj.get_total_price():.2f}"
    get_total_price.short_description = "Cart Total"


# Admin for the CartItem model (if you want to manage it separately)
# Note: It's often easier to manage CartItems via the CartInline above.
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    # CHANGED: 'product' to 'product_variant'
    # REMOVED: 'created_at', 'updated_at' from list_display, readonly_fields, list_filter
    list_display = ('id', 'cart', 'product_variant', 'quantity', 'price', 'get_product_name_display')
    list_filter = ('cart', 'product_variant__product__category',) # Filter by cart and product category
    search_fields = ('cart__user__username', 'cart__session_key', 'product_variant__product__name')
    # CHANGED: 'product' to 'product_variant'
    readonly_fields = ('price',) # Price is set automatically when item is added to cart

    def get_product_name_display(self, obj):
        # Custom method to display product name and variant attributes
        if obj.product_variant:
            return f"{obj.product_variant.product.name} ({obj.product_variant.display_attributes()})"
        return "N/A"
    get_product_name_display.short_description = "Product & Variant"