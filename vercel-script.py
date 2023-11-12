import subprocess

# Crear y activar un entorno virtual
subprocess.run(['python3', '-m', 'venv', 'venv'])
subprocess.run(['source', 'venv/bin/activate'], shell=True)

# Instalar las dependencias
subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

# Desactivar el entorno virtual
subprocess.run(['deactivate'], shell=True)
