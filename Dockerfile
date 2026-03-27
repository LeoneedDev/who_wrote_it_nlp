FROM python:3.13-slim-trixie

ARG MODEL_PATH=notebooks/models/model.joblib
ARG MODEL_URL="default_url" #TODO: set the default URL for the model

WORKDIR /app

# Install git so AI models can be installed directly from GitHub repositories
RUN apt-get update && apt-get install -y git curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN --mount=type=bind,source=${MODEL_PATH},target=/tmp/model.joblib,ro \
    if [ -f /tmp/model.joblib ]; then \
        cp /tmp/model.joblib /app/model.joblib; \
    else \
        apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* && \
        curl -L -o /app/model.joblib "$MODEL_URL"; \
    fi

COPY ${MODEL_PATH} model.joblib

# Upgrade pip and install Python dependencies (includes AI/ML libraries)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY util/ util/

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
