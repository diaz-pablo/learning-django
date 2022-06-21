from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from catalogo.models import Idioma, Genero, Libro, Ejemplar, Autor, POI
from django.views import generic
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib import messages
from catalogo.forms import GeneroForm, AutorForm, IdiomaForm, EjemplarForm
# para los graficos
# import random
from random import randint
# mapas
# import json
from django.core.serializers import serialize
from django.views.generic.base import TemplateView

# Create your views here.
def index(request):
    nroGeneros=Genero.objects.all().count()
    nroIdiomas=Idioma.objects.all().count()

    nroLibros=Libro.objects.all().count()
    nroEjemplares=Ejemplar.objects.all().count()
    nroDisponibles=Ejemplar.objects.filter(estado__exact='d').count()
    nroAutores=Autor.objects.count() # El 'all()' esta implícito por defecto.
    
    context = {
        'nroGeneros':nroGeneros,
        'nroIdiomas':nroIdiomas,
        'nroLibros':nroLibros,
        'nroEjemplares': nroEjemplares,
        'nroDisponibles': nroDisponibles,
        'nroAutores': nroAutores,
    }

    return render(request, 'index.html',context)

def genero_list(request):
    generos = Genero.objects.all()

    context = {
        'generos': generos
    }

    return render(request, 'genero_list.html', context)

def genero_new(request):
    if request.method == "POST":
        formulario = GeneroForm(request.POST)

        if formulario.is_valid():
            genero = formulario.save(commit=False)
            genero.nombre = formulario.cleaned_data['nombre']
            genero.save()
            
            return redirect('genero_list')
    else:
        formulario = GeneroForm()

    return render(request, 'genero_new.html', {'formulario': formulario})

def genero_update(request, pk):
    genero = get_object_or_404(Genero, pk=pk)
    if request.method == "POST":
        formulario = GeneroForm(request.POST, instance=genero)
        
        if formulario.is_valid():
            genero = formulario.save(commit=False)
            genero.nombre = formulario.cleaned_data['nombre']
            genero.save()

            return redirect('genero_list')
    else:
        formulario = GeneroForm(instance=genero)

    return render(request, 'genero_new.html', {'formulario': formulario})

def idioma_list(request):
    idiomas = Idioma.objects.all()

    context = {
        'idiomas': idiomas
    }

    return render(request, 'idioma_list.html', context)

def idioma_new(request):
    if request.method == "POST":
        formulario = IdiomaForm(request.POST)

        if formulario.is_valid():
            idioma = formulario.save(commit=False)
            idioma.nombre = formulario.cleaned_data['nombre']
            idioma.save()
            
            return redirect('idioma_list')
    else:
        formulario = IdiomaForm()

    return render(request, 'idioma_new.html', {'formulario': formulario})

def idioma_update(request, pk):
    idioma = get_object_or_404(Idioma, pk=pk)

    if request.method == "POST":
        formulario = IdiomaForm(request.POST, instance=idioma)
        
        if formulario.is_valid():
            idioma = formulario.save(commit=False)
            idioma.nombre = formulario.cleaned_data['nombre']
            idioma.save()

            return redirect('idioma_list')
    else:
        formulario = IdiomaForm(instance=idioma)

    return render(request, 'idioma_new.html', {'formulario': formulario})

def idioma_delete(request, pk):
    idioma = get_object_or_404(Idioma, pk=pk)
    idioma.delete()

    return redirect('idioma_list')
