"""
urls.py - Configuracion de rutas URL de la aplicacion 'gestion'.

Cada path() conecta una URL del navegador con una vista (funcion en views.py).
Estructura de path():
    path('ruta/', vista, name='nombre_para_templates')

- 'ruta/': la URL que el usuario visita en el navegador
- vista: la funcion de views.py que maneja esa URL
- name: nombre unico usado en los templates con {% url 'nombre' %}

<int:pk> en las URLs captura un numero entero (la clave primaria/ID del registro)
y lo pasa como parametro a la vista. Ejemplo:
    /doctores/editar/3/ → llama a doctor_editar(request, pk=3)

Las operaciones CRUD tienen 4 URLs por cada modelo:
    /modelo/           → Lista (SELECT)
    /modelo/nuevo/     → Crear (INSERT)
    /modelo/editar/pk/ → Editar (UPDATE)
    /modelo/eliminar/pk/ → Eliminar logico (UPDATE activo=False)
"""

from django.urls import path
from . import views

urlpatterns = [
    # ─── Pagina principal (Dashboard) ─────────────────────────────────
    path('', views.home, name='home'),

    # ─── CRUD Especialidades ──────────────────────────────────────────
    path('especialidades/', views.especialidad_lista, name='especialidad_lista'),
    path('especialidades/nueva/', views.especialidad_crear, name='especialidad_crear'),
    path('especialidades/editar/<int:pk>/', views.especialidad_editar, name='especialidad_editar'),
    path('especialidades/eliminar/<int:pk>/', views.especialidad_eliminar, name='especialidad_eliminar'),

    # ─── CRUD Doctores ────────────────────────────────────────────────
    path('doctores/', views.doctor_lista, name='doctor_lista'),
    path('doctores/nuevo/', views.doctor_crear, name='doctor_crear'),
    path('doctores/editar/<int:pk>/', views.doctor_editar, name='doctor_editar'),
    path('doctores/eliminar/<int:pk>/', views.doctor_eliminar, name='doctor_eliminar'),

    # ─── CRUD Pacientes ───────────────────────────────────────────────
    path('pacientes/', views.paciente_lista, name='paciente_lista'),
    path('pacientes/nuevo/', views.paciente_crear, name='paciente_crear'),
    path('pacientes/editar/<int:pk>/', views.paciente_editar, name='paciente_editar'),
    path('pacientes/eliminar/<int:pk>/', views.paciente_eliminar, name='paciente_eliminar'),

    # ─── CRUD Citas Medicas ───────────────────────────────────────────
    path('citas/', views.cita_lista, name='cita_lista'),
    path('citas/nueva/', views.cita_crear, name='cita_crear'),
    path('citas/editar/<int:pk>/', views.cita_editar, name='cita_editar'),
    path('citas/eliminar/<int:pk>/', views.cita_eliminar, name='cita_eliminar'),

    # ─── Registro de nuevos usuarios ──────────────────────────────────
    path('accounts/registro/', views.registro_usuario, name='registro'),
]
