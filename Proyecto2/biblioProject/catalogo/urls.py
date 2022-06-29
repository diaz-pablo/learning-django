from django.urls import path, include
from catalogo import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('autores/', views.AuthorListView.as_view(), name='author_list'),
    path('autor/crear', views.author_create, name='author_create'),
    path('autor/actualizar/<pk>', views.author_update, name='author_update'),
    path('autor/eliminar/<pk>', views.author_delete, name='author_delete'),
    path('autor/detalle/<pk>', views.AuthorDetailView.as_view(), name='author_details'),
    
    path('libros/', views.BookListView.as_view(), name='book_list'),
    path('libro/crear', views.book_create, name='book_create'),
    path('libro/actualizar/<pk>', views.book_update, name='book_update'),
    path('libro/eliminar/<pk>', views.book_delete, name='book_delete'),
    path('libro/detalle/<pk>', views.BookDetailView.as_view(), name='book_details'),

    path('ejemplares/', views.CopyListView.as_view(), name='copy_list'),
    path('ejemplar/crear', views.copy_create, name='copy_create'),
    path('ejemplar/actualizar/<pk>', views.copy_update, name='copy_update'),
    path('ejemplar/eliminar/<pk>', views.copy_delete, name='copy_delete'),
    path('ejemplar/detalle/<pk>', views.CopyDetailView.as_view(), name='copy_details'),
    
    path('ejemplares/', views.CopyListView.as_view(), name='copy_list'),
    path('ejemplar/crear', views.copy_create, name='copy_create'),
    path('ejemplar/actualizar/<pk>', views.copy_update, name='copy_update'),
    path('ejemplar/eliminar/<pk>', views.copy_delete, name='copy_delete'),
    path('ejemplar/detalle/<pk>', views.CopyDetailView.as_view(), name='copy_details'),
    
    path('generos/', views.GenderListView.as_view(), name='gender_list'),
    path('genero/crear', views.gender_create, name='gender_create'),
    path('genero/actualizar/<pk>', views.gender_update, name='gender_update'),
    path('genero/eliminar/<pk>', views.gender_delete, name='gender_delete'),
    path('genero/detalle/<pk>', views.GenderDetailView.as_view(), name='gender_details'),

    path('idiomas/', views.LanguageListView.as_view(), name='language_list'),
    path('idioma/crear', views.language_create, name='language_create'),
    path('idioma/actualizar/<pk>', views.language_update, name='language_update'),
    path('idioma/eliminar/<pk>', views.language_delete, name='language_delete'),
    path('idioma/detalle/<pk>', views.LanguageDetailView.as_view(), name='language_details'),

    path('charts/', views.ChartData, name='charts'),
    path('map/', views.POIsMapView.as_view(), name='map'),

    path('mis-prestamos/', views.MyLoansListView.as_view(), name='my_loans'),

    path('reportes/autor', views.AutorReport, name='reporte_autor'),

    path('accounts/register/', views.register, name="register"),
]
