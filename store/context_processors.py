"""
Context processor — ცვლადს ავტომატურად ხელმისაწვდომს ხდის ყველა template-ში,
რომ ცალკე ყოველ view-ში აღარ დაგვჭირდეს გადაცემა.
"""
from .models import Product


def latest_products(request):
    return {
        'latest_products': Product.objects.order_by('-created_at')[:5]
    }
