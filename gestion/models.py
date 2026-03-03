"""
models.py - Definicion de los modelos (tablas) de la base de datos.

Cada clase representa una tabla en PostgreSQL. Django se encarga de crear
las tablas automaticamente mediante las migraciones (python manage.py migrate).

Patron utilizado: ELIMINACION LOGICA (soft delete)
- En lugar de borrar registros de la BD, se usa un campo 'activo' (True/False).
- Cuando el usuario "elimina" un registro, se cambia activo=False.
- Las consultas filtran siempre por activo=True para no mostrar los eliminados.
- Esto permite recuperar datos si se eliminaron por error.
"""

from django.db import models


# ─── MODELO: ESPECIALIDAD ────────────────────────────────────────────────────
# Representa las especialidades medicas de la clinica (ej: Cardiologia, Pediatria).
# Es la tabla mas simple y sirve como catalogo para asignar especialidad a los doctores.

class Especialidad(models.Model):
    # CharField: campo de texto con longitud maxima definida
    nombre = models.CharField(max_length=100)
    # TextField: campo de texto sin limite (para descripciones largas)
    # blank=True significa que es opcional (el usuario puede dejarlo vacio)
    descripcion = models.TextField(blank=True)
    # BooleanField: campo True/False para la eliminacion logica
    # default=True: cuando se crea un registro nuevo, esta activo por defecto
    activo = models.BooleanField(default=True)

    class Meta:
        # verbose_name_plural: nombre que aparece en el panel de admin de Django
        verbose_name_plural = 'Especialidades'
        # ordering: ordena los resultados alfabeticamente por nombre
        ordering = ['nombre']

    def __str__(self):
        # __str__ define como se muestra el objeto cuando se convierte a texto
        # Por ejemplo: en un <select> de formulario aparece el nombre de la especialidad
        return self.nombre


# ─── MODELO: DOCTOR ───────────────────────────────────────────────────────────
# Representa a los doctores de la clinica. Cada doctor pertenece a una especialidad.

class Doctor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    # unique=True: no puede haber dos doctores con la misma cedula (restriccion de BD)
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    # EmailField: campo de texto que valida formato de email (ejemplo@dominio.com)
    email = models.EmailField(blank=True)
    # ForeignKey: crea una relacion de muchos-a-uno con Especialidad
    # on_delete=PROTECT: no se puede eliminar una especialidad si tiene doctores asignados
    # related_name='doctores': permite acceder a los doctores desde la especialidad
    #   Ejemplo: especialidad.doctores.all() devuelve todos los doctores de esa especialidad
    especialidad = models.ForeignKey(
        Especialidad, on_delete=models.PROTECT, related_name='doctores'
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Doctores'
        # Ordena primero por apellido y luego por nombre
        ordering = ['apellido', 'nombre']

    def __str__(self):
        # Muestra "Dr. Juan Perez" cuando se convierte a texto
        return f'Dr. {self.nombre} {self.apellido}'


# ─── MODELO: PACIENTE ─────────────────────────────────────────────────────────
# Representa a los pacientes registrados en la clinica.

class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    # DateField: campo de tipo fecha (YYYY-MM-DD en la base de datos)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    # Direccion es opcional (blank=True)
    direccion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


# ─── MODELO: CITA MEDICA ─────────────────────────────────────────────────────
# Representa las citas medicas. Relaciona un paciente con un doctor en una fecha/hora.
# Es el modelo principal del sistema ya que conecta pacientes y doctores.

class CitaMedica(models.Model):
    # ESTADO_CHOICES: lista de opciones permitidas para el campo 'estado'
    # Cada tupla tiene (valor_guardado_en_bd, texto_mostrado_al_usuario)
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),       # La cita esta programada
        ('Completada', 'Completada'),      # La cita ya se realizo
        ('Cancelada', 'Cancelada'),        # La cita fue cancelada
    ]

    # ForeignKey a Paciente: cada cita pertenece a un paciente
    # PROTECT: no se puede eliminar un paciente que tiene citas registradas
    paciente = models.ForeignKey(
        Paciente, on_delete=models.PROTECT, related_name='citas'
    )
    # ForeignKey a Doctor: cada cita es atendida por un doctor
    doctor = models.ForeignKey(
        Doctor, on_delete=models.PROTECT, related_name='citas'
    )
    fecha = models.DateField()
    # TimeField: campo de tipo hora (HH:MM:SS)
    hora = models.TimeField()
    # Motivo de la consulta (obligatorio)
    motivo = models.TextField()
    # Diagnostico del doctor (opcional, se llena despues de la consulta)
    diagnostico = models.TextField(blank=True)
    # Campo con opciones predefinidas (choices), por defecto 'Pendiente'
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default='Pendiente'
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cita Médica'
        verbose_name_plural = 'Citas Médicas'
        # Ordena por fecha y hora descendente (las mas recientes primero)
        # El signo '-' indica orden descendente (de mayor a menor)
        ordering = ['-fecha', '-hora']

    def __str__(self):
        return f'Cita: {self.paciente} - Dr. {self.doctor.apellido} ({self.fecha})'
