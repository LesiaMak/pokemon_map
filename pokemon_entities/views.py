import folium
from django.shortcuts import render
from django.utils import timezone
from pokemon_entities.models import Pokemon
from pokemon_entities.models import PokemonEntity
from django.shortcuts import get_object_or_404


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    now = timezone.now()
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=now, disappeared_at__gt=now)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url),
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
        })


def show_pokemon(request, pokemon_id):
    requested_pokemon = get_object_or_404(Pokemon, id=int(pokemon_id))
    pokemon = {
            'pokemon_id': requested_pokemon.id,
            'title_ru': requested_pokemon.title,
            'title_en': requested_pokemon.title_en,
            'title_jp': requested_pokemon.title_jp,
            'img_url': request.build_absolute_uri(requested_pokemon.image.url),
            'description': requested_pokemon.description,
            }
    pr_evol_pokemon = requested_pokemon.pre_evol
    next_evol_pokemon = requested_pokemon.next_evol.first()
    if pr_evol_pokemon:
        pokemon['previous_evolution'] = {
            "title_ru": pr_evol_pokemon.title,
            'pokemon_id': pr_evol_pokemon.id,
            'img_url': request.build_absolute_uri(pr_evol_pokemon.image.url)
            }
    if next_evol_pokemon:
        pokemon['next_evolution'] = {
            "title_ru": next_evol_pokemon.title,
            'pokemon_id': next_evol_pokemon.id,
            'img_url': request.build_absolute_uri(next_evol_pokemon.image.url)
                }

    pokemon_entities = PokemonEntity.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(requested_pokemon.image.url),
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
