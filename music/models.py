from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Artist(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    genres = models.ManyToManyField(Genre, blank=True, related_name='artists')

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

    def __str__(self):
        return self.title


class Playlist(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    songs = models.ManyToManyField(Song, blank=True)

    def __str__(self):
        return self.name



