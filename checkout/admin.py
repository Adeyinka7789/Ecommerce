
# checkout/admin.py
from django.contrib import admin
from .models import Order, OrderItem, Address

# Inline for OrderItems to be displayed directly within the Order admin page
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',) # Use a raw ID field for product selection if many products
    readonly_fields = ('product_name', 'product_price', 'quantity', 'get_total_price') # Make these read-only
    extra = 0 # Don't show extra empty forms by default

    def get_total_price(self, obj):
        return obj.get_total_price()
    get_total_price.short_description = 'Item Total'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'first_name', 'last_name', 'email', 'total_price', 'status',
        'created_at', 'updated_at',
    )
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('id', 'first_name', 'last_name', 'email', 'shipping_city', 'shipping_zip_code')
    readonly_fields = ('created_at', 'updated_at', 'total_price', 'transaction_id') # These are managed by code/payment gateway

    fieldsets = (
        ('Order Information', {
            'fields': ('user', 'status', 'total_price', 'transaction_id')
        }),
        ('Customer Details', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Shipping Address', {
            'fields': ('shipping_address_line1', 'shipping_address_line2',
                       'shipping_city', 'shipping_state', 'shipping_zip_code', 'shipping_country')
        }),
        ('Billing Address', {
            'fields': ('billing_address_line1', 'billing_address_line2',
                       'billing_city', 'billing_state', 'billing_zip_code', 'billing_country')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',) # Makes this section collapsible in admin
        }),
    )
    inlines = [OrderItemInline] # Include OrderItems directly in the Order admin page

admin.site.register(Address) # Register Address model separately if needed