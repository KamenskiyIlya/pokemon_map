import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime
from .models import Pokemon, PokemonEntity


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
    datetime_now = localtime()
    pokemon_entitys = PokemonEntity.objects.filter(
        appeared_at__lt=datetime_now,
        disappeared_at__gt=datetime_now
        )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entitys:
        img_url = request.build_absolute_uri(pokemon_entity.pokemon.photo.url) 
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )

    pokemons_on_page = []
    for pokemon in pokemons:
        if pokemon.photo:
            img_url = request.build_absolute_uri(pokemon.photo.url)
        else:
            img_url = None
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.name,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    if pokemon.photo:
        img_url = request.build_absolute_uri(pokemon.photo.url)
    else:
        img_url = None


    datetime_now = localtime()
    pokemon_entitys = PokemonEntity.objects.filter(
        appeared_at__lt=datetime_now,
        disappeared_at__gt=datetime_now,
        pokemon=pokemon
        )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entitys:
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )

    previous_evolution = None
    if pokemon.previous_evolution:
        prev_pokemon = pokemon.previous_evolution
        if prev_pokemon.photo:
            prev_img_url = request.build_absolute_uri(prev_pokemon.photo.url)
        else:
            prev_img_url = None
        previous_evolution = {
            "title_ru": prev_pokemon.name,
            "pokemon_id": prev_pokemon.id,
            "img_url": prev_img_url
        }


    pokemon_inf ={
        "pokemon_id": pokemon.id,
        "title_ru": pokemon.name,
        "title_en": pokemon.name_en,
        "title_jp": pokemon.name_jp,
        "description": pokemon.description,
        "img_url": img_url,
        "previous_evolution": previous_evolution
    }
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_inf
    })
