from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from music.models import Artist, Song, Album, Playlist


class BasicModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass123')
        self.artist = Artist.objects.create(name='Test Artist')
        self.album = Album.objects.create(title='Test Album')
        self.song = Song.objects.create(title='Test Song', album=self.album)
        self.song.artists.add(self.artist)

    def test_artist_str(self):
        self.assertEqual(str(self.artist), 'Test Artist')

    def test_album_str(self):
        self.assertEqual(str(self.album), 'Test Album')

    def test_song_str(self):
        self.assertEqual(str(self.song), 'Test Song')


class SongListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass123")
        self.artist = Artist.objects.create(name="Test Artist")
        self.album = Album.objects.create(title="Test Album")
        self.song = Song.objects.create(title="Test Song", album=self.album)
        self.song.artists.add(self.artist)

    def test_song_list_requires_login(self):
        resp = self.client.get(reverse('song_list'))
        self.assertEqual(resp.status_code, 302)  # redirect to login

    def test_song_list_logged_in(self):
        self.client.login(username="tester", password="pass123")
        resp = self.client.get(reverse('song_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "song_list.html")
        self.assertContains(resp, "Test Song")


class UploadSongViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass123")
        self.album = Album.objects.create(title="Upload Album")

    def test_upload_requires_login(self):
        response = self.client.get(reverse('upload_song'))
        self.assertEqual(response.status_code, 302)

    def test_upload_song_valid_post(self):
        self.client.login(username="tester", password="pass123")

        fake_mp3 = SimpleUploadedFile(
            "song.mp3",
            b"fake-audio-content",
            content_type="audio/mpeg"
        )

        response = self.client.post(reverse('upload_song'), {
            "title": "Uploaded Song",
            "album": self.album.id,
            "file": fake_mp3
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Song.objects.filter(title="Uploaded Song").exists())

    def test_upload_song_invalid_post(self):
        self.client.login(username="tester", password="pass123")

        response = self.client.post(reverse('upload_song'), {
            "title": "",
            "album": "",
        })

        self.assertEqual(response.status_code, 200)  # stays on page
        self.assertContains(response, "error")


class PlaylistTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass123")
        self.playlist = Playlist.objects.create(name="My Playlist", user=self.user)

        self.album = Album.objects.create(title="Album 1")
        self.song = Song.objects.create(title="Song 1", album=self.album)

    def test_playlist_str(self):
        self.assertEqual(str(self.playlist), "My Playlist")

    def test_add_song_to_playlist(self):
        self.client.login(username="tester", password="pass123")

        response = self.client.post(reverse('add_song_to_playlist', args=[self.song.id]), {
            "playlist": self.playlist.id
        })

        self.assertEqual(response.status_code, 302)
        self.assertIn(self.song, self.playlist.songs.all())

