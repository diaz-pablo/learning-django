from django.urls import path
from catalogo import views

urlpatterns = [
    path('', views.index, name='index'),
    path('libros/', views.LibroListView.as_view(), name='libros'),
    path('libro/<pk>', views.LibroDetailView.as_view(), name='libro'),
    
    path('autores/', views.AutorListView.as_view(), name='autores'),
    path('autor/new', views.autor_new, name='autor_new'),
    path('autor/update/<pk>', views.autor_update, name='autor_update'),
    path('autor/<pk>', views.AutorDetailView.as_view(), name='autor'),
    
    path('ejemplar/<pk>', views.EjemplarDetailView.as_view(), name='ejemplar'),
    
    path('generos/', views.genero_list, name='genero_list'),
    path('genero/new/', views.genero_new, name='genero_new'),
    path('genero/update/<pk>', views.genero_update, name='genero_update'),
    
    path('idiomas/', views.idioma_list, name='idioma_list'),
    path('idioma/new/', views.idioma_new, name='idioma_new'),
    path('idioma/update/<pk>', views.idioma_update, name='idioma_update'),
    path('idioma/delete/<pk>', views.idioma_delete, name='idioma_delete'),

    path('ejemplares', views.ejemplar_list, name='ejemplar_list'),
    path('ejemplar/new/', views.ejemplar_new, name='ejemplar_new'),

    path('charts/', views.ChartData, name='charts'),
    path('map/', views.POIsMapView.as_view(), name='map'),
]
