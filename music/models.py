from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    main_genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='main_artists')
    genres = models.ManyToManyField(Genre, blank=True, related_name='artists')

    def clean(self):
        if self.main_genre and self.main_genre not in self.genres.all():
            raise ValidationError("Genul principal trebuie să fie inclus în lista de genuri.")
    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')  # ← ADAUGĂ
    release_date = models.DateField(null=True, blank=True)
    cover_image = models.ImageField(upload_to='album_covers/', null=True, blank=True)

    def __str__(self):
        return self.title


class Song(models.Model):
    title = models.CharField(max_length=100)
    artists = models.ManyToManyField(Artist, related_name='songs')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    audio_file = models.FileField(upload_to='songs/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    def clean(self):
        # Dacă melodia are album:
        if self.album:
            album_artist = self.album.artist

            # Artistul albumului TREBUIE să fie în lista artiștilor melodiei
            if album_artist not in self.artists.all():
                raise ValidationError(
                    f"Albumul '{self.album}' aparține artistului '{album_artist}', "
                    f"dar melodia nu are acest artist în lista ei."
                )

    def __str__(self):
        return self.title


class Playlist(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song, blank=True)

    def __str__(self):
        return self.name



