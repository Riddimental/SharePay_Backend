import subprocess

# activa el entorno virtual
subprocess.run(['venv/bin/activate'], shell=True)


# ejecuta la aplicacion normalmente
subprocess.run(['python', 'manage.py', 'runserver'])
