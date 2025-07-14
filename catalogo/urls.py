from django.urls import path
from . import views
from django.contrib import admin #Aunque no se vé el uso del admin aquí, si no lo importo se presenta la excepción "LookupError: No installed app with label 'admin'".

urlpatterns = [path('', views.inicio, name='vistaHome'), path('libros/', views.LibroVistaLista.as_view(), name='todosLoslibros'), path('libros/conbarbara', views.LibroVistaListaConBarbara.as_view(), name='librosConBarbara'), path('libro/<int:pk>', views.VistaDetalleLibro.as_view(), name='detallesDeLibro'), path('autores/', views.VistaListaGenAutores.as_view(), name='toditicosLosAutores'), path('autor/<int:pk>', views.VistaDetalladaGenAutor.as_view(), name='autorDetalles'), path('reseteoContSesiones', views.borrarConteoVisitas, name='resetearVisitas'),]

urlpatterns += [
    path('LibrosEnManosDelUsuario/<str:username>', views.ListaLibrosPrestadosAlUsuario.as_view(), name='misLibrosalquilados'),
]
#Note la variable de url para url dinámica, <str:username>
urlpatterns += [
    path('TodosLosLibrosActualmenteAlquilados/', views.ListaDeLibrosPrestadosActualmente.as_view(), name='librosAlquiladosActualmente'),
]

urlpatterns += [
    path('libro/<uuid:claveprimaria>/renovacion/', views.renovacionLibroPorLibrero, name='renovDeLibroPorLibrero'),
]
#Nota: Podemos nombrar nuestros datos de URL capturados "claveprimaria" como queramos, porque tenemos un control completo sobre la función de vista (no
#estamos usando una clase de vista de detalles genérica que espere parámetros con un nombre determinado). sin embargo pk, abreviatura de "primary key", es una convención razonable de usar!
#Ojo: En <uuid:claveprimaria> del url, el nombre arbitrario "claveprimaria" que pareciera un parámetro real, comporta un nombre de parámetro que transportará el valor id de la instancia en cuestión, y que reconocerá la vista correspondiente.
#Por lo tanto, debe estar escrita igualmente en los parámetros formales de dicha función o clase de la respectiva vista.

urlpatterns += [
    path('autor/crear/', views.CrearAutor.as_view(), name='crearautorini'),
    path('autor/<int:pk>/actualizar/', views.ActualizarAutor.as_view(), name='actualizarEsteAutor'), path('autor/<int:pk>/borrar/', views.BorrarAutor.as_view(), name='borrar-autor'),]
# Debemos usar pk como el nombre de nuestro valor de clave principal (primary key) capturado, ya que este es el nombre del parámetro esperado por las clases de vista de ediciones genéricas implementadas para ello.
