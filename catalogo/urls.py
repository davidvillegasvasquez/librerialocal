from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [path('', views.inicio, name='vistaHome'), path('libros/', views.LibroVistaLista.as_view(), name='todosLoslibros'), path('libros/conbarbara', views.LibroVistaListaConBarbara.as_view(), name='librosConBarbara'), path('libro/<int:pk>', views.VistaDetalleLibro.as_view(), name='detallesDeLibro'), path('autores/', views.VistaListaGenAutores.as_view(), name='toditicosLosAutores'), path('autor/<int:pk>', views.VistaDetalladaGenAutor.as_view(), name='autorDetalles'),]
#El parámetro name identifica de manera única este mapeador de URL particular. Lo localizamos en la plantilla base, base1.html. para enlazar a home (<a href="{% url 'index' %}">Home</a>).
#En la variable de url <int:pk>, el nombre de parámetro pk es un nombre arbitrario y no obligatorio.
#Este mapeador buscará automaticamente la plantilla libro_detail.html, y en su contexto, usará toda la información pasada a través de los atributos del modelo.
#El parámetro name para las vistas genéricas detalladas, deben ser las referenciadas con el nombre utilizadas en el retorno del atributo método, get_absolute_url (return reverse('nombreDelUrl', args=[str(self.id)])), del modelo en cuestión.
#Y se referencian en las plantillas por doble corchete sin uso de simbolo % (href={% url 'nombre' %}), ni la proposición url antes del nombre. Ej:
#href="{{ objetoNomArbitr.get_absolute_url }}", dónde objetoNomArbitr es un identificador apuntador en la plantilla, a un objeto del modelo (clase), que tiene dicho método atributo .get_absolute_url.

