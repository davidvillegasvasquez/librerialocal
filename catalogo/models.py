from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.

class Genero(models.Model):
    """
    Modelo que representa un género literario (p. ej. ciencia ficción, poesía, etc.).
    """
    nombre = models.CharField(max_length=200, help_text="Ingrese el nombre del género (p. ej. Ciencia Ficción, Poesía Francesa etc.)")

    def __str__(self):
        """
        Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)
        """
        return self.nombre

from django.urls import reverse #Used to generate URLs by reversing the URL patterns

class Libro(models.Model):
    """
    Modelo que representa un libro (pero no un Ejemplar específico).
    """
    titulo = models.CharField(max_length=200)
    autor = models.ForeignKey('Autor', on_delete=models.SET_NULL, null=True)
    # ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
    # 'Autor' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.
    descripcion = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")
    isbn = models.CharField('ISBN',max_length=13, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genero = models.ManyToManyField(Genero, help_text="Seleccione un genero para este libro")
    # ManyToManyField, porque un género puede contener muchos libros y un libro puede cubrir varios géneros.
    # La clase Genre ya ha sido definida, entonces podemos especificar el objeto arriba.
    lenguaje = models.ForeignKey('Lenguaje', on_delete=models.SET_NULL, null=True)
    # ForeignKey, ya que un libro está escrito en un solo lenguaje, pero el mismo lenguaje puede haberse utilizado para escribir muchos otros libros.
    def __str__(self):
        """
        String que representa al objeto Book
        """
        return self.titulo

    def get_absolute_url(self):
        """
        Devuelve el URL a una instancia particular de Book
        """
        return reverse('detallesDeLibro', args=[str(self.id)])#Para las vistas detalladas que requieren el id de una instancia de este modelo como parámetro en la url, el parámetro name de la función path en el mapeador urls.py debe tener este #nombre ('detallesDeLibro') de url respectivo a dicha vista detallada genérica, de lo contrario se presentará la excepción: Reverse for 'detallesDeLibro' not found. 'libroDetalles' is not a valid view function or pattern name.
    class Meta:
        ordering = ['titulo', 'autor']

    def mostrar_genero(self):
    #Creates a string for tre in Admin.
        return ', '.join([ genero.nombre for genero in self.genero.all()[:3] ]) 

    mostrar_genero.short_description = 'Genero'

import uuid # Requerida para las instancias de libros únicos
from django.core.validators import MaxValueValidator, MinValueValidator 

class LibroInstancia(models.Model):
    """
    Modelo que representa una copia específica de un libro (i.e. que puede ser prestado por la biblioteca).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")
    libro = models.ForeignKey('Libro', on_delete=models.SET_NULL, null=True)
    imprenta = models.CharField(max_length=200)
    debidoderegresar = models.DateField(null=True, blank=True)
    prestatario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    PRESTAMO_STATUS = (
        ('m', 'Mantenimieno'),
        ('p', 'En prestamo'),
        ('d', 'Disponible'),
        ('r', 'Reservado'),
    )

    estatus = models.CharField(max_length=1, choices=PRESTAMO_STATUS, blank=True, default='m', help_text='Disponibilidad del libro')

    class Meta:
        ordering = ["debidoderegresar"] #ordering es un apuntador-identificador de palabra reservada de django para esta clase, no puedo usar el nombre "ordenar".
        permissions = (("puedeMarcarRetornado", "Colocar libro como retornado"),)

    @property
    def estaVencido(self):
        if self.debidoderegresar and date.today() > self.debidoderegresar:
            return True
        return False

    def __str__(self):
        """
        String para representar el Objeto del Modelo
        """
        #return '%s (%s)' % (self.id,self.libro.titulo)
        return f'{self.id} ({self.libro.titulo})' #Usando el formateo de cadena a partir de python 3.6

class Autor(models.Model):
    """
    Modelo que representa un autor
    """
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    nacimiento = models.DateField(null=True, blank=True)
    muerte = models.DateField('Muerte', null=True, blank=True)

    def get_absolute_url(self):
        """
        Retorna la url para acceder a una instancia particular de un autor.
        """
        return reverse('autorDetalles', args=[str(self.id)]) 

    def __str__(self):
        """
        String para representar el Objeto Modelo
        """
        return '%s, %s' % (self.apellido, self.nombre)

    class Meta:
        ordering = ['apellido']

class Lenguaje(models.Model):
    """
    Modelo que representa el lenguaje
    """
    nombre = models.CharField(max_length=100)

    def __str__(self):
        """
        String que representa al objeto Lenguaje
        """
        return self.nombre