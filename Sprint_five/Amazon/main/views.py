from django.shortcuts import render
from .models import Category, Product, Banner
from cart.models import CartItem
import os

def ready(self):
    if os.environ.get('RUN_MAIN') == 'true':
        my_function()

def my_function():
    cart_items = CartItem.objects.all()
    for item in cart_items:
        item.delete()
        item.save()
    pass
def home(request):
    """
    Homepage view. Collects all data the template needs and passes it
    as a single context dictionary. The template never queries the DB
    directly — all logic lives here.

    Context variables:
    ------------------
    banner              — The highest-priority active Banner (or None)
    categories          — All categories, ordered by `order` field
    categories_with_products
                        — List of dicts: {'category': <Category>,
                                          'products':  <QuerySet of up to 10>}
                          Only categories that actually have products are included.
    deal_products       — Up to 4 products where is_deal=True (for the flash-deals panel)
    featured_products   — Up to 10 products total (best sellers + high-rated, mixed)
    """

    # ── Hero Banner ────────────────────────────────────────────────
    # Grab the first active banner. The template handles the None case
    # gracefully by showing a CSS-only gradient fallback slide.
    banner = Banner.objects.filter(is_active=True).first()

    # ── All Categories (used in sub-nav, search dropdown, tiles) ──
    categories = Category.objects.all()   # already ordered by Meta

    # ── Per-category product blocks ────────────────────────────────
    # We build a list of (category, products) pairs so the template
    # can iterate with a single {% for %} instead of one block per category.
    # We annotate each category's slug directly — the template uses it
    # for the section id and anchor links.
    categories_with_products = []
    for cat in categories:
        products = (
            cat.products
               .order_by('-is_best_seller', '-reviews_count')[:10]
        )
        if products.exists():
            categories_with_products.append({
                'category': cat,
                'products': products,
            })

    # ── Flash Deals panel (4 cards in the dark banner) ────────────
    deal_products = (
        Product.objects
               .filter(is_deal=True)
               .order_by('-reviews_count')[:4]
    )

    # ── Featured / Best Sellers row ────────────────────────────────
    # Shows the top 10 best-selling products across ALL categories.
    featured_products = (
        Product.objects
               .filter(is_best_seller=True)
               .order_by('-reviews_count')[:10]
    )

    context = {
        'banner':                    banner,
        'categories':                categories,
        'categories_with_products':  categories_with_products,
        'deal_products':             deal_products,
        'featured_products':         featured_products,
    }
    return render(request, 'home.html', context)


def search(request):
    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    results = Product.objects.all()

    if query:
        results = results.filter(title__icontains=query)

    if category:
        results = results.filter(category__slug=category)
    results_count = results.count()

    
    context = {
    'query': query,
    'results': results,
    'results_count': results_count,
    'categories': Category.objects.all(),
    'selected_category': category,
}

    return render(request, 'search.html', context)