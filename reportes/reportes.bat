@echo off

rem Activa el entorno virtual
call D:\CEPRE\archivos\reportes\venv\Scripts\activate

rem Ejecuta el script Python
python D:\CEPRE\archivos\reportes\reportes.py

rem Desactiva el entorno virtual (opcional)
deactivate