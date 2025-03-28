from django.shortcuts import render
from club.models.club import Club
from disciplinas.models import Disciplina
from indumentaria.models import Articulo, TipoArticulo

def disciplinaIndumentaria(request, id):
    
    mi_club = Club.objects.filter(id=1)
    tipos = TipoArticulo.objects.filter()
    disciplina_buscada = Disciplina.objects.filter(id=id)
    articulos = Articulo.objects.filter(club=mi_club[0])
    articulos = articulos.filter(disciplina=id)
    disciplinas = Disciplina.objects.filter(club=mi_club[0])

    data = {
        'tipos' : tipos,
        'tipo_buscado': False,
        'disciplina_buscada': disciplina_buscada,
        'disciplinas': disciplinas,
        'articulos' : articulos
    }
    return render(request, 'indumentaria.html', data)