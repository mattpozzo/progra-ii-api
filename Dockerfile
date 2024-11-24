# Usa la imagen base de Python
FROM python:3.12-alpine

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /code

# Configura variables de entorno para Flask
ENV FLASK_APP run.py
ENV FLASK_RUN_HOST 0.0.0.0

# Instala las dependencias necesarias para compilar extensiones de Python
RUN apk add --no-cache gcc musl-dev linux-headers postgresql-dev


# Copia el archivo de dependencias al contenedor
COPY requirements.txt requirements.txt

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código fuente al contenedor
COPY . .

# Comando por defecto para ejecutar la aplicación
CMD ["flask", "run"]
