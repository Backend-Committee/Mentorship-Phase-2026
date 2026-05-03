from django.urls import path

from Room.views import RoomCreationView, RoomListView, RoomDetailView, EditRoomSettingsView

urlpatterns = [
    path('create_room/', RoomCreationView.as_view(), name='room-list-create'),
    path('', RoomListView.as_view(), name='room-list'),
    path('<int:pk>/', RoomDetailView.as_view(), name='room-detail'),
    path('<int:room_id>/settings/', EditRoomSettingsView.as_view(), name='room-settings')
]