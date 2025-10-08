from django.shortcuts import render, redirect
from .models import Libro, Autor, LibroInstancia, Genero
from django.urls import reverse

# Create your views here.
def borrarConteoVisitas(solicitudReset):
    """
    Ejemplo de como borrar conteo con la propiedad session
    """  
    solicitudReset.session['numeroDeVisitasAinicio'] = 0
    #solicitudReset.session.clear() #Da el mismo efecto de restablecer el contador, pero borra todos los demás parámetros de la sesión.
     
    return redirect('/') #Para usar con redirect y reverse. Es la mejor opción.
    #return render(solicitudReset,'base1-inicio.html',context={'cantVisitas':0})
    #Si se usa la función render, se perderá la visualización en otras variables de contexto a la primera sesión.
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
    # Numero de visitas a esta view, como está contado en la variable de sesión.
    numeroDeVisitas = solicitud.session.get('numeroDeVisitasAinicio', 0)#Como no está predefinida de arranque en el dict solicitud.session, le asignamos un nombre de identificador arbitrario (numeroDeVisitasAinicio) al contador de sesiones.
    #También recuerde que el identificador con nombre arbitrario (solicitud) es el nombre del parámetro que usamos en esta función, y pasa un objeto de la clase HttpRequest que tiene el atributo .session
    numeroDeVisitas += 1
    solicitud.session['numeroDeVisitasAinicio'] = numeroDeVisitas

    # Renderiza la plantilla HTML inicio.html con los datos en la variable contexto
    return render(solicitud,'base1-inicio.html',context={'cant_libros':num_libros,'cant_instancias':LibroInstancia.objects.count(), 'cant_inst_dispon':num_instan_disponi,'cant_autores':num_autores, 'cant_generos':Genero.objects.count(), 'cantVisitas':numeroDeVisitas})
#Recuerde que podemos colocar el retorno del atributo objects.count() directamente en el valor de la clave del par clave-valor en el diccionario.

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

class LibroVistaLista(generic.ListView): # ,LoginRequiredMixin):
    model = Libro
    context_object_name = 'mi_listaDeLibros'#Atributo opcional: si no lo uso, la variable de contexto del objeto en la plantilla para esta vista, será automáticamente libro_list, es decir, nombreDelModeloEnMinuscula_list.
    template_name = 'catalogo/todosLosLibros.html' #Atributo opcional. En caso de usar solamente una clase, el nombre por defecto de su plantilla única será:
#nombreDelModeloEnMinuscula_list.html (obligatorio el complemento _list), si no especifíco su atributo template_name. Esto es importante si voy a usar varias vistas de clase con un mismo modelo.

    #paginate_by = 2 #Paginación en grupo de dos objetos libro.

#Literal o constante, que simula un valor importado al módulo:
constante = 25
class LibroVistaListaConBarbara(generic.ListView):
    model = Libro
    context_object_name = 'listaDeLibrosConBarbara'
    template_name = 'catalogo/librosConBarbara.html'
    #Está claro que no haremos vistas genéricas para conseguir este tipo de queryset, si podemos hacer un filtrado a nivel de frontend con css y js, lo cual reduce la cantidad de computo en el backend, reduciendo el costo de alquiler en nuestro servidor.
    queryset = Libro.objects.filter(titulo__icontains='barbara')
    suma = 0
    #Un atributo método sobre un atributo del modelo (suma), que usaremos para la variable de contexto, 'variableDeContextoN': 
    def operSuma(self, num):
        self.suma = num + constante
        return self.suma
    
    #Podemos poner más variables de contexto en una vista genérica, sobreescribiendo el método get_context_data. Este es un ejemplo de como se sobreescriben los métodos implícitos (heredados de generic.ListView) de esta clase hecha por nosotros:
    def get_context_data(self, **kwargs):
        # Llame primero a la implementación base para obtener un contexto.
        context = super(LibroVistaListaConBarbara, self).get_context_data(**kwargs)
        #Agregamos al diccionario context:
        context['una2daVariableDeContexto'] = 'Sólo una cadena. Puede ser cualquier otro tipo de valor.'
        context['variableDeContextoN'] = self.operSuma(1000)
        return context

class VistaDetalleLibro(generic.DetailView):
    model = Libro #Como las listas genericas, los demás atributos son opcionales. Aquí usaremos los atributos por defectos que nos proporciona django(automáticos, implicitos).
    #template_name = 'catalogo/libroDetalle.html' #Podemos usar también como en listas genéricas, nombres arbitrarios para la plantilla, si no queremos usar los automáticos de django (nombreDelModelo_detail.html).

