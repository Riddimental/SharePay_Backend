import subprocess
import os

# Crear y activar un entorno virtual
subprocess.run(['python3', '-m', 'venv', 'venv'])


subprocess.run('dir')

# Actualizar pip
# subprocess.run(['pip', 'install', '--upgrade', 'pip'])

# Instalar las dependencias
subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

# Desactivar el entorno virtual
# subprocess.run(['deactivate'])
