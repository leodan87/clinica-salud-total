"""
forms.py - Definicion de los formularios de la aplicacion.

Los formularios en Django se encargan de:
1. Generar el HTML de los campos del formulario automaticamente
2. Validar los datos ingresados por el usuario
3. Guardar los datos validados en la base de datos

Usamos ModelForm: formularios que se generan automaticamente a partir
de los modelos (tablas). Django crea los campos del formulario basandose
en los campos del modelo.

Todos los widgets tienen la clase 'form-control' o 'form-select' de Bootstrap 5
para que los formularios se vean con estilos profesionales.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Especialidad, Doctor, Paciente, CitaMedica


# ─── FORMULARIO: ESPECIALIDAD ────────────────────────────────────────────────

class EspecialidadForm(forms.ModelForm):
    """
    Formulario para crear y editar especialidades.
    Solo incluye 'nombre' y 'descripcion' (el campo 'activo' se maneja internamente).
    """
    class Meta:
        model = Especialidad  # Modelo asociado al formulario
        fields = ['nombre', 'descripcion']  # Campos que aparecen en el formulario
        # widgets: personalizan como se renderiza cada campo en HTML
        # 'form-control' es una clase CSS de Bootstrap que estiliza los inputs
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ─── FORMULARIO: DOCTOR ──────────────────────────────────────────────────────

class DoctorForm(forms.ModelForm):
    """
    Formulario para crear y editar doctores.
    Filtra las especialidades para mostrar solo las activas en el <select>.
    """
    class Meta:
        model = Doctor
        fields = ['nombre', 'apellido', 'cedula', 'telefono', 'email', 'especialidad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            # EmailInput: genera un <input type="email"> que valida el formato
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # Select: genera un <select> (dropdown/desplegable)
            # 'form-select' es la clase CSS de Bootstrap para selects
            'especialidad': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Sobreescribimos __init__ para filtrar el queryset del campo especialidad.
        Solo muestra especialidades con activo=True en el desplegable.
        Si no hacemos esto, aparecerian tambien las especialidades eliminadas.
        """
        super().__init__(*args, **kwargs)
        self.fields['especialidad'].queryset = Especialidad.objects.filter(activo=True)


# ─── FORMULARIO: PACIENTE ────────────────────────────────────────────────────

class PacienteForm(forms.ModelForm):
    """
    Formulario para crear y editar pacientes.
    Incluye campo de fecha con selector de calendario HTML5.
    """
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'cedula', 'fecha_nacimiento', 'telefono', 'email', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            # DateInput con type='date': muestra un selector de fecha nativo del navegador
            'fecha_nacimiento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ─── FORMULARIO: CITA MEDICA ─────────────────────────────────────────────────

class CitaMedicaForm(forms.ModelForm):
    """
    Formulario para crear y editar citas medicas.
    Filtra pacientes y doctores para mostrar solo los activos en los <select>.
    """
    class Meta:
        model = CitaMedica
        fields = ['paciente', 'doctor', 'fecha', 'hora', 'motivo', 'diagnostico', 'estado']
        widgets = {
            # Desplegables para seleccionar paciente y doctor
            'paciente': forms.Select(attrs={'class': 'form-select'}),
            'doctor': forms.Select(attrs={'class': 'form-select'}),
            # Selectores nativos de fecha y hora del navegador
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'motivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # Estado: desplegable con las opciones definidas en ESTADO_CHOICES del modelo
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Filtra los querysets de paciente y doctor para mostrar
        solo registros activos (no eliminados) en los desplegables.
        """
        super().__init__(*args, **kwargs)
        self.fields['paciente'].queryset = Paciente.objects.filter(activo=True)
        self.fields['doctor'].queryset = Doctor.objects.filter(activo=True)


# ─── FORMULARIO: REGISTRO DE USUARIO ─────────────────────────────────────────

class RegistroUsuarioForm(UserCreationForm):
    """
    Formulario para registrar nuevos usuarios en el sistema.
    Extiende UserCreationForm de Django que ya incluye username, password1 y password2.
    Le agregamos el campo email y estilos de Bootstrap.
    """
    # Campo email adicional (UserCreationForm no lo incluye por defecto)
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User  # Usa el modelo User de Django (tabla auth_user)
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        """Agrega la clase CSS de Bootstrap a los campos heredados de UserCreationForm."""
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
