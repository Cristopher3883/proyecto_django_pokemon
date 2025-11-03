from django.urls import path
from listado_pokemon import views

urlpatterns = [
    path('inicio/', views.home),
    path('listado/', views.listado_pokemons, name='listado'),
    path('listado-stadistics/', views.listado_pokemon_stadistics, name='listado_stadistics'),
    path('pokemon/<int:id>/', views.pokemon_detail, name='pokemon_detail'),
    path('cargar-pokemons/', views.cargar_pokemons, name='cargar_pokemons'),
    path('importar-pokemons/', views.importar_pokemons, name='importar-pokemons'),
]