from django import forms

from .models import Disciplina
from django_svg_image_form_field import SvgAndImageFormField


class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        exclude = ['club']
        field_classes = {
            'imagen': SvgAndImageFormField,
        }
