# SharePay Backend

Este es el repositorio del backend de SharePay App, una aplicación de gestión de eventos.

## Prerequisitos

Asegúrate de tener instalados los siguientes requisitos antes de comenzar:

- Python 3.10 o superior
- Django 4.2.5 o superior
- Virtualenv 20.24 o superior

## Instrucciones

Sigue estos pasos para configurar y ejecutar el proyecto localmente:

1. Clona el repositorio:

   ```bash
   git clone git@github.com:Riddimental/SharePay_Backend.git
   ```

2. Crea un entorno virtual

   - **Windows**:

     ```cmd
     python -m venv myenv
     ```

   - **macOS y Linux**:

     ```sh
     python3 -m venv myenv
     ```

3. Activa el entorno virtual

   - **Windows**:

     ```cmd
     .\myenv\Scripts\activate
     ```

   - **macOS y Linux**:

     ```sh
     source myenv/bin/activate
     ```

4. Instala los requisitos del proyecto en el entorno virtual:

   ```bash
   pip install -r requirements.txt
   ```

5. Ejecuta el servidor de desarrollo de Django:

   ```bash
   python manage.py runserver
   ```

Esto ejecutará el servidor Backend de la aplicación SharePay App, que puedes encontrar en:

- [Repositorio SharePay App](https://github.com/MavelSterling/SharePay_AppWeb)
