from django.urls import path
from live_interaction import views
urlpatterns = [
    path('', views.Room_Box, name="room_box"),
    path('start_room/', views.CreateRoomView.as_view(), name="start_room"),
    path('join_room/<int:room_id>/', views.JoinRoomUserView.as_view(), name="join_room")
]
