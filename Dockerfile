FROM python:3.14-slim-trixie

ARG MODEL_PATH=model.joblib 
ARG MODEL_URL

WORKDIR /app

# Install git so AI models can be installed directly from GitHub repositories
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

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

EXPOSE 5000

CMD ["flask", "run"]
