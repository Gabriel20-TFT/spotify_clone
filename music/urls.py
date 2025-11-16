from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Pagini generale
    path('welcome/', views.welcome, name='welcome'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Artiști și albume
    path('artists/', views.artist_list, name='artists'),
    path('artist/<int:artist_id>/', views.artist_detail, name='artist_detail'),
    path('album/<int:album_id>/', views.album_detail, name='album_detail'),
    path('albums/', views.album_list, name='album_list'),

    # Melodii
    path('songs/', views.song_list, name='song_list'),
    path('song/<int:song_id>/', views.song_detail, name='song_detail'),
    path('upload/', views.upload_song, name='upload_song'),
    path('song/<int:song_id>/download/', views.download_song, name='download_song'),

    # Playlist-uri
    path('playlists/', views.playlist_list, name='playlist_list'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlist/<int:playlist_id>/add/<int:song_id>/', views.add_song_to_playlist, name='add_song_to_playlist'),
    path('playlist/<int:playlist_id>/remove/<int:song_id>/', views.remove_song_from_playlist, name='remove_song_from_playlist'),

    path('statistics/', views.statistics, name='statistics'),
    path('genres/', views.genre_list, name='genre_list'),
    path('genre/<int:genre_id>/', views.genre_detail, name='genre_detail'),
]




