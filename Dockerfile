FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies including fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
  locales tzdata libfreetype6 \
  && rm -rf /var/lib/apt/lists/*

# Set locale to German
RUN sed -i 's/# de_DE.UTF-8 UTF-8/de_DE.UTF-8 UTF-8/' /etc/locale.gen && \
  locale-gen

ENV LANG=de_DE.UTF-8 \
  LANGUAGE=de_DE:de \
  LC_ALL=de_DE.UTF-8 \
  TZ=Europe/Berlin

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt \
#   && pip uninstall -y polars \
#   && pip install --no-deps polars-lts-cpu

# Define environment variable
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "src/main.py"]