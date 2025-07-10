from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime #for checking renewal date range.

class FormRenovDeLibros(forms.Form):
    """
    Este es el formulario no consolidado (el que se presenta por primera vez). Se usa principalmente para limpiar y validar la fecha de renovación introducida por el usuario.
    """
    renovacionFecha = forms.DateField(help_text="Introduzca una fecha entre ahora y 4 semanas (normal 3).")

    def clean_renovacionFecha(self):
        fecha = self.cleaned_data['renovacionFecha']
        #Ojo: este método debe tener el nombre reservado clean_identificadorDelCampoDelFormularioAlimpiar, en este caso, clean_renovacionFecha, de lo contrario no validará nada.
        #Check date is not in past.
        if fecha < datetime.date.today():
            raise ValidationError(_('Fecha inválida - renovación al pasado'))

        #Check date is in range librarian allowed to change (+4 weeks).
        if fecha > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Fecha inválida - renovación más allá de las 4 semanas'))

        # Remember to always return the cleaned fecha.
        return fecha
