from django.shortcuts import render
from club.models.club import Club
from disciplinas.models import Disciplina
from indumentaria.models import Articulo, TipoArticulo

def indumentaria(request):
    
    mi_club = Club.objects.filter(id=1)
    tipos = TipoArticulo.objects.filter()
    articulos = Articulo.objects.filter(club=mi_club[0])
    disciplinas = Disciplina.objects.filter(club=mi_club[0])
    data = {
        'tipos' : tipos,
        'disciplinas': disciplinas,
        'articulos' : articulos
    }
    return render(request, 'indumentaria.html', data)