from django.shortcuts import render
from .models import Libro, Autor, LibroInstancia, Genero

# Create your views here.
def inicio(solicitud):
    """
    Función vista para la página inicio del sitio.
    """
    # Genera contadores de algunos de los objetos principales
    num_libros=Libro.objects.all().count()
    #num_instancias=LibroInstancia.objects.count() # El 'all()' esta implícito por defecto.
    #Libros disponibles (status = 'd')
    num_instan_disponi=LibroInstancia.objects.filter(estatus__exact='d').count()
    num_autores=Autor.objects.count()  

    # Renderiza la plantilla HTML inicio.html con los datos en la variable contexto
    return render(solicitud,'base1-inicio.html',context={'cant_libros':num_libros,'cant_instancias':LibroInstancia.objects.count(), 'cant_inst_dispon':num_instan_disponi,'cant_autores':num_autores, 'cant_generos':Genero.objects.count()})
#Recuerde que podemos colocar el retorno del atributo objects.count() directamente en el valor de la clave del par clave-valor en el diccionario.

from django.views import generic

class LibroVistaLista(generic.ListView):
    model = Libro
    context_object_name = 'mi_listaDeLibros'#Atributo opcional: si no lo uso, la variable de contexto del objeto en la plantilla para esta vista, será automáticamente libro_list, es decir, nombreDelModeloEnMinuscula_list.
    template_name = 'catalogo/todosLosLibros.html' #Atributo opcional. En caso de usar solamente una clase, el nombre por defecto de su plantilla única será:
#nombreDelModeloEnMinuscula_list.html (obligatorio el complemento _list), si no especifíco su atributo template_name. Esto es importante si voy a usar varias vistas de clase con un mismo modelo.

    paginate_by = 2 #Paginación en grupo de dos objetos libro.
    
class LibroVistaListaConBarbara(generic.ListView):
    model = Libro
    context_object_name = 'listaDeLibrosConBarbara'
    template_name = 'catalogo/librosConBarbara.html'
    queryset = Libro.objects.filter(titulo__icontains='barbara')

class VistaDetalleLibro(generic.DetailView):
    model = Libro #Como las listas genericas, los demás atributos son opcionales. Aquí usaremos los atributos por defectos que nos proporciona django(automáticos).
    #template_name = 'catalogo/libroDetalle.html' #Podemos usar también como en listas genéricas, nombres arbitrarios para la plantilla, si no queremos usar los automáticos de django (nombreDelModelo_detail.html).

class VistaListaGenAutores(generic.ListView):
    model = Autor
    paginate_by = 2

class VistaDetalladaGenAutor(generic.DetailView):
    model = Autor 