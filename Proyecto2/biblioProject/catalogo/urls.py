from django.urls import path
from catalogo import views

urlpatterns = [
    path('', views.index, name='index'),
    path('libros/', views.LibroListView.as_view(), name='libros'),
    path('libro/<pk>', views.LibroDetailView.as_view(), name='libro'),
    path('autores/', views.AutorListView.as_view(), name='autores'),
    path('autor/<pk>', views.AutorDetailView.as_view(), name='autor'),
    path('ejemplar/<pk>', views.EjemplarDetailView.as_view(), name='ejemplar'),
    path('generos/', views.genero_list, name='genero_list'),
    path('genero/new/', views.genero_new, name='genero_new'),
    path('genero/update/<pk>', views.genero_update, name='genero_update'),
]
