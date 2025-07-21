from django.test import TestCase

# Create your tests here.

from catalogo.models import Autor
#El nombre de la clase si puede ser arbitrario (catalogo.tests.test_models.PruebaDelModelo_Autor).
class PruebaDelModelo_Autor(TestCase):
    @classmethod
    def setUpTestData(cls):
        #Configurar objetos no modificados utilizados por todos los métodos de prueba
        Autor.objects.create(nombre='Big', apellido='Bob')

    def test_EtiquetaCampoNombre(self):
        autorini=Autor.objects.get(id=1)
        campoEtiqueta = autorini._meta.get_field('nombre').verbose_name
        self.assertEquals(campoEtiqueta,'nombre') #No entendí por qué aquí levanta el error, AssertionError: 'nombre' != 'Nombre' si lo comparo con 'Nombre'.
#Si es que va a colocar nombre y apellido alrevés, igual pasa si lo hago test con apellido. Averiguar.

    def test_EtiquetaParaCampoMuerte(self):
   #def pruebaDeLaEtiquetaMuerte(self): (Nombre de atributo método es "parcialmente" reservado: si el nombre del atributo-método no tiene el prefijo "test_", no ejecuta la prueba, solo dice que todo ok habiendo fallas y errores.

        #autorote=Autor.objects.get(id=1)
        #campoDeLaEtiqueta = autorote._meta.get_field('muerte').verbose_name
        #self.assertEquals(campoDeLaEtiqueta,'muerte')
        #Condensando las 3 proposiciones anteriores en una sola:
        self.assertEquals(Autor.objects.get(id=1)._meta.get_field('muerte').verbose_name, 'muerte')
        #Esta prueba detectará una falla porque la etiqueta que django pondrá en el formulario, será el nombre del campo "muerte" del modelo Autor, en mayúscula, "Muerte", y no "muerte".

    def test_maximaLongitudCampoNombre(self):
        autorito=Autor.objects.get(id=1)
        largoMaximo = autorito._meta.get_field('nombre').max_length
        self.assertEquals(largoMaximo,100)

    def test_nombreDelObjetoEsApellidoComaNombre(self):
        autorix=Autor.objects.get(id=1)
        excepcion_nombreObjeto = '%s, %s' % (autorix.apellido, autorix.nombre)
        self.assertEquals(excepcion_nombreObjeto,str(autorix))

    def test_obtenerUrlAbsoluta(self):
        autorene=Autor.objects.get(id=1)
        #Esto también fallará si la urlconf no está definida.
        self.assertEquals(autorene.get_absolute_url(),'/catalogo/autor/1')
