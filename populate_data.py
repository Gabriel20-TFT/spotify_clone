# import os
# import django
# from django.utils import timezone
# from datetime import timedelta
#
# # Setează mediul Django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spotify_clone.settings")
# django.setup()
#
# from music.models import Artist, Album, Song, Playlist
# from django.contrib.auth.models import User
#
# def populate():
#     # Obține utilizatorul existent
#     user = User.objects.get(username="mefistofel")
#
#     # Creează artiști
#     artist1 = Artist.objects.create(name="The Beatles", bio="Legendary band from UK.")
#     artist2 = Artist.objects.create(name="Daft Punk", bio="Famous electronic duo.")
#     artist3 = Artist.objects.create(name="Imagine Dragons", bio="American pop rock band.")
#
#     # Creează albume
#     album1 = Album.objects.create(title="Abbey Road", artist=artist1, release_date="1969-09-26")
#     album2 = Album.objects.create(title="Discovery", artist=artist2, release_date="2001-03-13")
#     album3 = Album.objects.create(title="Night Visions", artist=artist3, release_date="2012-09-04")
#
#     # Creează melodii
#     song1 = Song.objects.create(title="Come Together", album=album1, duration=timedelta(seconds=259))
#     song2 = Song.objects.create(title="Something", album=album1, duration=timedelta(seconds=182))
#     song3 = Song.objects.create(title="One More Time", album=album2, duration=timedelta(seconds=320))
#     song4 = Song.objects.create(title="Radioactive", album=album3, duration=timedelta(seconds=186))
#     song5 = Song.objects.create(title="Demons", album=album3, duration=timedelta(seconds=177))
#
#     # Creează un playlist pentru utilizator
#     playlist = Playlist.objects.create(name="My Favorites", user=user)
#
#     # Adaugă melodii în playlist
#     playlist.songs.add(song1, song3, song4)
#
#     print("Populare completă!")
#     print(f"Playlist '{playlist.name}' conține melodiile:")
#     for song in playlist.songs.all():
#         print(f"- {song.title}")
#
# if __name__ == "__main__":
#     populate()
