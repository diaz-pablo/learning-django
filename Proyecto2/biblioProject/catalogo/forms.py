from django import forms
from catalogo.models import Genero, Autor, Idioma
from django.forms.widgets import NumberInput

class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ('nombre',)

class IdiomaForm(forms.ModelForm):
    class Meta:
        model = Idioma
        fields = ('nombre',)

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ('apellido', 'nombre','fechaNac', 'fechaDeceso', 'image')

        widgets = {
            'fechaNac': NumberInput(attrs={'type': 'date'}),
            'fechaDeceso': NumberInput(attrs={'type': 'date'}),
        }