from django.shortcuts import render, HttpResponse, get_object_or_404

from .models import Pokemon, Type
from .utils import import_all_pokemons

from django.contrib.auth.decorators import login_required

from django.db.models import Avg, FloatField, Count, IntegerField
from django.db.models.functions import Coalesce

import json
import requests

@login_required  # protege la vista
def home(request):
    return HttpResponse("Inicio")

@login_required  # protege la vista
def listado_pokemons(request):
    pokemons = Pokemon.objects.all()  # Trae todos los Pokémon
    context = {
        "pokemons": pokemons
    }
    
    return render(request,"tables.html",context)

@login_required  # protege la vista
def pokemon_detail(request,id):
    pokemon = get_object_or_404(Pokemon, id=id)
    primer_tipo = pokemon.types.first()
    return render(request, 'pokemon_detail.html', {'pokemon': pokemon,'primer_tipo':primer_tipo})
    
@login_required  # protege la vista
def listado_pokemon_stadistics(request):
    # Obtenemos todos los tipos con el promedio de HP de sus pokemons
    tipos = Type.objects.annotate(
        media_hp=Coalesce(Avg('pokemons__hp'), 0, output_field=FloatField()),
        media_attack=Coalesce(Avg('pokemons__attack'), 0, output_field=FloatField()),
        media_defense=Coalesce(Avg('pokemons__defense'), 0, output_field=FloatField()),
        media_speed=Coalesce(Avg('pokemons__speed'), 0, output_field=FloatField()),
        media_special_defense=Coalesce(Avg('pokemons__special_defense'), 0, output_field=FloatField()),
        media_special_attack=Coalesce(Avg('pokemons__special_attack'), 0, output_field=FloatField()),
        num_pokemon=Coalesce(Count('pokemons'), 0, output_field=IntegerField()),
    )

    # Opcional: podemos ordenar por la media de HP
    #tipos = tipos.order_by('-media_hp')
    
    nombres_tipos = [t.nombre for t in tipos]
    medias_vida = [t.media_hp for t in tipos]
    medias_ataque = [t.media_attack for t in tipos]
    medias_defensa = [t.media_defense for t in tipos]
    medias_velocidad = [t.media_speed for t in tipos]
    medias_especial_defensa = [t.media_special_defense for t in tipos]
    medias_especial_ataque = [t.media_special_attack for t in tipos]
    num_pokemon = [t.num_pokemon for t in tipos]
    
    context = {
        'nombres_tipos': json.dumps(nombres_tipos),
        'medias_vida': json.dumps(medias_vida),
        'medias_ataque': json.dumps(medias_ataque),
        'medias_defensa': json.dumps(medias_defensa),
        'medias_velocidad': json.dumps(medias_velocidad),
        'medias_especial_defensa': json.dumps(medias_especial_defensa),
        'medias_especial_ataque': json.dumps(medias_especial_ataque),
        'num_pokemon': json.dumps(num_pokemon),
    }
               
    return render(request,"stadistics.html",context)

@login_required  # protege la vista
def cargar_pokemons(request):

    return render(request, "cargar_pokemons.html")


#-----------------------------------------------------
def importar_pokemons(request):
    url = "https://pokeapi.co/api/v2/pokemon?limit=10"
    response = requests.get(url)

    if response.status_code != 200:
        return HttpResponse("❌ No se pudo obtener la lista de Pokémon", status=500)

    pokemons = response.json().get("results", [])
    mensajes = [f"Se encontraron {len(pokemons)} Pokémon."]

    for idx, p in enumerate(pokemons, start=1):
        detail = requests.get(p["url"])
        if detail.status_code != 200:
            mensajes.append(f"No se pudo obtener {p['name']}")
            continue

        data = detail.json()

        stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
        poke, created = Pokemon.objects.update_or_create(
            nombre=data["name"],
            defaults={
                "hp": stats.get("hp", 0),
                "attack": stats.get("attack", 0),
                "defense": stats.get("defense", 0),
                "special_attack": stats.get("special-attack", 0),
                "special_defense": stats.get("special-defense", 0),
                "speed": stats.get("speed", 0),
                "weight": data["weight"] / 10,
                "height": data.get("height", 0),
                "img": (
                    data["sprites"]["other"]["official-artwork"]["front_default"]
                    or data["sprites"]["front_default"]
                ),
            },
        )

        # Tipos
        poke.types.clear()
        for tipo in data["types"]:
            type_name = tipo["type"]["name"]
            type_detail = requests.get(tipo["type"]["url"])
            sprite_url = None
            if type_detail.status_code == 200:
                type_data = type_detail.json()
                sprite_url = (
                    type_data.get("sprites", {})
                    .get("generation-vii", {})
                    .get("lets-go-pikachu-lets-go-eevee", {})
                    .get("name_icon")
                )

            tipo_obj, _ = Type.objects.update_or_create(
                nombre=type_name, defaults={"img": sprite_url}
            )
            poke.types.add(tipo_obj)

        # Evoluciones
        species_url = data["species"]["url"]
        species_detail = requests.get(species_url)
        if species_detail.status_code == 200:
            species_data = species_detail.json()
            evo_chain_url = species_data.get("evolution_chain", {}).get("url")
            if evo_chain_url:
                import_evolution_chain(evo_chain_url, poke)

        mensajes.append(f"[{idx}] ✅ {poke.nombre} guardado.")

    mensajes.append("🎉 ¡Importación completada con éxito!")
    return HttpResponse("<br>".join(mensajes))


def import_evolution_chain(url, base_pokemon):
    response = requests.get(url)
    if response.status_code != 200:
        return

    chain = response.json().get("chain", {})
    evo_list = []

    def traverse(node):
        evo_list.append(node["species"]["name"])
        for evo in node.get("evolves_to", []):
            traverse(evo)

    traverse(chain)

    for evo_name in evo_list:
        if evo_name == base_pokemon.nombre:
            continue

        evo_poke, created = Pokemon.objects.get_or_create(
            nombre=evo_name,
            defaults={
                "hp": 0,
                "attack": 0,
                "defense": 0,
                "special_attack": 0,
                "special_defense": 0,
                "speed": 0,
                "weight": 0,
                "height": 0,
                "img": None,
            }
        )
        base_pokemon.evoluciones.add(evo_poke)


 