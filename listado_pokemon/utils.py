# listado_pokemon/utils.py
import requests
from .models import Pokemon, Type
from django.db import transaction
from django.db.models import Q

def import_all_pokemons():
    url = "https://pokeapi.co/api/v2/pokemon?limit=10000"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": "No se pudo obtener la lista de Pokémon"}

    pokemons = response.json().get("results", [])
    resultados = []

    for idx, p in enumerate(pokemons, start=1):
        detail = requests.get(p["url"])
        if detail.status_code != 200:
            resultados.append(f"No se pudo obtener {p['name']}")
            continue

        data = detail.json()

        stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
        hp = stats.get("hp", 0)
        attack = stats.get("attack", 0)
        defense = stats.get("defense", 0)
        special_attack = stats.get("special-attack", 0)
        special_defense = stats.get("special-defense", 0)
        speed = stats.get("speed", 0)

        poke, created = Pokemon.objects.update_or_create(
            nombre=data["name"],
            defaults={
                "hp": hp,
                "attack": attack,
                "defense": defense,
                "special_attack": special_attack,
                "special_defense": special_defense,
                "speed": speed,
                "weight": data["weight"] / 10,
                "height": data.get("height", 0),
                "img": data["sprites"]["other"]["official-artwork"]["front_default"]
                        or data["sprites"]["front_default"],
            },
        )

        # Tipos
        poke.types.clear()
        for tipo in data["types"]:
            type_name = tipo["type"]["name"]
            tipo_obj, _ = Type.objects.update_or_create(nombre=type_name)
            poke.types.add(tipo_obj)

        # Evoluciones
        species_url = data["species"]["url"]
        species_detail = requests.get(species_url)
        if species_detail.status_code == 200:
            species_data = species_detail.json()
            evo_chain_url = species_data.get("evolution_chain", {}).get("url")
            if evo_chain_url:
                import_evolution_chain(evo_chain_url, poke)

        resultados.append(f"[{idx}] {poke.nombre} guardado")

    return {"success": resultados}


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
        evo_poke, _ = Pokemon.objects.get_or_create(
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
            },
        )
        base_pokemon.evoluciones.add(evo_poke)