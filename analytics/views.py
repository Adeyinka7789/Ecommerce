# analytics/views.py
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from checkout.models import Order, OrderItem
from products.models import Product
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from datetime import timedelta
from django.utils import timezone

@staff_member_required
def analytics_dashboard(request):
    # Total Orders and Revenue
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total=Sum('total_price'))['total'] or 0

    # Orders in the Last 30 Days
    last_30_days = timezone.now() - timedelta(days=30)
    recent_orders = Order.objects.filter(created_at__gte=last_30_days)
    recent_orders_count = recent_orders.count()
    recent_revenue = recent_orders.aggregate(total=Sum('total_price'))['total'] or 0

    # Popular Products (Top 5 by quantity sold)
    popular_products = OrderItem.objects.values('product_name').annotate(
        total_quantity=Sum('quantity')
    ).order_by('-total_quantity')[:5]

    # User Activity
    total_users = User.objects.count()
    active_users = User.objects.filter(last_login__gte=last_30_days).count()

    # Data for Charts (e.g., Orders per Day in Last 30 Days)
    orders_per_day = Order.objects.filter(created_at__gte=last_30_days).extra(
        select={'day': "date(created_at)"}
    ).values('day').annotate(count=Count('id')).order_by('day')

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'recent_orders_count': recent_orders_count,
        'recent_revenue': recent_revenue,
        'popular_products': popular_products,
        'total_users': total_users,
        'active_users': active_users,
        'orders_per_day': list(orders_per_day),  # For chart rendering
    }
    return render(request, 'analytics/dashboard.html', context)