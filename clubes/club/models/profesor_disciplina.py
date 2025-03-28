from django.db import models
from . import Personal
from disciplinas.models import Disciplina

class ProfesorDisciplina(models.Model):

    profesor = models.ForeignKey(Personal, on_delete=models.CASCADE)#limitar q solo sea personal de tipo profesor
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profesor} - {self.disciplina}"
    
    class Meta:
        verbose_name_plural = "Profesor Disciplina"
        verbose_name = "Profesor Disciplina"