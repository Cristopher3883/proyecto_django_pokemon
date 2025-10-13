from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Pokemon, Type

def home(request):
    return HttpResponse("Inicio")

def listado_pokemons(request):
    pokemons = Pokemon.objects.all()  # Trae todos los Pokémon
    context = {
        "pokemons": pokemons
    }
    
    return render(request,"tables.html",context)

def pokemon_detail(request,id):
    pokemon = get_object_or_404(Pokemon, id=id)
    return render(request, 'pokemon_detail.html', {'pokemon': pokemon})
    



