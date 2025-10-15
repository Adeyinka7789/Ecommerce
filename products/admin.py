# products/admin.py
from django.contrib import admin
# Make sure all new and old models are imported here
from .models import Category, Product, Variation, ProductVariant, ProductVariantAttribute

# 1. Inline for ProductVariantAttribute:
#    Allows you to add specific attributes (e.g., Size: Large, Color: Red)
#    when creating/editing a ProductVariant.
class ProductVariantAttributeInline(admin.TabularInline):
    model = ProductVariantAttribute
    extra = 1 # Number of empty forms to display initially
    fields = ('variation', 'attribute_value',) # Fields to show in the inline
    # You might want to pre-populate 'variation' choices to only relevant ones
    # but for simplicity, we'll leave it open for now.

# 2. Inline for ProductVariant:
#    Allows you to add/edit different variants (e.g., Red-Large T-shirt)
#    directly from the Product admin page.
class ProductVariantInline(admin.StackedInline): # StackedInline gives a more vertical layout for variant fields
    model = ProductVariant
    extra = 1 # Number of empty variant forms to display initially
    show_change_link = True # Allows clicking on a variant to edit it directly
    # Link the ProductVariantAttributeInline here so you can define attributes for each variant
    inlines = [ProductVariantAttributeInline]
    fieldsets = (
        (None, {
            'fields': ('price', 'stock', 'sku', 'image', 'is_active')
        }),
    )

# 3. Product Admin - Updated for variations
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'slug',
        'category',
        'display_price_range',   # NEW: Custom method to show price range from variants
        'display_total_stock',   # NEW: Custom method to show total stock from variants
        'is_available_status',   # NEW: Custom method to show overall product availability
        'created_at',            # CORRECTED: Uses 'created_at' from the Product model
        'updated_at',            # CORRECTED: Uses 'updated_at' from the Product model
    ]
    list_filter = [
        'category',              # CORRECTED: Filter by 'category' (ForeignKey field)
        'created_at',            # CORRECTED: Filter by creation date
        'updated_at',            # CORRECTED: Filter by update date
        # You can also filter by variant properties, e.g.:
        # 'variants__is_active',   # Filter by whether any variant is active
        # 'variants__stock',       # Filter by stock (e.g., products with variants where stock is > 0)
    ]
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    # Removed filter_horizontal = ('categories',) - this was incorrect for a ForeignKey
    # Removed other old list_display/list_filter fields that no longer exist on Product

    # Crucially, add the ProductVariantInline to the ProductAdmin
    inlines = [ProductVariantInline]

    # --- Custom methods for list_display to show variant-derived info ---

    @admin.display(description='Price Range')
    def display_price_range(self, obj):
        """Displays the min-max price range of active variants, or a single price if only one."""
        min_price = obj.get_min_variant_price()
        max_price = obj.get_max_variant_price()

        if min_price is None:
            return "N/A" # No active variants with a price
        if min_price == max_price:
            return f"${min_price:.2f}"
        return f"${min_price:.2f} - ${max_price:.2f}"

    @admin.display(description='Total Stock')
    def display_total_stock(self, obj):
        """Displays the sum of stock from all active variants."""
        total_stock = obj.get_total_stock()
        return total_stock if total_stock is not None else 0

    @admin.display(boolean=True, description='Overall Available?')
    def is_available_status(self, obj):
        """Checks if the product has at least one active variant with stock > 0."""
        return obj.is_available() # This calls the method we added to the Product model


# 4. Register the new Variation model (e.g., Size, Color)
@admin.register(Category) # Keep your Category admin registration
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_filter = ('created_at', 'updated_at')


@admin.register(Variation) # Register the new Variation model
class VariationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Note: ProductVariant and ProductVariantAttribute are typically not registered
# directly in the admin because they are managed via Inlines from the Product model.
# If you wanted to manage them separately, you would add @admin.register() for them
# and define their respective Admin classes.