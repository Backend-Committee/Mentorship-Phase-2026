from rest_framework import generics, permissions
from rest_framework.filters import SearchFilter
from .models import Reward, UserReward
from .serializer import RewardSerializer, UserSerializer, UserRewardSerializer

#user__>List of Rewards (view only) admin__>Create
class ListCreateReward(generics.ListCreateAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes = [permissions.IsAdminUser | permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['title', 'reward_type']
#admin__>only UpdateDeleteReward(put,delete),user__>get one reward
class GetUpdateDeleteReward(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reward.objects.all()
    serializer_class = RewardSerializer
    permission_classes = [permissions.IsAdminUser | permissions.IsAuthenticatedOrReadOnly]

class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    # بيرجع البروفايل الخاص بالسمتخدم فقط
    def get_object(self):
        return self.request.user

class UserRewardList(generics.ListAPIView):
    serializer_class = UserRewardSerializer
    permission_classes = [permissions.IsAuthenticated]
    #هيرجع الجوايز الخاصة بالمستخدم فقط
    def get_queryset(self):
        return UserReward.objects.filter(user=self.request.user)