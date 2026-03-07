from django.contrib import admin
from .models import Especialidad, Doctor, Paciente, CitaMedica


@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion', 'usuario', 'activo']
    list_filter = ['activo', 'usuario']
    search_fields = ['nombre']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['cedula', 'nombre', 'apellido', 'especialidad', 'telefono', 'usuario', 'activo']
    list_filter = ['activo', 'especialidad', 'usuario']
    search_fields = ['nombre', 'apellido', 'cedula']


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ['cedula', 'nombre', 'apellido', 'telefono', 'fecha_nacimiento', 'usuario', 'activo']
    list_filter = ['activo', 'usuario']
    search_fields = ['nombre', 'apellido', 'cedula']


@admin.register(CitaMedica)
class CitaMedicaAdmin(admin.ModelAdmin):
    list_display = ['fecha', 'hora', 'paciente', 'doctor', 'estado', 'usuario', 'activo']
    list_filter = ['activo', 'estado', 'fecha', 'usuario']
    search_fields = ['paciente__nombre', 'doctor__nombre']
