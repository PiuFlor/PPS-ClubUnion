
# Sistema de Gestión para Club de Fútbol

Este proyecto consiste en la gestión y administración de un club de fútbol. El sistema ayuda a organizar de manera eficiente información sobre los socios, profesores, deportes y categorías del club, reemplazando el manejo manual en papel por una solución digital.

El proyecto fue desarrollado utilizando **Django**, un framework web de Python, y fue realizado como parte de una pasantía. La aplicación permite gestionar todos los aspectos clave del club, mejorando la eficiencia administrativa.

## Funcionalidades principales:
- Registro y administración de socios del club.
- Gestión de profesores y deportes.
- Organización de categorías y actividades dentro del club.

## Requisitos previos
Asegúrate de tener instalado lo siguiente en tu máquina:
- Python 3.x

## Cómo iniciar el proyecto

## 1. Crear el entorno virtual
Crea un entorno virtual para el proyecto:
- python -m venv club_env

## 2. Activar el entorno virtual
En windowns:
- club_env\Scripts\activate
En macOS/Linux
- source club_env/bin/activate

## 3. Instalar los requerimientos
Con el entorno virtual activado, instala las dependencias del proyecto:
- pip install -r requirements.txt

## 4. Configurar variables de entorno
Renombra el archivo .env_template a .env y proporciona los valores necesarios:

## 5. Aplicar migraciones
Ejecuta las migraciones para configurar la base de datos:
- python manage.py migrate

## 6. Crear un superusuario
Crea un superusuario para acceder al panel de administración:
- python manage.py createsuperuser

## 7. Iniciar el servidor
Inicia el servidor de desarrollo de Django:
- python manage.py runserver

## 8. Acceder al panel de administración
Abre tu navegador y ve a la siguiente dirección para ingresar con las credenciales del superusuario:
- http://127.0.0.1:8000/admin

