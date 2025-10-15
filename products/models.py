# products/models.py
from django.db import models
from django.urls import reverse  # Used for get_absolute_url later for SEO
from django.utils.text import slugify  # For creating slugs from names
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(
        max_length=200,
        db_index=True,
        unique=True,
        help_text="Required and unique. Name of the category."
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text="Required. Unique URL-friendly identifier for the category."
    )
    description = models.TextField(
        blank=True,
        help_text="Optional. A description of the category."
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time the category was created."
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time the category was last updated."
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:category_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)  # New field to track views

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_min_variant_price(self):
        active_variants = self.variants.filter(is_active=True)
        if active_variants.exists():
            return active_variants.aggregate(models.Min('price'))['price__min']
        return None

    def get_max_variant_price(self):
        active_variants = self.variants.filter(is_active=True)
        if active_variants.exists():
            return active_variants.aggregate(models.Max('price'))['price__max']
        return None

    def get_total_stock(self):
        return self.variants.filter(is_active=True).aggregate(models.Sum('stock'))['stock__sum'] or 0

    def is_available(self):
        return self.variants.filter(is_active=True, stock__gt=0).exists()


class Variation(models.Model):
    name = models.CharField(max_length=50, unique=True, help_text="e.g., Size, Color, Material")

    class Meta:
        verbose_name = "Variation Type"
        verbose_name_plural = "Variation Types"

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    variations = models.ManyToManyField(Variation, through='ProductVariantAttribute')
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price for this specific variant")
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Stock quantity for this specific variant")
    sku = models.CharField(max_length=100, unique=True, blank=True, null=True, help_text="Stock Keeping Unit (optional)")
    image = models.ImageField(upload_to='products/variants/%Y/%m/%d/', blank=True, null=True, help_text="Optional image for this specific variant")
    is_active = models.BooleanField(default=True, help_text="Is this variant available for purchase?")

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"
        ordering = ['id']
        indexes = [
            models.Index(fields=['price']),
        ]

    def __str__(self):
        attributes = self.productvariantattribute_set.all()
        return f"{self.product.name} ({', '.join(f'{a.variation.name}: {a.attribute_value}' for a in attributes)})"

    def get_display_attributes(self):
        return ", ".join([
            f"{attr.variation.name}: {attr.attribute_value}"
            for attr in self.productvariantattribute_set.all().order_by('variation__name')
        ])

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.product.slug})


class ProductVariantAttribute(models.Model):
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    attribute_value = models.CharField(max_length=100)

    class Meta:
        unique_together = ('product_variant', 'variation')
        verbose_name = "Variant Attribute"
        verbose_name_plural = "Variant Attributes"

    def __str__(self):
        return f"{self.variation.name}: {self.attribute_value}"
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating from 1 to 5 stars"
    )
    comment = models.TextField(blank=True, help_text="Optional comment about the product")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'review'
        verbose_name_plural = 'reviews'

    def __str__(self):
        return f"{self.user.username}'s review for {self.product.name} ({self.rating} stars)"