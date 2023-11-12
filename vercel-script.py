import subprocess
import os

# Crear y activar un entorno virtual
subprocess.run(['python3', '-m', 'venv', 'venv'])

# Activar el entorno virtual
venv_activate_script = os.path.join('venv', 'bin', 'activate')
subprocess.run(['chmod', '+x', venv_activate_script])
subprocess.run([venv_activate_script])

# Actualizar pip
subprocess.run(['pip', 'install', '--upgrade', 'pip'])

# Instalar las dependencias
subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

# Desactivar el entorno virtual
subprocess.run(['deactivate'])
