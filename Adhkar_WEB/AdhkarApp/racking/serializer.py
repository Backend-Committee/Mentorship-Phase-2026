from rest_framework import serializers
from .models import *
class userprogress(serializers.ModelSerializer):
    adhkar_title = serializers.ReadOnlyField(source='adhkar.title') # لإظهار اسم الذكر
    class Meta:
        model=UserProgress
        fields = ['adhkar','adhkar_title','points_earned', 'completed_at'] 
        # الحقول دي السيرفر هو اللي بيملأها، المستخدم ملوش دعوة بيهاع نمنع الهاكر يدخل رقم كبير ويزود الاسكور بتاعه
        read_only_fields = ['points_earned', 'completed_at']
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['is_enabled', 'reminder_time']