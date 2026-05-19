from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import (
    HabitoBooleano,
    HabitoContador,
    HabitoSemanal,
    Registro
)

# ======================================
# FORM HABITO BOOLEANO
# ======================================

class HabitoBooleanoForm(forms.ModelForm):

    class Meta:
        model = HabitoBooleano

        fields = [
            'nombre',
            'descripcion',
            'fecha_inicio',
            'activo'
        ]


# ======================================
# FORM HABITO CONTADOR
# ======================================

class HabitoContadorForm(forms.ModelForm):

    class Meta:
        model = HabitoContador

        fields = [
            'nombre',
            'descripcion',
            'fecha_inicio',
            'activo',
            'objetivo_diario'
        ]


# ======================================
# FORM HABITO SEMANAL
# ======================================

class HabitoSemanalForm(forms.ModelForm):

    class Meta:
        model = HabitoSemanal

        fields = [
            'nombre',
            'descripcion',
            'fecha_inicio',
            'activo',
            'objetivo_semanal'
        ]


# ======================================
# FORM REGISTRO
# ======================================

class RegistroForm(forms.ModelForm):

    class Meta:
        model = Registro

        fields = [
            'fecha',
            'cumplido',
            'valor',
            'notas'
        ]


class RegistroUsuarioForm(UserCreationForm):

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2'
        ]
        
class ImportarJSONForm(forms.Form):

    archivo = forms.FileField()