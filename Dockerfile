FROM python:3.11.3
# Establece el directorio de trabajo dentro del contenedor
WORKDIR /main

# Copia el archivo de requerimientos al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt


# Copia el código fuente al directorio de trabajo
COPY . .

# Define el comando para ejecutar la aplicación
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
