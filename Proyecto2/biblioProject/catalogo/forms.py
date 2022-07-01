from django import forms
# from Proyecto2.biblioProject.catalogo.models import CustomUser
from catalogo.models import Autor, Libro, Ejemplar, Genero, Idioma, CustomUser
from django.forms.widgets import NumberInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError

class AuthorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)

        self.fields['apellido'].label = "Apellido"
        self.fields['nombre'].label = "Nombre"        
        self.fields['fechaNac'].label = "Fecha de Nacimiento"
        self.fields['fechaDeceso'].label = "Fecha de Deceso"       
        self.fields['image'].label = "Imagen"       

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

    class Meta:
        model = Autor
        fields = ('apellido', 'nombre','fechaNac', 'fechaDeceso', 'image')

        widgets = {
            'fechaNac': NumberInput(attrs={'type': 'date'}),
            'fechaDeceso': NumberInput(attrs={'type': 'date'}),
        }

class BookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)

        self.fields['titulo'].label = "Título"
        self.fields['autor'].label = "Autor"
        self.fields['resumen'].label = "Resumen"
        self.fields['isbn'].label = "ISBN"
        self.fields['idioma'].label = "Idioma"
        self.fields['genero'].label = "Género/s"
        self.fields['image'].label = "Imagen"

    def clean_titulo(self):
        titulo = self.cleaned_data['titulo']
        existe = Libro.objects.filter(titulo__iexact=titulo).exists()

        if existe:
            raise ValidationError("El título del libro ya existe!")

        return titulo

    class Meta:
        model = Libro
        fields = ('titulo', 'autor', 'resumen', 'isbn', 'idioma', 'genero', 'image')


class CopyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CopyForm, self).__init__(*args, **kwargs)

        self.fields['id'].label = "Id"
        self.fields['libro'].label = "Libro"
        self.fields['estado'].label = "Estado"
        self.fields['fechaDevolucion'].label = "Fecha de Devolución"
        self.fields['usuario'].label = "Usuario"

        self.fields['id'].disabled = True
        # self.fields['libro'].required = False

    class Meta:
        model = Ejemplar
        fields = ('id', 'libro', 'estado', 'fechaDevolucion', 'usuario')

        widgets = {
            'fechaDevolucion': NumberInput(attrs={'type': 'date'}),
        }

class GenderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GenderForm, self).__init__(*args, **kwargs)

        self.fields['nombre'].label = "Nombre"

    class Meta:
        model = Genero
        fields = ('nombre',)

class LanguageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LanguageForm, self).__init__(*args, **kwargs)

        self.fields['nombre'].label = "Nombre"

    class Meta:
        model = Idioma
        fields = ('nombre',)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'latitude', 'longitude')