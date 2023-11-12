import subprocess

# activa el entorno virtual
subprocess.run(['source', 'venv/bin/activate'], shell=True)

# actualiza pip
subprocess.run(['pip', 'install', '--upgrade', 'pip'])

# ejecuta la aplicacion normalmente
subprocess.run(['python', 'manage.py', 'runserver'])
