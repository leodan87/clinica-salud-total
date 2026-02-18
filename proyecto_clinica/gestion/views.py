"""
views.py - Vistas (controladores) de la aplicacion.

Las vistas son funciones que reciben una peticion HTTP del navegador (request)
y devuelven una respuesta HTTP (generalmente una pagina HTML renderizada).

Operaciones CRUD implementadas:
- CREATE (Insertar): vistas *_crear  → formulario nuevo, guarda con form.save()
- READ   (Consultar): vistas *_lista → consulta registros con .filter(activo=True)
- UPDATE (Actualizar): vistas *_editar → carga datos existentes, guarda cambios
- DELETE (Eliminar logico): vistas *_eliminar → cambia activo=False (no borra de la BD)

Cada vista usa el decorador @login_required para que solo usuarios
autenticados puedan acceder al sistema.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Especialidad, Doctor, Paciente, CitaMedica
from .forms import (
    EspecialidadForm, DoctorForm, PacienteForm,
    CitaMedicaForm, RegistroUsuarioForm,
)


# ─── INICIO (DASHBOARD) ──────────────────────────────────────────────────────

@login_required  # Solo usuarios autenticados pueden ver el dashboard
def home(request):
    """
    Vista principal del sistema (Panel de Control).
    Cuenta los registros activos de cada tabla y los envia al template
    para mostrar las estadisticas en tarjetas.
    """
    contexto = {
        # .filter(activo=True) solo cuenta registros no eliminados
        # .count() ejecuta un SELECT COUNT(*) en la base de datos (eficiente)
        'total_pacientes': Paciente.objects.filter(activo=True).count(),
        'total_doctores': Doctor.objects.filter(activo=True).count(),
        'total_citas': CitaMedica.objects.filter(activo=True).count(),
        # Filtra citas que estan activas Y en estado 'Pendiente'
        'citas_pendientes': CitaMedica.objects.filter(activo=True, estado='Pendiente').count(),
        'total_especialidades': Especialidad.objects.filter(activo=True).count(),
    }
    # render() combina el template HTML con los datos del contexto
    return render(request, 'home.html', contexto)


# ─── REGISTRO DE USUARIO ─────────────────────────────────────────────────────

def registro_usuario(request):
    """
    Vista publica (sin @login_required) para que nuevos usuarios
    puedan crear una cuenta en el sistema.
    Usa el patron POST/GET comun en Django:
    - GET: muestra el formulario vacio
    - POST: procesa los datos enviados por el formulario
    """
    if request.method == 'POST':
        # Crea el formulario con los datos enviados por el usuario
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            # Guarda el nuevo usuario en la tabla auth_user de Django
            form.save()
            # Muestra un mensaje de exito al usuario
            messages.success(request, 'Cuenta creada exitosamente. Ahora puedes iniciar sesión.')
            # Redirige al login para que inicie sesion con su nueva cuenta
            return redirect('login')
    else:
        # Si es GET, crea un formulario vacio
        form = RegistroUsuarioForm()
    return render(request, 'registration/register.html', {'form': form})


# ═══════════════════════════════════════════════════════════════════════════════
# CRUD DE ESPECIALIDADES
# Patron: listar, crear, editar, eliminar (se repite para cada modelo)
# ═══════════════════════════════════════════════════════════════════════════════

@login_required
def especialidad_lista(request):
    """
    READ (Consultar): Lista todas las especialidades activas.
    Equivalente SQL: SELECT * FROM gestion_especialidad WHERE activo = TRUE
    """
    especialidades = Especialidad.objects.filter(activo=True)
    return render(request, 'gestion/especialidad_lista.html', {'especialidades': especialidades})


@login_required
def especialidad_crear(request):
    """
    CREATE (Insertar): Muestra un formulario vacio y guarda una nueva especialidad.
    - GET: muestra el formulario vacio
    - POST: valida los datos y ejecuta INSERT INTO en la base de datos
    """
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            # form.save() ejecuta INSERT INTO gestion_especialidad (nombre, descripcion, activo) VALUES (...)
            form.save()
            messages.success(request, 'Especialidad creada exitosamente.')
            # Redirige a la lista para ver el nuevo registro
            return redirect('especialidad_lista')
    else:
        form = EspecialidadForm()
    return render(request, 'gestion/especialidad_formulario.html', {
        'form': form, 'titulo': 'Nueva Especialidad'
    })


@login_required
def especialidad_editar(request, pk):
    """
    UPDATE (Actualizar): Carga una especialidad existente en el formulario y guarda los cambios.
    - pk: clave primaria (ID) de la especialidad a editar, viene de la URL
    - instance=especialidad: le dice al formulario que trabaje con ese registro existente
    """
    # get_object_or_404: busca el registro por pk y activo=True
    # Si no lo encuentra, muestra una pagina de error 404
    especialidad = get_object_or_404(Especialidad, pk=pk, activo=True)
    if request.method == 'POST':
        # instance=especialidad: actualiza el registro existente en vez de crear uno nuevo
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            # form.save() ejecuta UPDATE gestion_especialidad SET ... WHERE id = pk
            form.save()
            messages.success(request, 'Especialidad actualizada exitosamente.')
            return redirect('especialidad_lista')
    else:
        # Carga el formulario con los datos actuales de la especialidad
        form = EspecialidadForm(instance=especialidad)
    return render(request, 'gestion/especialidad_formulario.html', {
        'form': form, 'titulo': 'Editar Especialidad'
    })


@login_required
def especialidad_eliminar(request, pk):
    """
    DELETE (Eliminacion logica): No borra el registro de la BD,
    solo cambia activo=False para que no aparezca en las consultas.
    Equivalente SQL: UPDATE gestion_especialidad SET activo = FALSE WHERE id = pk
    """
    especialidad = get_object_or_404(Especialidad, pk=pk, activo=True)
    if request.method == 'POST':
        # ELIMINACION LOGICA: cambiamos activo a False en vez de borrar
        especialidad.activo = False
        especialidad.save()
        messages.success(request, 'Especialidad eliminada exitosamente.')
        return redirect('especialidad_lista')
    # Si es GET, muestra la pagina de confirmacion ("¿Esta seguro de eliminar?")
    return render(request, 'gestion/confirmar_eliminacion.html', {
        'objeto': especialidad, 'tipo': 'especialidad', 'lista_url': 'especialidad_lista'
    })


# ═══════════════════════════════════════════════════════════════════════════════
# CRUD DE DOCTORES
# Mismo patron que Especialidades pero con select_related para optimizar
# ═══════════════════════════════════════════════════════════════════════════════

@login_required
def doctor_lista(request):
    """
    READ: Lista doctores activos.
    select_related('especialidad') hace un JOIN con la tabla de especialidades
    para traer todo en una sola consulta SQL (optimizacion de rendimiento).
    Sin select_related, Django haria una consulta extra por cada doctor.
    """
    doctores = Doctor.objects.filter(activo=True).select_related('especialidad')
    return render(request, 'gestion/doctor_lista.html', {'doctores': doctores})


@login_required
def doctor_crear(request):
    """CREATE: Registra un nuevo doctor en el sistema."""
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor registrado exitosamente.')
            return redirect('doctor_lista')
    else:
        form = DoctorForm()
    return render(request, 'gestion/doctor_formulario.html', {
        'form': form, 'titulo': 'Nuevo Doctor'
    })


@login_required
def doctor_editar(request, pk):
    """UPDATE: Edita los datos de un doctor existente."""
    doctor = get_object_or_404(Doctor, pk=pk, activo=True)
    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor actualizado exitosamente.')
            return redirect('doctor_lista')
    else:
        form = DoctorForm(instance=doctor)
    return render(request, 'gestion/doctor_formulario.html', {
        'form': form, 'titulo': 'Editar Doctor'
    })


@login_required
def doctor_eliminar(request, pk):
    """DELETE (logico): Desactiva un doctor sin borrarlo de la BD."""
    doctor = get_object_or_404(Doctor, pk=pk, activo=True)
    if request.method == 'POST':
        doctor.activo = False
        doctor.save()
        messages.success(request, 'Doctor eliminado exitosamente.')
        return redirect('doctor_lista')
    return render(request, 'gestion/confirmar_eliminacion.html', {
        'objeto': doctor, 'tipo': 'doctor', 'lista_url': 'doctor_lista'
    })


# ═══════════════════════════════════════════════════════════════════════════════
# CRUD DE PACIENTES
# Mismo patron CRUD que los anteriores
# ═══════════════════════════════════════════════════════════════════════════════

@login_required
def paciente_lista(request):
    """READ: Lista todos los pacientes activos."""
    pacientes = Paciente.objects.filter(activo=True)
    return render(request, 'gestion/paciente_lista.html', {'pacientes': pacientes})


@login_required
def paciente_crear(request):
    """CREATE: Registra un nuevo paciente."""
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente registrado exitosamente.')
            return redirect('paciente_lista')
    else:
        form = PacienteForm()
    return render(request, 'gestion/paciente_formulario.html', {
        'form': form, 'titulo': 'Nuevo Paciente'
    })


@login_required
def paciente_editar(request, pk):
    """UPDATE: Edita los datos de un paciente existente."""
    paciente = get_object_or_404(Paciente, pk=pk, activo=True)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Paciente actualizado exitosamente.')
            return redirect('paciente_lista')
    else:
        form = PacienteForm(instance=paciente)
    return render(request, 'gestion/paciente_formulario.html', {
        'form': form, 'titulo': 'Editar Paciente'
    })


@login_required
def paciente_eliminar(request, pk):
    """DELETE (logico): Desactiva un paciente sin borrarlo de la BD."""
    paciente = get_object_or_404(Paciente, pk=pk, activo=True)
    if request.method == 'POST':
        paciente.activo = False
        paciente.save()
        messages.success(request, 'Paciente eliminado exitosamente.')
        return redirect('paciente_lista')
    return render(request, 'gestion/confirmar_eliminacion.html', {
        'objeto': paciente, 'tipo': 'paciente', 'lista_url': 'paciente_lista'
    })


# ═══════════════════════════════════════════════════════════════════════════════
# CRUD DE CITAS MEDICAS
# Usa select_related para traer paciente y doctor en una sola consulta
# ═══════════════════════════════════════════════════════════════════════════════

@login_required
def cita_lista(request):
    """
    READ: Lista todas las citas medicas activas.
    select_related('paciente', 'doctor') hace JOIN con ambas tablas
    para evitar consultas extras (N+1 problem).
    """
    citas = CitaMedica.objects.filter(activo=True).select_related('paciente', 'doctor')
    return render(request, 'gestion/cita_lista.html', {'citas': citas})


@login_required
def cita_crear(request):
    """CREATE: Crea una nueva cita medica."""
    if request.method == 'POST':
        form = CitaMedicaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita médica creada exitosamente.')
            return redirect('cita_lista')
    else:
        form = CitaMedicaForm()
    return render(request, 'gestion/cita_formulario.html', {
        'form': form, 'titulo': 'Nueva Cita Médica'
    })


@login_required
def cita_editar(request, pk):
    """UPDATE: Edita una cita medica existente (cambiar fecha, estado, etc)."""
    cita = get_object_or_404(CitaMedica, pk=pk, activo=True)
    if request.method == 'POST':
        form = CitaMedicaForm(request.POST, instance=cita)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cita médica actualizada exitosamente.')
            return redirect('cita_lista')
    else:
        form = CitaMedicaForm(instance=cita)
    return render(request, 'gestion/cita_formulario.html', {
        'form': form, 'titulo': 'Editar Cita Médica'
    })


@login_required
def cita_eliminar(request, pk):
    """DELETE (logico): Desactiva una cita medica sin borrarla de la BD."""
    cita = get_object_or_404(CitaMedica, pk=pk, activo=True)
    if request.method == 'POST':
        cita.activo = False
        cita.save()
        messages.success(request, 'Cita médica eliminada exitosamente.')
        return redirect('cita_lista')
    return render(request, 'gestion/confirmar_eliminacion.html', {
        'objeto': cita, 'tipo': 'cita médica', 'lista_url': 'cita_lista'
    })
