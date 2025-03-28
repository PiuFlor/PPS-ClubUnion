from django import forms

from .models import TipoArticulo
from django_svg_image_form_field import SvgAndImageFormField


class TipoArticuloForm(forms.ModelForm):
    class Meta:
        model = TipoArticulo
        exclude = ['club']
        field_classes = {
            'imagen': SvgAndImageFormField,
        }