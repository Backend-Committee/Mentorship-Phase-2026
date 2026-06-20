"""
store/templatetags/store_filters.py
====================================
Custom template filters used in the homepage template.

Usage in template:
    {% load store_filters %}
    {{ product.rating|stars }}          → ★★★★½  (HTML string, mark_safe)
    {{ product.reviews_count|fmt_num }} → 12,340
    {{ product.price|currency }}        → $849.99
"""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='stars')
def stars(rating):
    """
    Converts a decimal rating (0.0–5.0) into a Unicode star string.

    Rules:
      - full star  (★) for each whole point
      - half star  (½) for a fractional part ≥ 0.25 and < 0.75
      - rounds to nearest half to keep it simple

    Examples:
      4.8  → ★★★★★   (rounds to 5)
      4.5  → ★★★★½
      4.2  → ★★★★☆   (rounds to 4)
      3.7  → ★★★★☆   (rounds to 4 — 3.5 rounds up)
      0.0  → ☆☆☆☆☆

    Returns an HTML <span> so CSS can color it orange via .stars class.
    """
    try:
        value = float(rating)
    except (TypeError, ValueError):
        value = 0.0

    value = max(0.0, min(5.0, value))

    # Round to nearest 0.5
    rounded = round(value * 2) / 2

    full  = int(rounded)          # number of full stars
    half  = 1 if (rounded % 1)   else 0   # 1 half star or 0
    empty = 5 - full - half       # remaining empty stars

    star_html = (
        '★' * full +
        '½' * half +
        '☆' * empty
    )
    return mark_safe(f'<span class="stars" aria-label="{value} out of 5 stars">{star_html}</span>')


@register.filter(name='fmt_num')
def fmt_num(value):
    """
    Formats an integer with comma thousands separators.
    Example: 12340 → '12,340'
    """
    try:
        return f'{int(value):,}'
    except (TypeError, ValueError):
        return value


@register.filter(name='currency')
def currency(value):
    """
    Formats a Decimal/float as a USD price string.
    Example: 849.99 → '$849.99'
    """
    try:
        return f'${float(value):.2f}'
    except (TypeError, ValueError):
        return value
