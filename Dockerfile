FROM python:3.11.9

WORKDIR /app

# Copiado de dependencias e instalacion
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copiado de codigo
COPY . .

# Exponer el puerto
EXPOSE 8000

# Variables de entorno para desarrollo
ENV FLASK_DEBUG=True
ENV PORT=8000

CMD ["python", "-u", "app.py"]