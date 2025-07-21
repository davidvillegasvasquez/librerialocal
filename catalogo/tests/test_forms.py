from django.test import TestCase

# Create your tests here.

import datetime
from django.utils import timezone
from catalogo.forms import ModeloFormRenovDeLibros

class PruebaFormulario_RenovDeLibros(TestCase):

    def test_renew_form_date_field_label(self):
        form = ModeloFormRenovDeLibros()
        self.assertTrue(form.fields['debidoderegresar'].label == None or form.fields['debidoderegresar'].label == 'Fecha de renovación')

    def test_renew_form_date_field_help_text(self):
        form = ModeloFormRenovDeLibros()
        self.assertEqual(form.fields['debidoderegresar'].help_text,'Ingrese una fecha entre ahora y 4 semanas arriba (lo normal son 3).') #Arrojará falla porque en forms.py está como "Introduzca una fecha entre ahora y 4 semanas arriba (lo normal son 3)."

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form_data = {'debidoderegresar': date}
        form = ModeloFormRenovDeLibros(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form_data = {'debidoderegresar': date}
        form = ModeloFormRenovDeLibros(data=form_data)
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form_data = {'debidoderegresar': date}
        form = ModeloFormRenovDeLibros(data=form_data)
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.now() + datetime.timedelta(weeks=4)
        form_data = {'debidoderegresar': date}
        form = ModeloFormRenovDeLibros(data=form_data)
        self.assertTrue(form.is_valid())
