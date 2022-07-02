from multiprocessing import context
from this import d
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from catalogo.models import Idioma, Genero, Libro, Ejemplar, Autor, CustomUser
from django.db.models import Count
from django.views import generic
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib import messages
from catalogo.forms import AuthorForm, BookForm, CopyForm, GenderForm, LanguageForm, CustomUserCreationForm
from random import randint
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth import authenticate, login
import calendar
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.pagesizes import A4
from datetime import date
from django.core import serializers

def register(request):
    context = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print(form)
            user = form.save()

            group = Group.objects.get(name='Partners')
            user.groups.add(group)

            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)

            return redirect('index')

        context['form'] = form

    return render(request, 'registration/register.html', context)

@login_required
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
class AuthorListView(PermissionRequiredMixin, generic.ListView):
    model = Autor
    context_object_name = 'authors'
    paginate_by = 5
    permission_required = 'catalogo.view_autor'

    queryset = Autor.objects.order_by('-id')
    template_name = 'authors/index.html'

class AuthorDetailView(PermissionRequiredMixin, generic.DetailView):
    model = Autor
    template_name = 'authors/show.html'
    permission_required = 'catalogo.view_autor'

    def autor_detail_view(request, pk):
        try:
            autor = Autor.objects.get(pk=pk)
        except Autor.DoesNotExist:
            raise Http404("Oops! El Autor no existe")

        context = {
            'autor': autor,
        }

        return render(request, 'authors/show.html', context)

@login_required
@permission_required('catalogo.add_autor')
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

@login_required
@permission_required('catalogo.change_autor')
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

@login_required
@permission_required('catalogo.delete_autor')
def author_delete(request, pk):
    author = get_object_or_404(Autor, pk=pk)
    author.delete()

    messages.success(request, "¡Autor eliminado exitosamente!")

    return redirect('author_list')

""" LIBROS """
class BookListView(PermissionRequiredMixin, ListView):
    model = Libro
    template_name = 'books/index.html'
    paginate_by = 5
    # context_object_name = 'books'
    permission_required = 'catalogo.view_libro'

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

class BookDetailView(PermissionRequiredMixin, DetailView):
    model = Libro
    template_name = 'books/show.html'
    permission_required = 'catalogo.view_libro'

    def get_context_data(self, *args, **kwargs):
        book = Libro.objects.get(pk=self.kwargs['pk'])
        context = super(BookDetailView, self).get_context_data(*args, **kwargs)

        copies = Ejemplar.objects.filter(libro__pk=book.pk).order_by('estado')

        context["copies"] = copies
        context["copy_by_status"] = copies.values('estado').annotate(total=Count('estado'))

        return context

@login_required
@permission_required('catalogo.add_libro')
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

@login_required
@permission_required('catalogo.change_libro')
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

@login_required
@permission_required('catalogo.delete_libro')
def book_delete(request, pk):
    book = get_object_or_404(Libro, pk=pk)
    book.delete()

    messages.success(request, "¡Libro eliminado exitosamente!")

    return redirect('book_list')

""" EJEMPLARES """
class CopyListView(PermissionRequiredMixin, ListView):
    model = Ejemplar
    template_name = 'copies/index.html'
    paginate_by = 5
    # context_object_name = 'copies'
    permission_required = 'catalogo.view_ejemplar'

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

class CopyDetailView(PermissionRequiredMixin, DetailView):
    model = Ejemplar
    template_name = 'copies/show.html'
    permission_required = 'catalogo.view_ejemplar'

    def get_context_data(self, *args, **kwargs):
        copy = Ejemplar.objects.get(pk=self.kwargs['pk'])
        context = super(CopyDetailView, self).get_context_data(*args, **kwargs)
        
        return context

@login_required
@permission_required('catalogo.add_ejemplar')
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

@login_required
@permission_required('catalogo.change_ejemplar')
def copy_update(request, pk):
    copy = get_object_or_404(Ejemplar, pk=pk)

    if request.method == "POST":
        form = CopyForm(request.POST, instance=copy)

        if form.is_valid():
            copy = form.save(commit=False)

            copy.libro = form.cleaned_data['libro']
            copy.fechaDevolucion = form.cleaned_data['fechaDevolucion']
            copy.estado = form.cleaned_data['estado']
            copy.usuario = form.cleaned_data['usuario']

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

@login_required
@permission_required('catalogo.delete_ejemplar')
def copy_delete(request, pk):
    copy = get_object_or_404(Ejemplar, pk=pk)
    copy.delete()

    messages.success(request, "¡Ejemplar eliminado exitosamente!")

    return redirect('copy_list')

""" GÉNEROS """
class GenderListView(PermissionRequiredMixin, ListView):
    model = Genero
    template_name = 'genders/index.html'
    paginate_by = 5
    # context_object_name = 'genders'
    permission_required = 'catalogo.view_genero'

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

class GenderDetailView(PermissionRequiredMixin, DetailView):
    model = Genero
    template_name = 'genders/show.html'
    permission_required = 'catalogo.view_genero'

    def get_context_data(self, *args, **kwargs):
        gender = Genero.objects.get(pk=self.kwargs['pk'])
        context = super(GenderDetailView, self).get_context_data(*args, **kwargs)
        
        return context

@login_required
@permission_required('catalogo.add_genero')
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

@login_required
@permission_required('catalogo.change_genero')
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

@login_required
@permission_required('catalogo.delete_genero')
def gender_delete(request, pk):
    gender = get_object_or_404(Genero, pk=pk)
    gender.delete()

    messages.success(request, "¡Género eliminado exitosamente!")

    return redirect('gender_list')

