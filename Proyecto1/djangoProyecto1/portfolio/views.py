from django.shortcuts import render
from portfolio.models import Proyecto

# Create your views here.
def projectIndex(request):
    proyectos = Proyecto.objects.all()
    context = {
        'proyectos': proyectos
    }

    return render(request, 'projectIndex.html', context)

def projectDetail(request,pk):
    proyecto = Proyecto.objects.get(pk=pk)
    context = {
        'proyecto': proyecto
    }
    
    return render(request, 'projectDetail.html', context)