import subprocess
import os

# Crear y activar un entorno virtual
subprocess.run(['python3', '-m', 'venv', 'venv'])

# Activar el entorno virtual
venv_activate_script = os.path.join('venv', 'bin', 'activate')
activate_command = f'source {venv_activate_script}'
subprocess.run(['/bin/bash', '-c', activate_command], shell=True)

# Actualizar pip
subprocess.run(['pip', 'install', '--upgrade', 'pip'])

# Instalar las dependencias
subprocess.run(['pip', 'install', '-r', 'requirements.txt'])

# Desactivar el entorno virtual
subprocess.run(['deactivate'])