""" IDIOMAS """
class LanguageListView(PermissionRequiredMixin, ListView):
    model = Idioma
    template_name = 'languages/index.html'
    paginate_by = 5
    # context_object_name = 'languages'
    permission_required = 'catalogo.view_idioma'

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

class LanguageDetailView(PermissionRequiredMixin, DetailView):
    model = Idioma
    template_name = 'languages/show.html'
    permission_required = 'catalogo.view_idioma'

    def get_context_data(self, *args, **kwargs):
        language = Idioma.objects.get(pk=self.kwargs['pk'])
        context = super(LanguageDetailView, self).get_context_data(*args, **kwargs)
        
        return context

@login_required
@permission_required('catalogo.add_idioma')
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

@login_required
@permission_required('catalogo.change_idioma')
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

@login_required
@permission_required('catalogo.delete_idioma')
def language_delete(request, pk):
    language = get_object_or_404(Idioma, pk=pk)
    language.delete()

    messages.success(request, "¡Idioma eliminado exitosamente!")

    return redirect('language_list')

# @register.filter
def get_month_name(month_number):
    months = [None, 'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Setiembre', 'Octubre', 'Noviembre', 'Diciembre']
    return months[month_number]

def get_color(index):
    colors = ['#FDCA40', '#254D32', '#181D27', '#A0CCDA', '#9CFFD9', '#947EB0', '#808D8E', '#25283D', '#632A50', '#4392F1', '#DC493A', '#F78154']

    return colors[index]

@login_required
def ChartData(request):
    # Obtenemos los meses    
    months = Ejemplar.objects.order_by('fechaDevolucion').dates('fechaDevolucion', 'month')
    
    # Ejemplares reservados con fecha de devolucion seteada ordenados por la fecha de devolucion
    prestados = Ejemplar.objects.filter(estado__iexact='p')
    conFechaDeDevolucion = prestados.filter(fechaDevolucion__isnull=False)
    ordenados = conFechaDeDevolucion.order_by('fechaDevolucion')

    etiquetas = []
    datos = []
    colors = []
    for m in months:
        etiquetas.append(get_month_name(m.month))
        datos.append(ordenados.filter(fechaDevolucion__month=m.month).count())
        colors.append(get_color(m.month))

    chartLabel = "Préstamos"
    
    context = {
        "labels": etiquetas,
        "chartLabel": chartLabel,
        "data": datos,
        "colors": colors
    }

    return render(request, 'charts.html', context)

class POIsMapView(LoginRequiredMixin, TemplateView):
    """POIS and map view."""

    template_name = "map.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # pois = POI.objects.all()
        pois = CustomUser.objects.filter(groups__name='Partners')
        lista = []

        for poi in pois:
            json_dict = {}
            json_dict['type'] = 'Feature'
            json_dict['properties'] = dict(name=poi.username)
            json_dict['geometry'] = dict(
                type='Point', coordinates=list([poi.longitude, poi.latitude]))
            lista.append(json_dict)

        context["markers"] = lista

        return context

class MyLoansListView(PermissionRequiredMixin, generic.ListView):
    model = Ejemplar
    paginate_by = 5
    context_object_name = 'my_loans'
    template_name ='my_loans/index.html'
    permission_required = 'catalogo.can_view_my_loans'

    def get_queryset(self):
        return Ejemplar.objects.filter(usuario=self.request.user).filter(estado__exact='p').order_by('fechaDevolucion')



def AutorReport(request):
    today = date.today().strftime('%Y-%m-%d')
    buffer = io.BytesIO()
    report = canvas.Canvas(buffer, pagesize=A4)
    data = Autor.objects.all()
    report.setFont('Helvetica', 15, leading=None)
    report.setFillColorRGB(0.30,0.45,0.25)
    report.drawString(260,800,'Catalogo:: Autores')
    report.line(0,780,1000,780)
    x1=0
    y1=750
    counter = 0

    object_list= serializers.serialize("python", data)

    for object in object_list:
        counter= counter + 1
        for field_name, field_value in object['fields'].items():
            if counter==1:
                report.setFont("Helvetica",12,leading=None)
                report.drawString(x1+100,y1,field_name)
                report.line(0,880,1000,780)
            else:
                report.setFont("Helvetica",11,leading=None)
                
                if field_name=='fechaNac' or field_name=='fechaDeceso':
                    if field_value!=None:
                        valor=str(field_value)
                    else:
                        valor=''
                    report.drawString(x1+100,y1, valor) 
                elif field_name=='image':
                    if field_value!='':
                        valor=f'http://localhost:8000/{field_value}'
                        report.drawImage(valor, x1+100, y1, 25, 25) 
                else:
                    valor=field_value
                    report.drawString(x1+100,y1, valor)

            x1 = x1 + 100

        y1 = y1 - 50
        x1=2

        if counter==1:
            for field_name, field_value in object['fields'].items():
                report.setFont("Helvetica",11,leading=None)
                
                if field_name=='fechaNac' or field_name=='fechaDeceso':
                    if field_value!=None:
                        valor=str(field_value)
                    else:
                        valor=''
                    report.drawString(x1+100,y1, valor) 
                elif field_name=='image':
                    if field_value!='':
                        valor=f'http://localhost:8000/{field_value}'
                        report.drawImage(valor, x1+100, y1, 25, 25) 
                else:
                    valor=field_value
                    report.drawString(x1+100,y1, valor)
                x1 = x1 + 100

            y1 = y1 - 50
            x1=2
        

    report.setTitle(f'DW2022: Reporte del {today}')
    report.showPage()
    report.save()
    buffer.seek(0)
    
    return FileResponse(buffer, as_attachment=True, filename="reporte.pdf")
