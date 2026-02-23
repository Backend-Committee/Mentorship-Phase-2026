from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    AddCommentView, AddLikeView, PollListView, PollCreateView, PollDetailView, PollVoteView, PollCommentView
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/comment/', AddCommentView.as_view(), name='add-comment'),
    path('post/<int:pk>/like/', AddLikeView.as_view(), name='add-like'),
    
    path('polls/', PollListView.as_view(), name='poll-list'),
    path('polls/new/', PollCreateView.as_view(), name='poll-create'),
    path('polls/<int:pk>/', PollDetailView.as_view(), name='poll-detail'),
    path('polls/<int:pk>/vote/', PollVoteView.as_view(), name='poll-vote'),
    path('polls/<int:pk>/comment/', PollCommentView.as_view(), name='poll-comment'),
]