from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Panel, Category


@receiver(post_save, sender=Panel)
def create_default_categories(sender, instance, created, **kwargs):
    """Create default system categories when a panel is created."""
    if not created:
        return

    default_categories = [
        ("Food & Dining", "#FF6B6B"),
        ("Transportation", "#4ECDC4"),
        ("Entertainment", "#45B7D1"),
        ("Utilities", "#FFA07A"),
        ("Shopping", "#98D8C8"),
        ("Healthcare", "#F7DC6F"),
        ("Housing", "#BB8FCE"),
        ("Education", "#85C1E2"),
        ("Insurance", "#F8B195"),
        ("Other", "#CCCCCC"),
    ]

    for name, color in default_categories:
        Category.objects.get_or_create(
            panel=instance,
            name=name,
            defaults={"color_hex": color, "is_default": True},
        )
