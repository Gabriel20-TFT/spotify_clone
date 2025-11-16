import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spotify_clone.settings")
django.setup()

from music.models import Artist, Genre


def migrate_genres():
    print("🎵 Începem migrarea genurilor din text în relații...\n")

    artists = Artist.objects.all()

    if not artists:
        print("❌ Nu există artiști în baza de date!")
        return

    print(f"📊 Găsiți {artists.count()} artiști\n")

    migrated_count = 0
    created_genres = set()

    for artist in artists:
        if artist.genre:  # Dacă are gen în câmpul text
            print(f"🎤 {artist.name}")
            print(f"   Gen text: {artist.genre}")

            # Split dacă sunt multiple genuri separate prin virgulă
            genre_text = artist.genre.replace('/', ',')
            genre_names = [g.strip() for g in genre_text.split(',') if g.strip()]



            for genre_name in genre_names:
                if genre_name:
                    # Creează genul dacă nu există
                    genre_obj, created = Genre.objects.get_or_create(name=genre_name)

                    if created:
                        created_genres.add(genre_name)
                        print(f"   ✅ Gen creat: {genre_name}")

                    # Adaugă la relația ManyToMany (dacă nu e deja adăugat)
                    if genre_obj not in artist.genres.all():
                        artist.genres.add(genre_obj)
                        print(f"   🔗 Asociat cu: {genre_name}")

            migrated_count += 1
            print()
        else:
            print(f"⚠️  {artist.name} - nu are gen specificat")
            print()

    print("=" * 60)
    print(f"🎉 Migrare completă!")
    print(f"   ✅ Artiști procesați: {migrated_count}/{artists.count()}")
    print(f"   ✨ Genuri noi create: {len(created_genres)}")
    print(f"   📊 Total genuri în baza de date: {Genre.objects.count()}")

    if created_genres:
        print(f"\n🎨 Genuri create:")
        for genre in sorted(created_genres):
            count = Genre.objects.get(name=genre).artists.count()
            print(f"   - {genre}: {count} artiști")

    print("\n📈 Statistici finale:")
    for genre in Genre.objects.all().order_by('name'):
        count = genre.artists.count()
        if count > 0:
            artists_names = ", ".join([a.name for a in genre.artists.all()[:3]])
            if count > 3:
                artists_names += f" (+{count - 3} alții)"
            print(f"   {genre.name}: {count} artiști ({artists_names})")


if __name__ == "__main__":
    migrate_genres()