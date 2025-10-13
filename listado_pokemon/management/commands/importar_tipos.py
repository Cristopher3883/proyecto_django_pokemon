# listado_pokemon/management/commands/importar_tipos.py
import requests
from django.core.management.base import BaseCommand
from listado_pokemon.models import Type  # Ajusta según tu app

class Command(BaseCommand):
    help = "Importa todos los tipos de Pokémon desde la PokeAPI con sprite de generación VII (Let's Go)"

    def handle(self, *args, **options):
        url = "https://pokeapi.co/api/v2/type/"
        response = requests.get(url)

        if response.status_code != 200:
            self.stdout.write(self.style.ERROR("❌ No se pudo obtener la lista de tipos"))
            return

        tipos = response.json().get("results", [])
        self.stdout.write(self.style.SUCCESS(f"Se encontraron {len(tipos)} tipos."))

        for idx, tipo in enumerate(tipos, start=1):
            type_name = tipo["name"]
            type_detail = requests.get(tipo["url"])

            if type_detail.status_code != 200:
                self.stdout.write(self.style.WARNING(f"No se pudo obtener {type_name}"))
                continue

            type_data = type_detail.json()
            sprite_url = type_data.get("sprites", {}) \
                .get("generation-vii", {}) \
                .get("lets-go", {}) \
                .get("front_default")

            tipo_obj, created = Type.objects.update_or_create(
                nombre=type_name,
                defaults={"img": sprite_url}
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"[{idx}] ✅ {type_name} creado con sprite"))
            else:
                self.stdout.write(self.style.SUCCESS(f"[{idx}] ✅ {type_name} actualizado con sprite"))

        self.stdout.write(self.style.SUCCESS("🎉 ¡Importación de tipos completada con éxito!"))