from multiprocessing import context
from django.shortcuts import render, redirect, get_object_or_404
from catalogo.models import Idioma, Genero, Libro, Ejemplar, Autor, POI
from django.db.models import Count
from django.views import generic
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib import messages
from catalogo.forms import AuthorForm, BookForm, CopyForm, GenderForm, LanguageForm
from random import randint
from django.views.generic.base import TemplateView

def index(request):
    nroGeneros = Genero.objects.all().count()
    nroIdiomas = Idioma.objects.all().count()

    nroLibros = Libro.objects.all().count()
    nroEjemplares = Ejemplar.objects.all().count()
    nroDisponibles = Ejemplar.objects.filter(estado__exact='d').count()
    nroAutores = Autor.objects.count()

    context = {
        'nroGeneros': nroGeneros,
        'nroIdiomas': nroIdiomas,
        'nroLibros': nroLibros,
        'nroEjemplares': nroEjemplares,
        'nroDisponibles': nroDisponibles,
        'nroAutores': nroAutores,
    }

    return render(request, 'index.html', context)

""" AUTORES """
class AuthorListView(generic.ListView):
    model = Autor
    context_object_name = 'authors'
    paginate_by = 5
    # context_object_name = 'authors'

    queryset = Autor.objects.order_by('-id')
    template_name = 'authors/index.html'

class AuthorDetailView(generic.DetailView):
    model = Autor
    template_name = 'authors/show.html'

    def autor_detail_view(request, pk):
        try:
            autor = Autor.objects.get(pk=pk)
        except Autor.DoesNotExist:
            raise Http404("Oops! El Autor no existe")

        context = {
            'autor': autor,
        }

        return render(request, 'authors/show.html', context)

def author_create(request):
    if request.method == "POST":
        form = AuthorForm(request.POST, request.FILES)

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
        form = AuthorForm()

    context = {
        'form': form
    }

    return render(request, 'authors/create.html', context)

def author_update(request, pk):
    author = get_object_or_404(Autor, pk=pk)

    if request.method == "POST":
        form = AuthorForm(request.POST, request.FILES, instance=author)

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
        form = AuthorForm(instance=author)

        context = {
            'form': form
        }

    return render(request, 'authors/edit.html', context)

def author_delete(request, pk):
    author = get_object_or_404(Autor, pk=pk)
    author.delete()

    messages.success(request, "¡Autor eliminado exitosamente!")

    return redirect('author_list')

""" LIBROS """
class BookListView(ListView):
    model = Libro
    template_name = 'books/index.html'
    paginate_by = 5
    # context_object_name = 'books'

    def get_context_data(self, **kwargs):
        books = Libro.objects.order_by('-id')
        context = super(BookListView, self).get_context_data(**kwargs)
        paginator = Paginator(books, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)

        context['books'] = books

        return context

class BookDetailView(DetailView):
    model = Libro
    template_name = 'books/show.html'

    def get_context_data(self, *args, **kwargs):
        book = Libro.objects.get(pk=self.kwargs['pk'])
        context = super(BookDetailView, self).get_context_data(*args, **kwargs)

        copies = Ejemplar.objects.filter(libro__pk=book.pk).order_by('estado')

        context["copies"] = copies
        context["copy_by_status"] = copies.values('estado').annotate(total=Count('estado'))

        return context

def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)

        if form.is_valid():
            book = form.save(commit=False)

            book.titulo = form.cleaned_data['titulo']
            book.autor = form.cleaned_data['autor']
            book.resumen = form.cleaned_data['resumen']
            book.isbn = form.cleaned_data['isbn']
            book.idioma = form.cleaned_data['idioma']
            book.image = form.cleaned_data['image']
            book.save()

            for gender in form.cleaned_data['genero']:
                book.genero.add(gender)

            messages.success(request, "¡Libro agregado exitosamente!")

            return redirect('book_list')
    else:
        form = BookForm()

    context = {
        'form': form
    }

    return render(request, 'books/create.html', context)

def book_update(request, pk):
    book = get_object_or_404(Libro, pk=pk)

    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)

        if form.is_valid():
            book = form.save(commit=False)

            book.titulo = form.cleaned_data['titulo']
            book.autor = form.cleaned_data['autor']
            book.resumen = form.cleaned_data['resumen']
            book.isbn = form.cleaned_data['isbn']
            book.idioma = form.cleaned_data['idioma']

            if len(request.FILES) != 0:
                book.image = form.cleaned_data['image']

            book.genero.clear()

            book.save()

            for gender in form.cleaned_data['genero']:
                book.genero.add(gender)

            messages.success(request, "¡Autor actualizado exitosamente!")

            return redirect('book_list')
        else:
            context = {
                'form': form
            }

            return render(request, 'books/edit.html', context)
    else:
        form = BookForm(instance=book)

        context = {
            'form': form
        }

    return render(request, 'books/edit.html', context)

