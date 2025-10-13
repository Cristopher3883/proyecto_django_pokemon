from django.urls import path
from listado_pokemon import views

urlpatterns = [
    path('inicio/', views.home),
    path('listado/', views.listado_pokemons, name='listado'),
     path('pokemon/<int:id>/', views.pokemon_detail, name='pokemon_detail'),
]