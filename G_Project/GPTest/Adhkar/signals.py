from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, Reward, UserReward

@receiver(post_save, sender=UserProfile)
def check_rewards(sender, instance, **kwargs):
    # 1. بنجيب كل الجوائز اللي نقاطها أقل من أو تساوي نقاط المستخدم الحالية
    available_rewards = Reward.objects.filter(points_threshold__lte=instance.total_points)

    for reward in available_rewards:
        # 2. بنروح نتأكد: هل المستخدم ده أخد الجايزة دي قبل كدة؟
        # لو مأخدهاش (get_or_create) بنسجلها له فوراً
        UserReward.objects.get_or_create(
            user=instance.user,
            reward=reward
        )