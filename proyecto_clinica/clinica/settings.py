"""
settings.py - Configuracion principal del proyecto Django.

Este archivo controla todo el comportamiento de Django:
- Conexion a la base de datos (PostgreSQL)
- Aplicaciones instaladas
- Middleware (capas de procesamiento de cada peticion)
- Configuracion de seguridad
- Archivos estaticos (CSS, JS, imagenes)
- Zona horaria e idioma

Usa variables de entorno (os.environ.get) para que los valores sensibles
como SECRET_KEY y la URL de la base de datos no esten en el codigo fuente.
En produccion (Railway), estas variables se configuran en el panel de Railway.
En desarrollo local, se usan los valores por defecto.
"""

import os
import dj_database_url
from pathlib import Path

# BASE_DIR: ruta absoluta del directorio del proyecto (donde esta manage.py)
# Se usa como referencia para construir otras rutas (ej: STATIC_ROOT)
BASE_DIR = Path(__file__).resolve().parent.parent


# ─── SEGURIDAD ────────────────────────────────────────────────────────────────

# SECRET_KEY: clave secreta para firmar cookies, tokens CSRF, etc.
# En produccion se lee de la variable de entorno 'SECRET_KEY' de Railway
# En desarrollo usa la clave por defecto (insegura, solo para desarrollo)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-_wcurx@^!c4sgf19z8uo6)yd%8q_6^)r357azjm_w&s^)og-mn')

# DEBUG: modo depuracion
# True = muestra errores detallados (solo para desarrollo)
# False = muestra paginas de error genericas (para produccion)
# En Railway la variable DEBUG='False'
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# ALLOWED_HOSTS: dominios/IPs desde los que se puede acceder al sitio
# En Railway: '.railway.app' permite acceso desde el dominio de Railway
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# CSRF_TRUSTED_ORIGINS: origenes confiables para proteccion CSRF
# Necesario para que los formularios funcionen en produccion con HTTPS
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',') if os.environ.get('CSRF_TRUSTED_ORIGINS') else []


# ─── APLICACIONES INSTALADAS ─────────────────────────────────────────────────

INSTALLED_APPS = [
    'django.contrib.admin',          # Panel de administracion de Django
    'django.contrib.auth',           # Sistema de autenticacion (login, logout, usuarios)
    'django.contrib.contenttypes',   # Framework de tipos de contenido
    'django.contrib.sessions',       # Manejo de sesiones de usuario
    'django.contrib.messages',       # Sistema de mensajes flash (exito, error, etc.)
    'django.contrib.staticfiles',    # Manejo de archivos estaticos (CSS, JS)
    'bootstrap5',                    # Paquete django-bootstrap-v5 para estilos
    'gestion',                       # Nuestra aplicacion principal de gestion clinica
]


# ─── MIDDLEWARE ───────────────────────────────────────────────────────────────
# Middleware: capas que procesan cada peticion HTTP antes de llegar a la vista
# y cada respuesta antes de enviarla al navegador

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',        # Seguridad HTTP (HTTPS, headers)
    'whitenoise.middleware.WhiteNoiseMiddleware',           # Sirve archivos estaticos en produccion
    'django.contrib.sessions.middleware.SessionMiddleware', # Manejo de sesiones
    'django.middleware.common.CommonMiddleware',            # Funciones comunes (trailing slash, etc.)
    'django.middleware.csrf.CsrfViewMiddleware',            # Proteccion contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Autenticacion de usuarios
    'django.contrib.messages.middleware.MessageMiddleware',    # Mensajes flash
    'django.middleware.clickjacking.XFrameOptionsMiddleware', # Proteccion contra clickjacking
]


# ─── CONFIGURACION DE URLs Y TEMPLATES ────────────────────────────────────────

# ROOT_URLCONF: archivo principal de URLs del proyecto
ROOT_URLCONF = 'clinica.urls'

# TEMPLATES: configuracion del sistema de templates (plantillas HTML)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],          # Directorios adicionales de templates (usamos APP_DIRS)
        'APP_DIRS': True,    # Busca templates en carpeta 'templates/' de cada app
        'OPTIONS': {
            # context_processors: variables disponibles en todos los templates
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',   # Variable 'request' en templates
                'django.contrib.auth.context_processors.auth',  # Variable 'user' en templates
                'django.contrib.messages.context_processors.messages',  # Mensajes flash
            ],
        },
    },
]

# WSGI_APPLICATION: punto de entrada para el servidor web (gunicorn en produccion)
WSGI_APPLICATION = 'clinica.wsgi.application'


# ─── BASE DE DATOS ────────────────────────────────────────────────────────────
# Usa dj_database_url para leer la URL de conexion de la variable de entorno DATABASE_URL
# En Railway: DATABASE_URL se configura automaticamente al crear la BD PostgreSQL
# En local: usa la conexion por defecto a PostgreSQL local

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:admin@localhost:5432/clinica_db'
    )
}


# ─── VALIDACION DE CONTRASENAS ────────────────────────────────────────────────
# Reglas que Django aplica al crear o cambiar contrasenas de usuarios

AUTH_PASSWORD_VALIDATORS = [
    {
        # No permite contrasenas similares al nombre de usuario o email
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Requiere un minimo de 8 caracteres
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Rechaza contrasenas comunes (ej: "password", "123456")
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Rechaza contrasenas que son solo numeros
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ─── INTERNACIONALIZACION ────────────────────────────────────────────────────

LANGUAGE_CODE = 'es'               # Idioma del sitio: espanol
TIME_ZONE = 'America/Guayaquil'    # Zona horaria: Ecuador
USE_I18N = True                    # Activa traduccion de textos
USE_TZ = True                      # Usa fechas con zona horaria


# ─── ARCHIVOS ESTATICOS (CSS, JavaScript, Imagenes) ──────────────────────────
# Django no sirve archivos estaticos en produccion por si solo.
# Usamos WhiteNoise para servir CSS/JS/imagenes directamente desde Django.

STATIC_URL = 'static/'                    # URL base para archivos estaticos
STATIC_ROOT = BASE_DIR / 'staticfiles'    # Carpeta donde collectstatic recopila los archivos

# WhiteNoise comprime y cachea los archivos estaticos para mejor rendimiento
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ─── CONFIGURACION GENERAL ───────────────────────────────────────────────────

# Tipo de campo para claves primarias autogeneradas (IDs)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ─── AUTENTICACION - REDIRECCIONES ───────────────────────────────────────────
# Estas URLs controlan hacia donde se redirige al usuario despues del login/logout

LOGIN_REDIRECT_URL = '/'                 # Despues de login exitoso → dashboard
LOGOUT_REDIRECT_URL = '/accounts/login/' # Despues de logout → pagina de login
LOGIN_URL = '/accounts/login/'           # Si no esta autenticado → pagina de login
