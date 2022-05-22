from django.contrib import admin
from blog.models import Posteo, Categoria, Comentario

# Register your models here.
class PosteoAdmin(admin.ModelAdmin):
    pass

class CategoriaAdmin(admin.ModelAdmin):
    pass

class ComentarioAdmin(admin.ModelAdmin):
    pass

admin.site.register(Posteo, PosteoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Comentario, ComentarioAdmin)