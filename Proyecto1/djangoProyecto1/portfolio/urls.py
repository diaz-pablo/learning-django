from django.urls import path
from portfolio import views

urlpatterns = [
    path('', views.projectIndex, name='projectIndex'),
    path('<int:pk>/', views.projectDetail, name='projectDetail'),
]