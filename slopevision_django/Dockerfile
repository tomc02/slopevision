# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /code

# Install system dependencies and Chromium with ChromeDriver
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxss1 \
    libappindicator1 \
    libasound2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxi6 \
    ffmpeg \
    ca-certificates \
    fonts-liberation \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# Set Chrome and Chromedriver path environment variables
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Install pip dependencies
COPY requirements.txt .
COPY slopevision-dev.json .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Expose the port if needed
EXPOSE 8000

RUN apt-get update && apt-get install -y wget gnupg
RUN playwright install --with-deps

# Run your Django app with Gunicorn
CMD ["gunicorn", "slopevision_django.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "900"]
