from django.shortcuts import render
from club.models.club import Club
from disciplinas.models import Disciplina

def home(request):
    club = Club.objects.filter(id=1)
    disciplinas = Disciplina.objects.filter(club=club[0])
    data = {
        'disciplinas': disciplinas
    }
    return render(request, 'index.html', data)