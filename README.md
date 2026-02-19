# Clinica Salud Total

Sistema de gestion de clinica medica desarrollado con Django. Permite administrar especialidades, doctores, pacientes y citas medicas de forma integral.

## Descripcion

Clinica Salud Total es una aplicacion web que facilita la gestion diaria de una clinica medica. Proporciona un panel de control con estadisticas en tiempo real y operaciones CRUD completas para cada entidad del sistema.

### Funcionalidades principales

- **Panel de control (Dashboard):** Muestra estadisticas generales como total de pacientes, doctores, citas pendientes y especialidades activas.
- **Gestion de Especialidades:** Crear, editar, listar y eliminar especialidades medicas (ej. Cardiologia, Pediatria).
- **Gestion de Doctores:** Registrar doctores con su cedula, datos de contacto y especialidad asignada.
- **Gestion de Pacientes:** Registrar pacientes con sus datos personales, fecha de nacimiento y direccion.
- **Gestion de Citas Medicas:** Agendar citas vinculando paciente y doctor, con fecha, hora, motivo, diagnostico y estado (Pendiente, Completada, Cancelada).
- **Autenticacion de usuarios:** Registro de nuevos usuarios e inicio de sesion. Todas las vistas estan protegidas con `@login_required`.
- **Panel de administracion Django:** Acceso al admin con filtros y busqueda para cada modelo.
- **Eliminacion logica (Soft Delete):** Los registros no se borran fisicamente, se marcan como inactivos para preservar la integridad de los datos.

## Tecnologias utilizadas

| Tecnologia | Uso |
|---|---|
| Python 3.13 | Lenguaje de programacion |
| Django 4.2 | Framework web |
| PostgreSQL | Base de datos |
| Bootstrap 5 | Estilos y componentes de interfaz |
| Bootstrap Icons | Iconografia |
| Gunicorn | Servidor WSGI para produccion |
| WhiteNoise | Servir archivos estaticos en produccion |
| Railway | Plataforma de despliegue |

## Modelos de datos

- **Especialidad:** nombre, descripcion, activo
- **Doctor:** nombre, apellido, cedula (unica), telefono, email, especialidad (FK), activo
- **Paciente:** nombre, apellido, cedula (unica), fecha de nacimiento, telefono, email, direccion, activo
- **CitaMedica:** paciente (FK), doctor (FK), fecha, hora, motivo, diagnostico, estado, activo

## Estructura del proyecto

```
clinica-django/
├── proyecto_clinica/
│   ├── clinica/           # Configuracion del proyecto Django
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── gestion/           # Aplicacion principal
│   │   ├── models.py      # Modelos de datos
│   │   ├── views.py       # Vistas (controladores)
│   │   ├── forms.py       # Formularios
│   │   ├── admin.py       # Configuracion del admin
│   │   ├── urls.py        # Rutas de la aplicacion
│   │   └── templates/     # Plantillas HTML
│   └── manage.py
├── requirements.txt
├── Procfile
└── runtime.txt
```

## Rutas principales

| Ruta | Descripcion |
|---|---|
| `/` | Dashboard principal |
| `/especialidades/` | Listado de especialidades |
| `/doctores/` | Listado de doctores |
| `/pacientes/` | Listado de pacientes |
| `/citas/` | Listado de citas medicas |
| `/accounts/login/` | Inicio de sesion |
| `/accounts/registro/` | Registro de usuario |
| `/admin/` | Panel de administracion Django |

## Instalacion local

1. Clonar el repositorio:
   ```bash
   git clone <url-del-repositorio>
   cd clinica-django
   ```

2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. Configurar la base de datos PostgreSQL y ajustar `settings.py` con las credenciales correspondientes.

5. Ejecutar migraciones:
   ```bash
   cd proyecto_clinica
   python manage.py migrate
   ```

6. Crear un superusuario:
   ```bash
   python manage.py createsuperuser
   ```

7. Iniciar el servidor de desarrollo:
   ```bash
   python manage.py runserver
   ```

8. Abrir en el navegador: `http://127.0.0.1:8000/`

## Despliegue en Railway

La aplicacion esta desplegada en **Railway**, una plataforma en la nube que hospeda tanto el proyecto Django como la base de datos PostgreSQL.

### Como funciona

- Railway ejecuta el proyecto usando **Gunicorn** como servidor, configurado en el archivo `Procfile`:
  ```
  web: cd proyecto_clinica && gunicorn clinica.wsgi --bind 0.0.0.0:$PORT
  ```
- Railway provee una base de datos **PostgreSQL** en la nube y genera automaticamente la variable de entorno `DATABASE_URL` para que Django se conecte a ella.
- Los archivos estaticos (CSS, JS, imagenes) se sirven con **WhiteNoise** sin necesidad de un servidor adicional.
- Las migraciones se ejecutan automaticamente en cada despliegue.

### Archivos de configuracion para Railway

| Archivo | Funcion |
|---|---|
| `Procfile` | Define el comando para iniciar el servidor con Gunicorn |
| `runtime.txt` | Especifica la version de Python (3.13.2) |
| `requirements.txt` | Lista las dependencias que Railway instala automaticamente |

### Variables de entorno en Railway

Estas variables se configuran en el panel de Railway:

| Variable | Descripcion |
|---|---|
| `SECRET_KEY` | Clave secreta de Django |
| `DEBUG` | `False` en produccion |
| `ALLOWED_HOSTS` | Dominios permitidos |
| `CSRF_TRUSTED_ORIGINS` | Origenes HTTPS de confianza |
| `DATABASE_URL` | URL de conexion a PostgreSQL (generada automaticamente por Railway) |
