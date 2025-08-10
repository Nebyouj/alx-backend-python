# messaging_app/Dockerfile
FROM python:3.10

# Set work directory
WORKDIR /app

# Prevents Python from writing .pyc files & enables output without buffering
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . /app/

# Expose Django default port
EXPOSE 8000

# Start server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# To build the Docker image, run:
# docker build -t my-django-app .
docker run -p 8000:8000 my-django-app

