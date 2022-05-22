from django.contrib import admin
from catalogo.models import Idioma, Genero, Autor, Libro, Ejemplar

# Register your models here.
class IdiomaAdmin(admin.ModelAdmin):
    pass

class GeneroAdmin(admin.ModelAdmin):
    pass

class AutorAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'fechaNac', 'image', 'image_preview')
    list_filter = (('apellido', 'nombre'))

    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'muestra_genero', 'image', 'preview', 'image_preview')
    list_filter = (('titulo',))
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

class EjemplarAdmin(admin.ModelAdmin):
    list_display = ('fechaDevolucion', 'estado')

admin.site.register(Idioma, IdiomaAdmin)
admin.site.register(Genero, GeneroAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Ejemplar, EjemplarAdmin)