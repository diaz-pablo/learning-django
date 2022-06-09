from django import forms
from catalogo.models import Genero, Autor, Idioma, Ejemplar
from django.forms.widgets import NumberInput

class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ('nombre',)

class IdiomaForm(forms.ModelForm):
    class Meta:
        model = Idioma
        fields = ('nombre',)

class AutorFormCreate(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ('apellido', 'nombre','fechaNac', 'fechaDeceso', 'image')

        widgets = {
            'fechaNac': NumberInput(attrs={'type': 'date'}),
            'fechaDeceso': NumberInput(attrs={'type': 'date'}),
        }

class AutorFormUpdate(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ('apellido', 'nombre','fechaNac', 'fechaDeceso', 'image')

        widgets = {
            'fechaNac': NumberInput(attrs={'type': 'date'}),
            'fechaDeceso': NumberInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        # asi vuelves tus campos no requeridos
        self.fields['image'].required = False

ESTADO_EJEMPLAR = (
    ('m', 'en Mantenimiento'),
    ('p', 'Prestado'),
    ('d', 'Disponible'),
    ('r', 'Reservado'),
)

class EjemplarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].disabled = True

        estado = forms.ChoiceField(
            widget=forms.Select,
            choices=ESTADO_EJEMPLAR,
            initial='d'
        )

    class Meta:
        model = Ejemplar
        fields = ('id', 'libro','estado')