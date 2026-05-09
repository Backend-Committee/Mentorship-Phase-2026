from django.db.models.signals import post_save 
from users.models import Reward, UserReward
from django.dispatch import receiver
from .models import UserProgress

@receiver(post_save, sender=UserProgress)
def update_user_system(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        
        user.total_points += instance.points_earned
        user.save()
     
        all_eligible_rewards = Reward.objects.filter(points_threshold__lte=user.total_points)
        
        for reward in all_eligible_rewards:
            if not UserReward.objects.filter(user=user, reward=reward).exists():
                UserReward.objects.create(user=user, reward=reward)