import subprocess

# Crear y activar un entorno virtual
subprocess.run(['python3', '-m', 'venv', 'venv'])
subprocess.run(['venv/bin/activate'], shell=True)

# actualiza pip
subprocess.run(['pip', 'install', '--upgrade', 'pip'])

# Instalar las dependencias
subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

# Desactivar el entorno virtual
# subprocess.run(['deactivate'], shell=True)
