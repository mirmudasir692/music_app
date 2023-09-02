from django.urls import path
from music import views

urlpatterns = [
    path('', views.Music_home, name='home'),
    path('listen_music/<int:id>/', views.listen_music, name="listen_music"),
    path('artist_songs/<int:id>/', views.songs_of_artist, name='artist_songs'),
    path('watch_later/', views.Watch_laterview.as_view(), name="watch_later"),
    path('add_watch_later/<int:id>/',
         views.Watch_laterview.as_view(), name="add_watch_later"),
    path('playlist_songs/<int:id>/',
         views.PlaylistSongsView.as_view(), name="playlist_songs"),
    path('user_history/', views.History_of_user.as_view(), name="user_history"),
    path('remove_history', views.delete_history, name='remove_history'),
    path('search_music/',views.SearchMusicView.as_view(),name="search_music"),
    path('remove_later',views.Watch_laterview.as_view(),name='remove_later')
]
