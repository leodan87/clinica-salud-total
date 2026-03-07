from django.db import migrations


def asignar_usuario(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Especialidad = apps.get_model('gestion', 'Especialidad')
    Doctor = apps.get_model('gestion', 'Doctor')
    Paciente = apps.get_model('gestion', 'Paciente')
    CitaMedica = apps.get_model('gestion', 'CitaMedica')

    primer_usuario = User.objects.first()
    if primer_usuario:
        Especialidad.objects.filter(usuario__isnull=True).update(usuario=primer_usuario)
        Doctor.objects.filter(usuario__isnull=True).update(usuario=primer_usuario)
        Paciente.objects.filter(usuario__isnull=True).update(usuario=primer_usuario)
        CitaMedica.objects.filter(usuario__isnull=True).update(usuario=primer_usuario)


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0002_citamedica_usuario_doctor_usuario_and_more'),
    ]

    operations = [
        migrations.RunPython(asignar_usuario, migrations.RunPython.noop),
    ]
