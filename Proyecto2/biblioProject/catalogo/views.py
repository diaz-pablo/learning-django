from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from catalogo.models import Idioma, Genero, Libro, Ejemplar, Autor
from django.views import generic
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from catalogo.forms import GeneroForm, AutorFormCreate, AutorFormUpdate, IdiomaForm, EjemplarForm

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

# De esta forma solo deja enviar datos del Autor
class AutorListView(generic.ListView):
    model = Autor
    context_object_name = 'autores'
    paginate_by = 5

    # en este caso va un modelo
    queryset = Autor.objects.all()
    # si quiero filtrar
    template_name='autores.html'
    # nombre del template

# De esta forma solo deja enviar datos del Autor
class AutorDetailView(generic.DetailView):
    model = Autor
    template_name = 'autor.html'
    # es obligatorio el nombre del template

    def autor_detail_view(request,pk):
        try:
            autor=Autor.objects.get(pk=pk)
        except Autor.DoesNotExist: # PREGUNTAR SOBRE ESTO!
            raise Http404("Oops! El Autor no existe")
        
        context = {
            'autor':autor,
        }

        return render(request, 'autor.html',context)

def autor_new(request):
    if request.method == "POST":
        formulario = AutorFormCreate(request.POST, request.FILES)

        if formulario.is_valid():
            autor = formulario.save(commit=False)
            autor.apellido = formulario.cleaned_data['apellido']
            autor.nombre = formulario.cleaned_data['nombre']
            autor.fechaNac = formulario.cleaned_data['fechaNac']
            autor.fechaDeceso = formulario.cleaned_data['fechaDeceso']
            autor.image = formulario.cleaned_data['image']
            autor.save()
            
            return redirect('autores')
    else:
        formulario = AutorFormCreate()

    return render(request, 'autor_new.html', {'formulario': formulario})

def autor_update(request, pk):
    autor = get_object_or_404(Autor, pk=pk)

    if request.method == "POST":
        formulario = AutorFormUpdate(request.POST, request.FILES)
    
        if formulario.is_valid():
            autor.apellido = formulario.cleaned_data['apellido']
            autor.nombre = formulario.cleaned_data['nombre']
            autor.fechaNac = formulario.cleaned_data['fechaNac']
            autor.fechaDeceso = formulario.cleaned_data['fechaDeceso']
            autor.image = formulario.cleaned_data['image']
            autor.save()
    
            return redirect('autores')
        else:
            return render(request, 'autor_new.html', {'formulario': formulario})
    else:
        formulario = AutorFormUpdate(instance=autor)

    return render(request, 'autor_new.html', {'formulario': formulario})

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