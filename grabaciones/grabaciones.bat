@echo off

rem Activa el entorno virtual
call D:\CEPRE\archivos\grabaciones\venv\Scripts\activate

rem Ejecuta el script Python
python D:\CEPRE\archivos\grabaciones\grabaciones.py

rem Desactiva el entorno virtual (opcional)
deactivate