from django.db import models


class Especialidad(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Especialidades'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Doctor(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    especialidad = models.ForeignKey(
        Especialidad, on_delete=models.PROTECT, related_name='doctores'
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Doctores'
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f'Dr. {self.nombre} {self.apellido}'


class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    cedula = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    direccion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class CitaMedica(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    ]

    paciente = models.ForeignKey(
        Paciente, on_delete=models.PROTECT, related_name='citas'
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.PROTECT, related_name='citas'
    )
    fecha = models.DateField()
    hora = models.TimeField()
    motivo = models.TextField()
    diagnostico = models.TextField(blank=True)
    estado = models.CharField(
        max_length=20, choices=ESTADO_CHOICES, default='Pendiente'
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cita Médica'
        verbose_name_plural = 'Citas Médicas'
        ordering = ['-fecha', '-hora']

    def __str__(self):
        return f'Cita: {self.paciente} - Dr. {self.doctor.apellido} ({self.fecha})'
