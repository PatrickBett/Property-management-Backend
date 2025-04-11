FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Set environment variable to prevent Django from buffering output
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 8000

# Collect static files
CMD ["bash", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn --bind 0.0.0.0:8000 backend.wsgi:application"]
