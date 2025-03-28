from django.shortcuts import render
from club.models.club import Club
from disciplinas.models import Disciplina
from indumentaria.models import Articulo, TipoArticulo

def tipoIndumentaria(request, id):
    
    mi_club = Club.objects.filter(id=1)
    tipos = TipoArticulo.objects.filter()
    tipo_buscado = TipoArticulo.objects.filter(id=id)
    articulos = Articulo.objects.filter(club=mi_club[0])
    articulos = articulos.filter(tipoArticulo=id)
    disciplinas = Disciplina.objects.filter(club=mi_club[0])

    data = {
        'tipos' : tipos,
        'tipo_buscado': tipo_buscado,
        'disciplina_buscada': False,
        'disciplinas': disciplinas,
        'articulos' : articulos
    }
    return render(request, 'indumentaria.html', data)