def book_delete(request, pk):
    book = get_object_or_404(Libro, pk=pk)
    book.delete()

    messages.success(request, "¡Libro eliminado exitosamente!")

    return redirect('book_list')

""" EJEMPLARES """
class CopyListView(ListView):
    model = Ejemplar
    template_name = 'copies/index.html'
    paginate_by = 5
    # context_object_name = 'copies'

    def get_context_data(self, **kwargs):
        copies = Ejemplar.objects.order_by('-id')
        context = super(CopyListView, self).get_context_data(**kwargs)
        paginator = Paginator(copies, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            copies = paginator.page(page)
        except PageNotAnInteger:
            copies = paginator.page(1)
        except EmptyPage:
            copies = paginator.page(paginator.num_pages)

        context['copies'] = copies

        return context

class CopyDetailView(DetailView):
    model = Ejemplar
    template_name = 'copies/show.html'

    def get_context_data(self, *args, **kwargs):
        copy = Ejemplar.objects.get(pk=self.kwargs['pk'])
        context = super(CopyDetailView, self).get_context_data(*args, **kwargs)
        
        return context

def copy_create(request):
    if request.method == "POST":
        form = CopyForm(request.POST)

        if form.is_valid():
            copy = form.save(commit=False)

            copy.libro = form.cleaned_data['libro']
            copy.fechaDevolucion = form.cleaned_data['fechaDevolucion']
            copy.estado = form.cleaned_data['estado']
            
            copy.save()

            messages.success(request, "Ejemplar agregado exitosamente!")

            return redirect('copy_list')
    else:
        form = CopyForm()

    context = {
        'form': form
    }

    return render(request, 'copies/create.html', context)

def copy_update(request, pk):
    copy = get_object_or_404(Ejemplar, pk=pk)

    if request.method == "POST":
        form = CopyForm(request.POST, instance=copy)

        if form.is_valid():
            copy = form.save(commit=False)

            copy.libro = form.cleaned_data['libro']
            copy.fechaDevolucion = form.cleaned_data['fechaDevolucion']
            copy.estado = form.cleaned_data['estado']

            copy.save()

            messages.success(request, "¡Ejemplar actualizado exitosamente!")

            return redirect('copy_list')
        else:
            context = {
                'form': form
            }

            return render(request, 'copies/edit.html', context)
    else:
        form = CopyForm(instance=copy)

        context = {
            'form': form
        }

    return render(request, 'copies/edit.html', context)

def copy_delete(request, pk):
    copy = get_object_or_404(Ejemplar, pk=pk)
    copy.delete()

    messages.success(request, "¡Ejemplar eliminado exitosamente!")

    return redirect('copy_list')

""" GÉNEROS """
class GenderListView(ListView):
    model = Genero
    template_name = 'genders/index.html'
    paginate_by = 5
    # context_object_name = 'genders'

    def get_context_data(self, **kwargs):
        genders = Genero.objects.order_by('-id')
        context = super(GenderListView, self).get_context_data(**kwargs)
        paginator = Paginator(genders, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            genders = paginator.page(page)
        except PageNotAnInteger:
            genders = paginator.page(1)
        except EmptyPage:
            genders = paginator.page(paginator.num_pages)

        context['genders'] = genders

        return context

class GenderDetailView(DetailView):
    model = Genero
    template_name = 'genders/show.html'

    def get_context_data(self, *args, **kwargs):
        gender = Genero.objects.get(pk=self.kwargs['pk'])
        context = super(GenderDetailView, self).get_context_data(*args, **kwargs)
        
        return context

def gender_create(request):
    if request.method == "POST":
        form = GenderForm(request.POST)

        if form.is_valid():
            gender = form.save(commit=False)

            gender.nombre = form.cleaned_data['nombre']
            
            gender.save()

            messages.success(request, "¡Género agregado exitosamente!")

            return redirect('gender_list')
    else:
        form = GenderForm()

    context = {
        'form': form
    }

    return render(request, 'genders/create.html', context)

def gender_update(request, pk):
    gender = get_object_or_404(Genero, pk=pk)

    if request.method == "POST":
        form = GenderForm(request.POST, instance=gender)

        if form.is_valid():
            gender = form.save(commit=False)

            gender.nombre = form.cleaned_data['nombre']

            gender.save()

            messages.success(request, "¡Género actualizado exitosamente!")

            return redirect('gender_list')
        else:
            context = {
                'form': form
            }

            return render(request, 'genders/edit.html', context)
    else:
        form = GenderForm(instance=gender)

        context = {
            'form': form
        }

    return render(request, 'genders/edit.html', context)

def gender_delete(request, pk):
    gender = get_object_or_404(Genero, pk=pk)
    gender.delete()

    messages.success(request, "¡Género eliminado exitosamente!")

    return redirect('gender_list')

""" IDIOMAS """
class LanguageListView(ListView):
    model = Idioma
    template_name = 'languages/index.html'
    paginate_by = 5
    # context_object_name = 'languages'

    def get_context_data(self, **kwargs):
        languages = Idioma.objects.order_by('-id')
        context = super(LanguageListView, self).get_context_data(**kwargs)
        paginator = Paginator(languages, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            languages = paginator.page(page)
        except PageNotAnInteger:
            languages = paginator.page(1)
        except EmptyPage:
            languages = paginator.page(paginator.num_pages)

        context['languages'] = languages

        return context

class LanguageDetailView(DetailView):
    model = Idioma
    template_name = 'languages/show.html'

    def get_context_data(self, *args, **kwargs):
        language = Idioma.objects.get(pk=self.kwargs['pk'])
        context = super(LanguageDetailView, self).get_context_data(*args, **kwargs)
        
        return context

def language_create(request):
    if request.method == "POST":
        form = LanguageForm(request.POST)

        if form.is_valid():
            language = form.save(commit=False)

            language.nombre = form.cleaned_data['nombre']
            
            language.save()

            messages.success(request, "¡Idioma agregado exitosamente!")

            return redirect('language_list')
    else:
        form = LanguageForm()

    context = {
        'form': form
    }

    return render(request, 'languages/create.html', context)

def language_update(request, pk):
    language = get_object_or_404(Idioma, pk=pk)

    if request.method == "POST":
        form = LanguageForm(request.POST, instance=language)

        if form.is_valid():
            language = form.save(commit=False)

            language.nombre = form.cleaned_data['nombre']

            language.save()

            messages.success(request, "¡Idioma actualizado exitosamente!")

            return redirect('language_list')
        else:
            context = {
                'form': form
            }

            return render(request, 'languages/edit.html', context)
    else:
        form = LanguageForm(instance=language)

        context = {
            'form': form
        }

    return render(request, 'languages/edit.html', context)

def language_delete(request, pk):
    language = get_object_or_404(Idioma, pk=pk)
    language.delete()

    messages.success(request, "¡Idioma eliminado exitosamente!")

    return redirect('language_list')


# def idioma_list(request):
#     idiomas = Idioma.objects.all()

#     context = {
#         'idiomas': idiomas
#     }

#     return render(request, 'idioma_list.html', context)


# def idioma_new(request):
#     if request.method == "POST":
#         formulario = IdiomaForm(request.POST)

#         if formulario.is_valid():
#             idioma = formulario.save(commit=False)
#             idioma.nombre = formulario.cleaned_data['nombre']
#             idioma.save()

#             return redirect('idioma_list')
#     else:
#         formulario = IdiomaForm()

#     return render(request, 'idioma_new.html', {'formulario': formulario})


# def idioma_update(request, pk):
#     idioma = get_object_or_404(Idioma, pk=pk)

#     if request.method == "POST":
#         formulario = IdiomaForm(request.POST, instance=idioma)

#         if formulario.is_valid():
#             idioma = formulario.save(commit=False)
#             idioma.nombre = formulario.cleaned_data['nombre']
#             idioma.save()

#             return redirect('idioma_list')
#     else:
#         formulario = IdiomaForm(instance=idioma)

#     return render(request, 'idioma_new.html', {'formulario': formulario})


# def idioma_delete(request, pk):
#     idioma = get_object_or_404(Idioma, pk=pk)
#     idioma.delete()

#     return redirect('idioma_list')

def ChartData(request):
    chartLabel = "Préstamos"
    etiquetas = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
                 'Julio', 'Agosto', 'Setiembre', 'Octubre', 'Noviembre', 'Diciembre']
    meses = 12
    minimo = 10
    maximo = 100
    datos = []

    for i in range(meses):
        datos.append(randint(minimo, maximo))

    context = {
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
        lista = []

        for poi in pois:
            json_dict = {}
            json_dict['type'] = 'Feature'
            json_dict['properties'] = dict(name=poi.nombre)
            json_dict['geometry'] = dict(
                type='Point', coordinates=list([poi.lng, poi.lat]))
            lista.append(json_dict)

        context["markers"] = lista

        return context
