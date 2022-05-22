from django.urls import path
from helloDIUNSa import views

urlpatterns = [
    path('', views.helloDIUNSa, name='helloDIUNsa'),
]