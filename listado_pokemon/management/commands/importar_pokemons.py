import requests
from django.core.management.base import BaseCommand
from listado_pokemon.models import Pokemon, Type


class Command(BaseCommand):
    help = "Importa todos los Pokémon y tipos desde la PokeAPI (con sprites de Let's Go Pikachu/Eevee)"

    def handle(self, *args, **options):
        url = "https://pokeapi.co/api/v2/pokemon?limit=100"
        response = requests.get(url)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR("❌ No se pudo obtener la lista de Pokémon"))
            return

        pokemons = response.json().get("results", [])
        self.stdout.write(self.style.SUCCESS(f"Se encontraron {len(pokemons)} Pokémon."))

        for idx, p in enumerate(pokemons, start=1):
            detail = requests.get(p["url"])
            if detail.status_code != 200:
                self.stdout.write(self.style.WARNING(f"No se pudo obtener {p['name']}"))
                continue

            data = detail.json()

            # Extraer estadísticas
            stats = {s["stat"]["name"]: s["base_stat"] for s in data["stats"]}
            hp = stats.get("hp", 0)
            attack = stats.get("attack", 0)
            defense = stats.get("defense", 0)
            special_attack = stats.get("special-attack", 0)
            special_defense = stats.get("special-defense", 0)
            speed = stats.get("speed", 0)

            # Guardar o actualizar Pokémon
            poke, _ = Pokemon.objects.update_or_create(
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
                    "img": (
                        data["sprites"]["other"]["official-artwork"]["front_default"]
                        or data["sprites"]["front_default"]
                    ),
                },
            )

            # Tipos (ManyToMany)
            poke.types.clear()
            for tipo in data["types"]:
                type_name = tipo["type"]["name"]
                type_url = tipo["type"]["url"]

                # Obtener sprite del tipo
                sprite_url = None
                type_detail = requests.get(type_url)
                if type_detail.status_code == 200:
                    type_data = type_detail.json()

                    # Buscar dentro de generation-vii / lets-go-pikachu-lets-go-eevee
                    try:
                        sprite_url = (
                            type_data["sprites"]
                            ["generation-vii"]
                            ["lets-go-pikachu-lets-go-eevee"]
                            ["name_icon"]
                        )
                    except KeyError:
                        # Si no existe esa generación, usar otra alternativa (por ejemplo, generation-viii)
                        sprite_url = (
                            type_data["sprites"]
                            .get("generation-viii", {})
                            .get("sword-shield", {})
                            .get("name_icon")
                        )

                tipo_obj, _ = Type.objects.update_or_create(
                    nombre=type_name,
                    defaults={"img": sprite_url},
                )
                poke.types.add(tipo_obj)

            self.stdout.write(self.style.SUCCESS(f"[{idx}] ✅ {poke.nombre} guardado."))

        self.stdout.write(self.style.SUCCESS("🎉 ¡Importación completada con éxito!"))