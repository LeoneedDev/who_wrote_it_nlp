list:
    @just --list --unsorted --list-heading "" --list-prefix "  - "

init:
    #!/usr/bin/env bash
    set -euo pipefail
    cp .env.example .env
    source .env

    echo "Dont forget to fill in the .env file with your WANDB_TOKEN"

    if ! command -v python >/dev/null 2>&1; then
        echo "Python is not installed. Please install Python to continue."
        exit 1
    fi

    PYTHON_VERSION="$(python --version 2>&1 | awk '{print $2}')"
    if [[ ! "$PYTHON_VERSION" =~ ^3\.13 ]]; then
        echo "Python 3.13 is required, but found version $PYTHON_VERSION"
        if command -v python3.13 >/dev/null 2>&1; then
            echo "Found python3.13, using it instead"
            PYTHON_BIN="python3.13"
        else
            echo "Python 3.13 not found. Please install Python 3.13 to continue."
            exit 1
        fi
    else
        PYTHON_BIN="python"
    fi

    if ! command -v pip >/dev/null 2>&1; then
        echo "pip is not installed. Please install pip to continue."
        exit 1
    fi

    if [ ! -d "venv" ]; then
        "$PYTHON_BIN" -m venv venv
    fi
    source venv/bin/activate

    pip install --upgrade pip
    pip install -r requirements.txt

# run docker server for predictions on port(default: 5000)
run port="5000":
    #!/usr/bin/env bash
    set -euo pipefail
    if ! just check_model_exists >/dev/null 2>&1; then
        echo "Model not found. Downloading model..."
        python util/model_downloder.py
    fi
    docker build -t who-wrote-it-app .
    docker run -p {port}:5000 who-wrote-it-app

[private]
check_model_exists:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ ! -f "notebooks/models/model.joblib" ]; then
        echo "Model not found. Please run: just download_model"
        exit 1
    fi

# remove the docker image
prune:
    docker rmi who-wrote-it-app

# use the model to predict on new data
predict text="" port="5000":
    #!/usr/bin/env bash
    set -euo pipefail
    if ! just health port={port}; then
        exit 1
    fi
    if [ -z "{text}" ]; then
        echo "Please provide text to predict, e.g. just predict text='Hello world'"
        exit 1
    fi

    response=$(curl -s -X POST http://localhost:{port}/predict -H "Content-Type: application/json" -d "{\"text\": \"{text}\"}")
    echo "Prediction response: $response"

health port="5000":
    #!/usr/bin/env bash
    set -euo pipefail
    response=$(curl -s -w "\n%{http_code}" http://localhost:{port}/health)
    status_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')

    if [ "$status_code" != "200" ]; then
        echo "Health check failed (status: $status_code). Run: just run"
        exit 1
    fi

    echo "Health check response: $body"