# De esta forma podemos mandar mas que datos del libro, podemos mandar datos de las relaciones y ademas se agregó la paginacion que en esta no anda como la anterior
class LibroListView(ListView):
    model = Libro
    template_name='libros.html'
    # nombre del template
    paginate_by = 5 # muestra la paginacion, pero muestra todo, NO muestra 3 por pagina

    def get_context_data(self, **kwargs):
        libros = Libro.objects.all()
        context = super(LibroListView, self).get_context_data(**kwargs)
        paginator = Paginator(libros, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            libros = paginator.page(page)
        except PageNotAnInteger:
            libros = paginator.page(1)
        except EmptyPage:
            libros = paginator.page(paginator.num_pages)

        context['libros'] = libros

        return context 

# De esta forma deja enviar datos del Libro y del Ejemplar
class LibroDetailView(DetailView):
    # specify the model to use
    model = Libro
    template_name = 'libro.html'
  
    # override context data
    def get_context_data(self, *args, **kwargs):
        libro = Libro.objects.get(pk=self.kwargs['pk'])
        context = super(LibroDetailView, self).get_context_data(*args, **kwargs)
        # add extra field
        context["ejemplares"] = Ejemplar.objects.filter(libro__pk=libro.pk)      
        return context

class EjemplarDetailView(generic.DetailView):
    model = Ejemplar
    template_name = 'ejemplar.html'

    # override context data
    def get_context_data(self, *args, **kwargs):
        context = super(EjemplarDetailView, self).get_context_data(*args, **kwargs)
        return context

""" AUTORES """
class AutorListView(generic.ListView):
    model = Autor
    context_object_name = 'authors'
    paginate_by = 5

    queryset = Autor.objects.order_by('-id')
    template_name = 'authors/index.html'

class AutorDetailView(generic.DetailView):
    model = Autor
    template_name = 'authors/show.html'

    def autor_detail_view(request,pk):
        try:
            autor=Autor.objects.get(pk=pk)
        except Autor.DoesNotExist:
            raise Http404("Oops! El Autor no existe")
        
        context = {
            'autor': autor,
        }

        return render(request, 'authors/show.html', context)

def author_create(request):
    if request.method == "POST":
        form = AutorForm(request.POST, request.FILES)

        if form.is_valid():
            author = form.save(commit=False)

            author.apellido = form.cleaned_data['apellido']
            author.nombre = form.cleaned_data['nombre']
            author.fechaNac = form.cleaned_data['fechaNac']
            author.fechaDeceso = form.cleaned_data['fechaDeceso']
            author.image = form.cleaned_data['image']
            
            author.save()

            messages.success(request, "¡Autor agregado exitosamente!")
            
            return redirect('author_list')
    else:
        form = AutorForm()

    context = {
        'form': form
    }

    return render(request, 'authors/create.html', context)

def author_update(request, pk):
    author = get_object_or_404(Autor, pk=pk)

    if request.method == "POST":
        form = AutorForm(request.POST, request.FILES)

        context = {
            'form': form
        }
    
        if form.is_valid():
            author.apellido = form.cleaned_data['apellido']
            author.nombre = form.cleaned_data['nombre']
            author.fechaNac = form.cleaned_data['fechaNac']
            author.fechaDeceso = form.cleaned_data['fechaDeceso']
            
            if len(request.FILES) != 0:
                author.image = form.cleaned_data['image']

            author.save()
    
            messages.success(request, "¡Autor actualizado exitosamente!")

            return redirect('author_list')
        else:
            return render(request, 'authors/edit.html', context)
    else:
        form = AutorForm(instance=author)

        context = {
            'form': form
        }

    return render(request, 'authors/edit.html', context)

def author_delete(request, pk):
    author = get_object_or_404(Autor, pk=pk)
    author.delete()

    messages.success(request, "¡Autor eliminado exitosamente!")

    return redirect('author_list')

def ejemplar_list(request):
    ejemplares = Ejemplar.objects.all()

    context = {
        'ejemplares': ejemplares
    }

    return render(request, 'ejemplar_list.html', context)

def ejemplar_new(request):
    if request.method == "POST":
        formulario = EjemplarForm(request.POST)

        if formulario.is_valid():
            ejemplar = formulario.save(commit=False)
            ejemplar.fechaDevolucion = formulario.cleaned_data["fechaDevolucion"]
            ejemplar.save()
            
            return redirect('ejemplar_list')
    else:
        formulario = EjemplarForm()

    return render(request, 'ejemplar_new.html', {'formulario': formulario})

def ChartData(request):
    chartLabel = "Préstamos"
    etiquetas = ['Enero', 'Febrero', 'Marzo','Abril', 'Mayo', 'Junio','Julio','Agosto','Setiembre','Octubre','Noviembre','Diciembre']
    meses = 12
    minimo= 10
    maximo = 100
    datos = []

    for i in range(meses):
        datos.append(randint(minimo, maximo))

    context ={
        "labels": etiquetas,
        "chartLabel": chartLabel,
        "data": datos,
    }

    return render(request, 'charts.html', context)

class POIsMapView(TemplateView):
    """POIS and map view."""
    
    template_name = "map.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        
        pois = POI.objects.all()
        lista=[]
        
        for poi in pois:
            json_dict={}
            json_dict['type'] = 'Feature'
            json_dict['properties'] = dict(name=poi.nombre)
            json_dict['geometry'] = dict(type='Point', coordinates=list([poi.lng,poi.lat]))
            lista.append(json_dict)

        context["markers"]= lista
        
        return context