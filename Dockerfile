FROM python:latest

WORKDIR /app

# Install git so AI models can be installed directly from GitHub repositories
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Upgrade pip and install Python dependencies (includes AI/ML libraries)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY server.py .

EXPOSE 5000

CMD ["python", "server.py"]
