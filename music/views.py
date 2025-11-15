from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import DatabaseError
from .models import Artist, Album, Song, Playlist
from .forms import SongForm
from django.http import FileResponse, Http404
import mimetypes
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)
logger = logging.getLogger('music')
try:
    ...
except Exception as e:
    logger.exception("Eroare la upload_song")
    messages.error(request, "Eroare neașteptată.")


# ======================
# Pagina de bun venit
# ======================
def welcome(request):
    return render(request, 'music/welcome.html')


# ======================
# Înregistrare utilizator
# ======================
def register(request):
    try:
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Contul tău a fost creat cu succes!')
                return redirect('welcome')
            else:
                messages.error(request, 'Datele introduse nu sunt valide. Încearcă din nou.')
        else:
            form = UserCreationForm()
    except DatabaseError:
        logger.exception("DatabaseError la register")
        messages.error(request, 'Eroare la baza de date. Încearcă mai târziu.')
        form = UserCreationForm()
    except Exception as e:
        logger.exception("Eroare neașteptată la register")
        messages.error(request, 'A apărut o eroare neașteptată. Administratorul a fost notificat.')
        form = UserCreationForm()

    return render(request, 'music/register.html', {'form': form})


# ======================
# Autentificare utilizator
# ======================
def user_login(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Autentificare reușită!')
                return redirect('welcome')
            else:
                messages.error(request, 'Nume utilizator sau parolă incorectă.')
        return render(request, 'music/login.html')
    except Exception as e:
        logger.exception("Eroare la autentificare")
        messages.error(request, 'A apărut o eroare la autentificare. Administratorul a fost notificat.')
        return render(request, 'music/login.html')


    # ======================
# Delogare utilizator
# ======================
def user_logout(request):
    try:
        logout(request)
        messages.info(request, 'Te-ai delogat cu succes.')
        return redirect('welcome')
    except Exception as e:
        messages.error(request, f'Eroare la delogare: {e}')
        return redirect('welcome')


# ======================
# Pagina principală
# ======================
@login_required(login_url='login')
def index(request):
    try:
        return render(request, 'music/index.html')
    except Exception as e:
        messages.error(request, f'A apărut o eroare la încărcarea paginii: {e}')
        return render(request, 'music/index.html')


# ======================
# Lista artiștilor
# ======================
@login_required(login_url='login')
def artist_list(request):
    try:
        artists = Artist.objects.all()
        if not artists:
            messages.warning(request, 'Momentan nu există artiști în baza de date.')
        return render(request, 'music/artists.html', {'artists': artists})
    except DatabaseError:
        messages.error(request, 'Eroare la conectarea la baza de date.')
        return render(request, 'music/artists.html', {'artists': []})
    except Exception as e:
        messages.error(request, f'A apărut o eroare neașteptată: {e}')
        return render(request, 'music/artists.html', {'artists': []})


# ======================
# Detalii artist
# ======================
@login_required(login_url='login')
def artist_detail(request, artist_id):
    try:
        artist = get_object_or_404(Artist, id=artist_id)
        albums = artist.album_set.all()
        return render(request, 'music/artist_detail.html', {'artist': artist, 'albums': albums})
    except DatabaseError:
        messages.error(request, 'Eroare la baza de date. Nu s-au putut încărca detaliile artistului.')
        return redirect('artist_list')
    except Exception as e:
        messages.error(request, f'Eroare neașteptată: {e}')
        return redirect('artist_list')


# ======================
# Detalii album
# ======================
@login_required(login_url='login')
def album_detail(request, album_id):
    try:
        album = get_object_or_404(Album, id=album_id)
        songs = album.song_set.all()
        return render(request, 'music/album_detail.html', {'album': album, 'songs': songs})
    except DatabaseError:
        messages.error(request, 'Eroare la baza de date. Nu s-au putut încărca melodiile.')
        return redirect('artist_list')
    except Exception as e:
        messages.error(request, f'Eroare neașteptată: {e}')
        return redirect('artist_list')


# ======================
# Lista playlist-uri
# ======================
@login_required(login_url='login')
def playlist_list(request):
    try:
        playlists = Playlist.objects.all()
        if not playlists:
            messages.warning(request, 'Nu există playlist-uri disponibile.')
        return render(request, 'music/playlist_list.html', {'playlists': playlists})
    except DatabaseError:
        messages.error(request, 'Eroare la baza de date.')
        return render(request, 'music/playlist_list.html', {'playlists': []})
    except Exception as e:
        messages.error(request, f'Eroare neașteptată: {e}')
        return render(request, 'music/playlist_list.html', {'playlists': []})


# ======================
# Detalii playlist
# ======================
@login_required(login_url='login')
def playlist_detail(request, playlist_id):
    try:
        playlist = get_object_or_404(Playlist, id=playlist_id)
        songs = playlist.songs.all()
        return render(request, 'music/playlist_detail.html', {'playlist': playlist, 'songs': songs})
    except DatabaseError:
        messages.error(request, 'Eroare la baza de date. Nu s-au putut încărca melodiile din playlist.')
        return redirect('playlist_list')
    except Exception as e:
        logger.exception(request, f'Eroare neașteptată: {e}')
        return redirect('playlist_list')


# ======================
# Adaugă melodie în playlist
# ======================
@login_required(login_url='login')
def add_song_to_playlist(request, playlist_id, song_id):
    try:
        playlist = get_object_or_404(Playlist, id=playlist_id)
        song = get_object_or_404(Song, id=song_id)
        playlist.songs.add(song)
        messages.success(request, f'Melodia "{song.title}" a fost adăugată în playlist!')
    except DatabaseError:
        logger.exception("DatabaseError la add_song_to_playlist")
        messages.error(request, 'Eroare la baza de date. Melodia nu a fost adăugată.')
    except Exception:
        logger.exception("Eroare neașteptată la add_song_to_playlist")
        messages.error(request, 'A apărut o eroare neașteptată. Administratorul a fost notificat.')
    return redirect('playlist_detail', playlist_id=playlist_id)


# ======================
# Șterge melodie din playlist
# ======================
@login_required(login_url='login')
def remove_song_from_playlist(request, playlist_id, song_id):
    try:
        playlist = get_object_or_404(Playlist, id=playlist_id)
        song = get_object_or_404(Song, id=song_id)
        playlist.songs.remove(song)
        messages.info(request, f'Melodia "{song.title}" a fost ștearsă din playlist.')
    except DatabaseError:
        messages.error(request, 'Eroare la baza de date. Melodia nu a putut fi ștearsă.')
    except Exception as e:
        messages.error(request, f'Eroare neașteptată: {e}')
    return redirect('playlist_detail', playlist_id=playlist_id)


# ======================
# Lista melodiilor
# ======================
@login_required(login_url='login')
def song_list(request):
    try:
        songs = Song.objects.all()
        return render(request, 'music/song_list.html', {'songs': songs})
    except DatabaseError:
        messages.error(request, 'Eroare la baza de date. Melodiile nu pot fi afișate.')
        return render(request, 'music/song_list.html', {'songs': []})
    except Exception as e:
        logger.exception(request, f'Eroare neașteptată: {e}')
        return render(request, 'music/song_list.html', {'songs': []})


# ======================
# Detalii melodie
# ======================
@login_required(login_url='login')
def song_detail(request, song_id):
    try:
        song = get_object_or_404(Song, id=song_id)
        return render(request, 'music/song_detail.html', {'song': song})
    except Exception as e:
        messages.error(request, f'Eroare neașteptată: {e}')
        return redirect('song_list')


# ======================
# Încărcare melodie nouă
# ======================
@login_required(login_url='login')
def upload_song(request):
    try:
        if request.method == 'POST':
            form = SongForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Melodia a fost încărcată cu succes!')
                return redirect('song_list')
            else:
                messages.error(request, 'Formular invalid. Verifică datele introduse.')
        else:
            form = SongForm()
    except DatabaseError as db_error:
        logger.exception("DatabaseError la upload_song")
        messages.error(request, 'Eroare la salvarea în baza de date. Încearcă mai târziu.')
        form = SongForm()
    except Exception as e:
        # logger.exception va include stack trace în errors.log
        logger.exception("Eroare neașteptată la upload_song")
        messages.error(request, 'A apărut o eroare neașteptată. Administratorul a fost notificat.')
        form = SongForm()
    return render(request, 'music/upload_song.html', {'form': form})

@login_required
def download_song(request, song_id):
    song = get_object_or_404(Song, id=song_id)
    if not song.audio_file:
        messages.error(request, "Melodia nu are fișier atașat.")
        return redirect('song_detail', song_id=song_id)
    file_path = song.audio_file.path
    if not os.path.exists(file_path):
        raise Http404("Fișierul nu a fost găsit.")
    mime_type, _ = mimetypes.guess_type(file_path)
    response = FileResponse(open(file_path, 'rb'), as_attachment=True, filename=os.path.basename(file_path))
    if mime_type:
        response['Content-Type'] = mime_type
    return response