# products/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Variation, ProductVariant, ProductVariantAttribute, Review
from django.db.models import Q, Sum, Avg
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.utils import timezone

def index(request):
    featured_products = Product.objects.filter(variants__is_active=True, variants__stock__gt=0).distinct().order_by('-created_at')[:4]
    popular_products = Product.objects.filter(variants__is_active=True, variants__stock__gt=0, view_count__gte=5).distinct().order_by('-view_count')[:4]
    categories = Category.objects.all()

    context = {
        'products': featured_products,
        'popular_products': popular_products,
        'categories': categories,
        'site_name': 'Modern Fashion',
    }
    return render(request, 'index.html', context)

def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(variants__is_active=True, variants__stock__gt=0).distinct().order_by('name')
    categories = Category.objects.all()

    category_slug_from_query = request.GET.get('category')
    if category_slug_from_query:
        category = get_object_or_404(Category, slug=category_slug_from_query)
        products = products.filter(category=category)
    elif category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'category': category,
        'products': products,
        'categories': categories,
        'site_name': 'Modern Fashion',
        'page_title': 'All Products' if not category else category.name,
        'selected_category_slug': category_slug_from_query or category_slug
    }
    return render(request, 'products/product_list.html', context)

@login_required
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product.view_count += 1
    product.save()

    variants = product.variants.filter(is_active=True).order_by('id')

    variation_options = {}
    product_variation_types = Variation.objects.filter(
        productvariantattribute__product_variant__product=product
    ).distinct()

    for var_type in product_variation_types:
        attribute_values = ProductVariantAttribute.objects.filter(
            product_variant__product=product,
            variation=var_type
        ).values_list('attribute_value', flat=True).distinct().order_by('attribute_value')
        variation_options[var_type.name] = list(attribute_values)

    default_variant = None
    if variants.exists():
        default_variant = variants.first()

    # Handle review submission
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()

        if not rating:
            return render(request, 'product_detail.html', {
                'product': product,
                'variants': variants,
                'variation_options': variation_options,
                'default_variant': default_variant,
                'error': 'Please provide a rating.',
            })

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValidationError("Rating must be between 1 and 5.")
        except (ValueError, ValidationError):
            return render(request, 'product_detail.html', {
                'product': product,
                'variants': variants,
                'variation_options': variation_options,
                'default_variant': default_variant,
                'error': 'Invalid rating value.',
            })

        if product.reviews.filter(user=request.user).exists():
            return render(request, 'product_detail.html', {
                'product': product,
                'variants': variants,
                'variation_options': variation_options,
                'default_variant': default_variant,
                'error': 'You have already submitted a review for this product.',
            })

        review = Review(product=product, user=request.user, rating=rating, comment=comment)
        review.save()

        return redirect('products:product_detail', slug=slug)

    # Fetch reviews for display
    reviews = product.reviews.all()
    avg_rating = product.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    review_count = product.reviews.count()

    # Fetch related products
    related_products = Product.objects.filter(
        category=product.category,
        variants__is_active=True,
        variants__stock__gt=0
    ).exclude(id=product.id).distinct().order_by('?')[:4]

    # Track recently viewed products in session
    if 'recently_viewed' not in request.session:
        request.session['recently_viewed'] = []
    recently_viewed = request.session['recently_viewed']
    if product.id not in recently_viewed:
        recently_viewed.insert(0, product.id)
        if len(recently_viewed) > 4:
            recently_viewed.pop()
        request.session['recently_viewed'] = recently_viewed

    # Fetch recently viewed products
    recently_viewed_products = Product.objects.filter(id__in=recently_viewed, variants__is_active=True, variants__stock__gt=0).distinct().order_by('-id')

    context = {
        'product': product,
        'variants': variants,
        'variation_options': variation_options,
        'default_variant': default_variant,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'review_count': review_count,
        'related_products': related_products,
        'recently_viewed_products': recently_viewed_products,
    }
    return render(request, 'product_detail.html', context)

def search_products(request):
    query = request.GET.get('q')
    products = Product.objects.filter(variants__is_active=True, variants__stock__gt=0).distinct()

    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).distinct()

    context = {
        'query': query,
        'products': products
    }
    return render(request, 'products/search_results.html', context)