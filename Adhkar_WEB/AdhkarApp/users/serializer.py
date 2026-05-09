from rest_framework import serializers
from .models import *
#for admin
class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model=Reward
        fields='__all__'
#for user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'email', 'total_points','is_staff']     
#for user
class UserRewardSerializer(serializers.ModelSerializer):
    reward_details = serializers.ReadOnlyField(source='reward.title')
    reward_image = serializers.ImageField(source='reward.image', read_only=True)
    reward_description = serializers.ReadOnlyField(source='reward.description')
    class Meta:
        model = UserReward
        fields = ['reward_details', 'reward_image', 'reward_description', 'unlocked_at']