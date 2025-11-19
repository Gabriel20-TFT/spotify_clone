from django import forms
from .models import Song
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import os


class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'artists', 'album', 'audio_file', 'cover_image','duration']

    def clean(self):
        cleaned_data = super().clean()
        artists = cleaned_data.get("artists")
        album = cleaned_data.get("album")

        if album and artists:
            if album.artist not in artists:
                raise ValidationError(
                    "Albumul selectat nu aparține artistului/artiștilor aleși."
                )

        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Obligatoriu. Introdu o adresă de email validă.')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
