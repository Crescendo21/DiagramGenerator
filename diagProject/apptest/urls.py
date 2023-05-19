from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_diagram', views.create_diagram, name='create_diagram'),
    path('result', views.result, name='result'),  # Ajoutez cette ligne
]
