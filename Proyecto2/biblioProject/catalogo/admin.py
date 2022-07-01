from django.contrib import admin
from catalogo.models import Idioma, Genero, Autor, Libro, Ejemplar, CustomUser

# Register your models here.
class IdiomaAdmin(admin.ModelAdmin):
    pass

class GeneroAdmin(admin.ModelAdmin):
    pass

class AutorAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'fechaNac', 'image', 'image_preview')
    list_filter = (('apellido', 'nombre'))
    list_per_page = 5

    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'muestra_genero', 'image', 'image_preview')
    list_filter = (('titulo',))
    readonly_fields = ('image_preview',) # Muestra en el add la imagen (solo lectura)
    list_per_page = 5

    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

class EjemplarAdmin(admin.ModelAdmin):
    list_display = ('libro', 'fechaDevolucion', 'estado', 'usuario')
    list_per_page = 10
    # search_fields = ('libro', )

# class POIAdmin(admin.ModelAdmin):
#     list_display = ('nombre', 'lng', 'lat')
#     list_per_page = 5

admin.site.register(CustomUser)
admin.site.register(Idioma, IdiomaAdmin)
admin.site.register(Genero, GeneroAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Ejemplar, EjemplarAdmin)
# admin.site.register(POI, POIAdmin)