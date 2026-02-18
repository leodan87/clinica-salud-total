from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Especialidad, Doctor, Paciente, CitaMedica
from .forms import (
    EspecialidadForm, DoctorForm, PacienteForm,
    CitaMedicaForm, RegistroUsuarioForm,
)


# ─── INICIO ──────────────────────────────────────────────────────────────────

@login_required
def home(request):
    contexto = {
        'total_pacientes': Paciente.objects.filter(activo=True).count(),
        'total_doctores': Doctor.objects.filter(activo=True).count(),
        'total_citas': CitaMedica.objects.filter(activo=True).count(),
        'citas_pendientes': CitaMedica.objects.filter(activo=True, estado='Pendiente').count(),
        'total_especialidades': Especialidad.objects.filter(activo=True).count(),
    }
    return render(request, 'home.html', contexto)


# ─── REGISTRO DE USUARIO ─────────────────────────────────────────────────────

def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada exitosamente. Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registration/register.html', {'form': form})


# ─── ESPECIALIDADES ──────────────────────────────────────────────────────────

@login_required
def especialidad_lista(request):
    especialidades = Especialidad.objects.filter(activo=True)
    return render(request, 'gestion/especialidad_lista.html', {'especialidades': especialidades})


@login_required
def especialidad_crear(request):
    if request.method == 'POST':
        form = EspecialidadForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Especialidad creada exitosamente.')
            return redirect('especialidad_lista')
    else:
        form = EspecialidadForm()
    return render(request, 'gestion/especialidad_formulario.html', {
        'form': form, 'titulo': 'Nueva Especialidad'
    })


@login_required
def especialidad_editar(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk, activo=True)
    if request.method == 'POST':
        form = EspecialidadForm(request.POST, instance=especialidad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Especialidad actualizada exitosamente.')
            return redirect('especialidad_lista')
    else:
        form = EspecialidadForm(instance=especialidad)
    return render(request, 'gestion/especialidad_formulario.html', {
        'form': form, 'titulo': 'Editar Especialidad'
    })


@login_required
def especialidad_eliminar(request, pk):
    especialidad = get_object_or_404(Especialidad, pk=pk, activo=True)
    if request.method == 'POST':
        especialidad.activo = False
        especialidad.save()
        messages.success(request, 'Especialidad eliminada exitosamente.')
        return redirect('especialidad_lista')
    return render(request, 'gestion/confirmar_eliminacion.html', {
        'objeto': especialidad, 'tipo': 'especialidad', 'lista_url': 'especialidad_lista'
    })


# ─── DOCTORES ────────────────────────────────────────────────────────────────

@login_required
def doctor_lista(request):
    doctores = Doctor.objects.filter(activo=True).select_related('especialidad')
    return render(request, 'gestion/doctor_lista.html', {'doctores': doctores})


@login_required
def doctor_crear(request):
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
    doctor = get_object_or_404(Doctor, pk=pk, activo=True)
    if request.method == 'POST':
        doctor.activo = False
        doctor.save()
        messages.success(request, 'Doctor eliminado exitosamente.')
        return redirect('doctor_lista')
    return render(request, 'gestion/confirmar_eliminacion.html', {
        'objeto': doctor, 'tipo': 'doctor', 'lista_url': 'doctor_lista'
    })


# ─── PACIENTES ───────────────────────────────────────────────────────────────

@login_required
def paciente_lista(request):
    pacientes = Paciente.objects.filter(activo=True)
    return render(request, 'gestion/paciente_lista.html', {'pacientes': pacientes})


@login_required
def paciente_crear(request):
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
    paciente = get_object_or_404(Paciente, pk=pk, activo=True)
    if request.method == 'POST':
        paciente.activo = False
        paciente.save()
        messages.success(request, 'Paciente eliminado exitosamente.')
        return redirect('paciente_lista')
    return render(request, 'gestion/confirmar_eliminacion.html', {
        'objeto': paciente, 'tipo': 'paciente', 'lista_url': 'paciente_lista'
    })


# ─── CITAS MÉDICAS ───────────────────────────────────────────────────────────

@login_required
def cita_lista(request):
    citas = CitaMedica.objects.filter(activo=True).select_related('paciente', 'doctor')
    return render(request, 'gestion/cita_lista.html', {'citas': citas})


@login_required
def cita_crear(request):
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
    cita = get_object_or_404(CitaMedica, pk=pk, activo=True)
    if request.method == 'POST':
        cita.activo = False
        cita.save()
        messages.success(request, 'Cita médica eliminada exitosamente.')
        return redirect('cita_lista')
    return render(request, 'gestion/confirmar_eliminacion.html', {
        'objeto': cita, 'tipo': 'cita médica', 'lista_url': 'cita_lista'
    })
