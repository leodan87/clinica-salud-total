from django.urls import path
from . import views

urlpatterns = [
    # Inicio
    path('', views.home, name='home'),

    # Especialidades
    path('especialidades/', views.especialidad_lista, name='especialidad_lista'),
    path('especialidades/nueva/', views.especialidad_crear, name='especialidad_crear'),
    path('especialidades/editar/<int:pk>/', views.especialidad_editar, name='especialidad_editar'),
    path('especialidades/eliminar/<int:pk>/', views.especialidad_eliminar, name='especialidad_eliminar'),

    # Doctores
    path('doctores/', views.doctor_lista, name='doctor_lista'),
    path('doctores/nuevo/', views.doctor_crear, name='doctor_crear'),
    path('doctores/editar/<int:pk>/', views.doctor_editar, name='doctor_editar'),
    path('doctores/eliminar/<int:pk>/', views.doctor_eliminar, name='doctor_eliminar'),

    # Pacientes
    path('pacientes/', views.paciente_lista, name='paciente_lista'),
    path('pacientes/nuevo/', views.paciente_crear, name='paciente_crear'),
    path('pacientes/editar/<int:pk>/', views.paciente_editar, name='paciente_editar'),
    path('pacientes/eliminar/<int:pk>/', views.paciente_eliminar, name='paciente_eliminar'),

    # Citas Médicas
    path('citas/', views.cita_lista, name='cita_lista'),
    path('citas/nueva/', views.cita_crear, name='cita_crear'),
    path('citas/editar/<int:pk>/', views.cita_editar, name='cita_editar'),
    path('citas/eliminar/<int:pk>/', views.cita_eliminar, name='cita_eliminar'),

    # Registro de usuario
    path('accounts/registro/', views.registro_usuario, name='registro'),
]
