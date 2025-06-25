from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [path('', views.inicio, name='vistaHome'), path('libros/', views.LibroVistaLista.as_view(), name='todosLoslibros'), path('libros/conbarbara', views.LibroVistaListaConBarbara.as_view(), name='librosConBarbara'), path('libro/<int:pk>', views.VistaDetalleLibro.as_view(), name='detallesDeLibro'), path('autores/', views.VistaListaGenAutores.as_view(), name='toditicosLosAutores'), path('autor/<int:pk>', views.VistaDetalladaGenAutor.as_view(), name='autorDetalles'), path('reseteoContSesiones', views.borrarConteoVisitas, name='resetearVisitas'),]

urlpatterns += [
    path('Mislibrosalquilados/', views.ListaLibrosPrestadosAlUsuario.as_view(), name='misLibrosalquilados'),
]

urlpatterns += [
    path('TodosLosLibrosActualmenteAlquilados/', views.ListaDeLibrosPrestadosActualmente.as_view(), name='librosAlquiladosActualmente'),
]

#El parámetro name identifica de manera única este mapeador de URL particular. Lo localizamos en la plantilla base, base1.html. para enlazar a home (<a href="{% url 'index' %}">Home</a>).
#En la variable de url <int:pk>, el nombre de parámetro pk es un nombre arbitrario y no obligatorio.
#Este mapeador buscará automaticamente la plantilla libro_detail.html, y en su contexto, usará toda la información pasada a través de los atributos del modelo.
#El parámetro name para las vistas genéricas detalladas, deben ser las referenciadas con el nombre utilizadas en el retorno del atributo método, get_absolute_url (return reverse('nombreDelUrl', args=[str(self.id)])), del modelo en cuestión.
#Y se referencian en las plantillas por doble corchete sin uso de simbolo % (href={% url 'nombre' %}), ni la proposición url antes del nombre. Ej:
#href="{{ objetoNomArbitr.get_absolute_url }}", dónde objetoNomArbitr es un identificador apuntador en la plantilla, a un objeto del modelo (clase), que tiene dicho método atributo .get_absolute_url.
#Atención: duré como 3 horas tirando flecha para la vista de reiniciar el contador: si nó coloco un texto, así sea un sólo caracter en la url, y dejo las comillas vacias, se tomará 
#la url de la primera vista (views.inicio), con url '', y no se reiniciará ningún contador, porque no se llamará ninguna vista views.borrarConteoVisitas sino a views.inicio.
#Esto nos dice que diferentes nombres urls pueden referenciar la misma función si tienen igual cadena de url en el primer parámetro de la función path.