class VistaListaGenAutores(generic.ListView):
    model = Autor
    #Si usamos listas o tablas no podemos paginar:
    #paginate_by = 2

class VistaDetalladaGenAutor(generic.DetailView):
    model = Autor 

class ListaLibrosPrestadosAlUsuario(LoginRequiredMixin, generic.ListView):
    """
    Vista genérica basada en clases que enumera los libros prestados al usuario actual.
    """
    model = LibroInstancia
    template_name ='catalogo/listaInstanciasDeLibrosPrestadasAlUsuario.html'
    paginate_by = 2

    def get_queryset(self):
        return LibroInstancia.objects.filter(prestatario=self.request.user).filter(estatus__exact='p').order_by('debidoderegresar')

from django.contrib.auth.mixins import PermissionRequiredMixin

class ListaDeLibrosPrestadosActualmente(PermissionRequiredMixin, generic.ListView):
    """
    Vista tipo lista genérica basada en clases que enumera todos los libros prestados actualmente, y que sólo puede ser mostrado si el usuario pertenece al grupo de bibliotecarios.
    """
    permission_required = ('catalogo.puedeMarcarRetornado',)#Puede ser una tupla con n permisos requeridos.
    model = LibroInstancia
    template_name ='catalogo/todosLosLibrosPrestadosActualmente.html'
    paginate_by = 2

    def get_queryset(self):
        return LibroInstancia.objects.filter(estatus__exact='p').order_by('debidoderegresar')

from django.contrib.auth.decorators import permission_required, login_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import datetime
from catalogo.forms import ModeloFormRenovDeLibros

#@login_required #Trabaja igual sin este decorador. Averiguar por qué?
@permission_required('catalogo.puedeMarcarRetornado')
def renovacionLibroPorLibrero(solicitud, claveprimaria):
    """
    View function for renewing a specific BookInstance by librarian
    """
    libroInstancia=get_object_or_404(LibroInstancia, pk = claveprimaria)

    # If this is a POST request then process the Form data
    if solicitud.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        formulario = ModeloFormRenovDeLibros(solicitud.POST)
        # Check if the form is valid:
        if formulario.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            libroInstancia.debidoderegresar= formulario.cleaned_data['debidoderegresar']
            libroInstancia.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('librosAlquiladosActualmente') )

    # If this is a GET (or any other method) create the default form.
    else:
        fechaDeRenovacionPropuesta = datetime.date.today() + datetime.timedelta(weeks=3)

        formulario = ModeloFormRenovDeLibros(initial={'debidoderegresar': fechaDeRenovacionPropuesta}) #Ojo: los nombres de variables de contexto deben coincidir con sus respectivos nombres de campo en la clase formulario creada, o no se visualizarán en la plantilla.

    return render(solicitud, 'catalogo/formularioRenovacion.html', {'formulario': formulario, 'instanciaDeLibro':libroInstancia})

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import logout

"""
Las vistas "create" y "update" utilizan la misma plantilla de forma predeterminada, que se nombrará después de su model: model_name_form.html. Lo más que puedes cambiar este nombre predeterminado por django, es el sufijo a algo diferente a _form usando el campo template_name_suffix en tu vista, ejemplo: template_name_suffix = '_other_suffix'. Aquí vamos a usar el método conservador de una sóla plantilla model_name_form.html para las vistas crear/actualizar, porque usamos el suffix y nos produjo un extraño duplicado de instancias en una ocasión.
"""
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

#Los dos decoradores @method_decorator para borrar caché de navegación y requerido de logeo, son inprescindibles para que un usuario no pueda acceder a los formularios post luego de darse de baja en su sesión.
@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class CrearAutor(CreateView):
    model = Autor
    fields = '__all__'
    initial={'muerte':'05/01/2018',}

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class ActualizarAutor(UpdateView):
    model = Autor
    fields = ['nombre','apellido','nacimiento','muerte']

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class BorrarAutor(DeleteView):
    model = Autor
    #Obviamente no necesitamos indicar los campos.
    success_url = reverse_lazy('toditicosLosAutores')

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class CrearLibro(CreateView):
    model = Libro
    fields = '__all__'

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class ActualizarLibro(UpdateView):
    model = Libro
    fields = '__all__'

@method_decorator(login_required, name='dispatch')
@method_decorator(never_cache, name='dispatch')
class BorrarLibro(DeleteView):
    model = Libro
    success_url = reverse_lazy('todosLoslibros')


