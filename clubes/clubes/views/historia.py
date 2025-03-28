from django.shortcuts import render
from club.models.club import Club
from disciplinas.models import Disciplina

def historia(request):

    mi_club = Club.objects.filter(id=1)
    disciplinas = Disciplina.objects.filter(club=mi_club[0])
    data = {
        'disciplinas': disciplinas,
    }
    return render(request, 'historia.html', data)