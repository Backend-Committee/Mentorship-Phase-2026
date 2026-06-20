from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Category(models.Model):
    """
    Represents a top-level product category (e.g. Electronics, Books).
    The `slug` is used to build anchor links (#electronics) and URL paths.
    The `image_url` points to an external/CDN image used in the category tile.
    The `color` is a CSS hex used as a soft background tint behind the image.
    The `order` field controls left-to-right display order.
    """
    name      = models.CharField(max_length=100)
    slug      = models.SlugField(max_length=100, unique=True)
    image_url = models.URLField(max_length=500, blank=True)
    color     = models.CharField(
        max_length=7,
        default='#E8F4FD',
        help_text='Hex color for the category tile background, e.g. #E8F4FD'
    )
    order     = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering  = ['order', 'name']
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    A single product. Each product belongs to exactly one Category.

    Pricing:
      - `price`     — current selling price
      - `old_price` — original/crossed-out price (optional); if set, a
                      discount percentage is computed dynamically in the view.

    Badges (boolean flags):
      - `is_best_seller` → orange "Best Seller" badge
      - `is_prime`       → dark "Prime" badge
      - `is_deal`        → red "Deal" badge

    `image_url` holds the full URL to the product photo (CDN / external host).
    `stock` allows the view to mark items as out-of-stock if needed later.
    """
    category          = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    title             = models.CharField(max_length=300)
    brand             = models.CharField(max_length=100)
    short_description = models.CharField(max_length=500, blank=True)
    price             = models.DecimalField(max_digits=10, decimal_places=2)
    old_price         = models.DecimalField(
        max_digits=10, decimal_places=2,
        null=True, blank=True
    )
    rating            = models.DecimalField(
        max_digits=3, decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=0
    )
    reviews_count     = models.PositiveIntegerField(default=0)
    image_url         = models.URLField(max_length=500)
    stock             = models.PositiveIntegerField(default=0)
    is_best_seller    = models.BooleanField(default=False)
    is_prime          = models.BooleanField(default=False)
    is_deal           = models.BooleanField(default=False)
    created_at        = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_best_seller', '-reviews_count']

    def __str__(self):
        return self.title

    @property
    def discount_percent(self):
        """
        Returns the integer discount percentage if old_price is set and
        higher than the current price; otherwise returns None.
        Example: price=64.99, old_price=99.99 → 35
        """
        if self.old_price and self.old_price > self.price:
            discount = ((self.old_price - self.price) / self.old_price) * 100
            return round(discount)
        return None

    @property
    def in_stock(self):
        return self.stock > 0


class Banner(models.Model):
    """
    Homepage hero banner. One active banner is shown at a time.
    `image_url` should be a wide landscape image (≥ 1500×500px recommended).
    `button_text` labels the CTA button (e.g. 'Shop Now').
    `button_link` is the URL/anchor the button points to.
    `is_active` lets you stage banners without deleting them.
    `order` controls priority when multiple banners are active.
    """
    title        = models.CharField(max_length=200)
    subtitle     = models.CharField(max_length=300, blank=True)
    eyebrow_text = models.CharField(
        max_length=100,
        blank=True,
        help_text='Small label above the headline, e.g. "Limited Time Offer"'
    )
    image_url    = models.URLField(max_length=500)
    button_text  = models.CharField(max_length=60, default='Shop Now')
    button_link  = models.CharField(max_length=200, default='#')
    is_active    = models.BooleanField(default=True)
    order        = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title
