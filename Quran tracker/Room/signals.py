from django.db.models.signals import post_delete
from django.dispatch import receiver
from User.models import UserRoom
from .models import Room


@receiver(post_delete, sender=UserRoom)
def handle_admin_delete(sender , instance, **kwargs):
    members = UserRoom.objects.filter(room=instance.room)
    if not members.exists():
        instance.room.delete()
        return

    if instance.room.admin == instance.user:
        new_admin = members.first().user
        instance.room.admin = new_admin
        instance.room.save()