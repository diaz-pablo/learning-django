from django import forms
from catalogo.models import Genero, Autor, Libro, Idioma, Ejemplar
from django.forms.widgets import NumberInput

class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ('nombre',)

class IdiomaForm(forms.ModelForm):
    class Meta:
        model = Idioma
        fields = ('nombre',)

# class AutorFormCreate(forms.ModelForm):
#     class Meta:
#         model = Autor
#         fields = ('apellido', 'nombre','fechaNac', 'fechaDeceso', 'image')

#         widgets = {
#             'fechaNac': NumberInput(attrs={'type': 'date'}),
#             'fechaDeceso': NumberInput(attrs={'type': 'date'}),
#         }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ('apellido', 'nombre','fechaNac', 'fechaDeceso', 'image')

        widgets = {
            'fechaNac': NumberInput(attrs={'type': 'date'}),
            'fechaDeceso': NumberInput(attrs={'type': 'date'}),
        }
    
    # def __init__(self, *args, **kwargs):
    #     super(self.__class__, self).__init__(*args, **kwargs)

    #     self.fields['image'].required = False

    def clean(self):
        super(AuthorForm, self).clean()

        apellido = self.cleaned_data.get('apellido')
        nombre = self.cleaned_data.get('nombre')
        fechaNac = self.cleaned_data.get('fechaNac')
        fechaDeceso = self.cleaned_data.get('fechaDeceso')

        if apellido != None:
            if len(apellido) < 3:
                self._errors['apellido'] = self.error_class(['El apellido debe tener al menos 3 caracteres'])
           
        if nombre != None:
            if len(nombre) < 5:
                self._errors['nombre'] = self.error_class(['El nombre debe tener al menos 5 caracteres'])

        if fechaNac != None and fechaDeceso != None:
            if fechaDeceso<fechaNac:
                self._errors['fechaDeceso'] = self.error_class(['La fecha de deceso debe ser mayor  a la de nacimiento'])
    
        return self.cleaned_data

class BookForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ('titulo', 'autor', 'resumen', 'isbn', 'idioma', 'genero', 'image')

    # genders = forms.ModelMultipleChoiceField(queryset=Genero.objects.all())

class EjemplarForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id'].disabled = True

    class Meta:
        model = Ejemplar
        fields = ('id', 'libro','estado', 'fechaDevolucion')

        widgets = {
            'fechaDevolucion': NumberInput(attrs={'type': 'date'}),
        }