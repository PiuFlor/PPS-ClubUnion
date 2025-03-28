from django.shortcuts import render
from club.models.club import Club
from disciplinas.models import Disciplina

def disciplina(request, id):
    
    disciplina = Disciplina.objects.filter(id=id)[0]
    mi_club = Club.objects.filter(id=1)
    disciplinas = Disciplina.objects.filter(club=mi_club[0])
    data = {
        'disciplina': disciplina,
        'disciplinas': disciplinas,
    }
    return render(request, 'disciplina.html', data)