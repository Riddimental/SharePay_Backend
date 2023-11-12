#!/bin/bash

# Crear y activar el entorno virtual
python3 -m venv venv
source venv/bin/activate 

# Instalar las dependencias
pip install -r requirements.txt

# Desactivar el entorno virtual
deactivate
