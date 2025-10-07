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

urlpatterns += [
    path('autor/crear/', views.CrearAutor.as_view(), name='crearautorini'),
    path('autor/<int:pk>/actualizar/', views.ActualizarAutor.as_view(), name='actualizarEsteAutor'), path('autor/<int:pk>/borrar/', views.BorrarAutor.as_view(), name='borrar-autor'),]
# Debemos usar pk como el nombre de nuestro valor de clave principal (primary key) capturado, ya que este es el nombre del parámetro esperado por las clases de vista de ediciones genéricas implementadas para ello.

urlpatterns += [
    path('libro/crear/', views.CrearLibro.as_view(), name='crearlibro'),
    path('libro/<int:pk>/actualizar/', views.ActualizarLibro.as_view(), name='actualizarLibro'), path('libro/<int:pk>/borrar/', views.BorrarLibro.as_view(), name='borrarlibro'),]
