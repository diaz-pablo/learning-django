from django.shortcuts import render
from blog.models import Posteo, Comentario
from blog.forms import frmComentario

# Create your views here.
def blogIndex(request):
    posteos = Posteo.objects.all().order_by('-created_on')
    #todos los posteos ordenados x fecha de alta
    # aca hay manejo de modelo
    
    context = {
        'posteos' : posteos,
    }
    
    return render(request, 'blogIndex.html',context)
    # aca se manda datos del modelo a la vista (template)

def blogDetail(request, pk):
    posteo = Posteo.objects.get(pk=pk)
    # un posteo especifico

    formulario = frmComentario()

    if request.method == 'POST':
        formulario = frmComentario(request.POST)

        if formulario.is_valid():
            comentario = Comentario(
                autor = formulario.cleaned_data['autor'],
                body = formulario.cleaned_data['body'],
                posteo = posteo
            )

            comentario.save()

            formulario = frmComentario()

    comentarios = Comentario.objects.filter(posteo=posteo)
    # los comentarios del posteo filtrado
    countComment = comentarios.count()
    
    context = {
        'posteo':posteo,
        'comentarios':comentarios,
        'formulario':formulario,
        'countComment': countComment,
    }

    # aca tengo data de dos modelos
    return render(request, 'blogDetail.html', context)

