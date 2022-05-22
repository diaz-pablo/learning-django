from django.urls import path
from blog import views

urlpatterns = [
    path('', views.blogIndex, name='blogIndex'),
    path('<int:pk>/', views.blogDetail, name='blogDetail'),
]