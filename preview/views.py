# preview/views.py
from django.shortcuts import render
from products.models import Product, Category  # <--- Import Category model
from django.db.models import Q  # <--- Import Q for filtering if needed

# Create your views here.

def home(request):
    # Fetch products that are overall available (have at least one active, in-stock variant)
    products = Product.objects.filter(variants__is_active=True, variants__stock__gt=0).distinct()
    products = products.order_by('-created_at')[:8]  # Show 8 latest available products

    # Fetch all categories
    categories = Category.objects.all()  # <--- Fetch categories

    context = {
        'site_name': 'Excellent Fashion Wares',  # <--- Match template default
        'page_title': 'Homepage',
        'products': products,
        'categories': categories,  # <--- Pass categories to the template
    }
    return render(request, "index.html", context)

def about(request):
    context = {
        'site_name': 'Excellent Fashion Wares',  # <--- Match template default
        'page_title': 'About Us',
        'company_description': 'We are a leading e-commerce store specializing in awesome Fashion wares'
    }
    return render(request, "about.html", context)