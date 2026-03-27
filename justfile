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
run:
    #!/usr/bin/env bash
    set -euo pipefail
    if ! just check_model_exists >/dev/null 2>&1; then
        echo "Model not found. Downloading model..."
        if [ -x "venv/bin/python" ]; then
            PYTHON_BIN="venv/bin/python"
        elif command -v python >/dev/null 2>&1; then
            PYTHON_BIN="python"
        elif command -v python3 >/dev/null 2>&1; then
            PYTHON_BIN="python3"
        else
            echo "Python interpreter not found. Run: just init"
            exit 1
        fi

        "$PYTHON_BIN" util/model_downloder.py
    fi

    docker compose up -d --build

[private]
check_model_exists:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ ! -f "notebooks/models/model.joblib" ]; then
        exit 1
    fi

# remove the docker image
prune:
    docker compose down --rmi local --volumes --remove-orphans

# use the model to predict on new data
predict text="":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ -z "{{ text }}" ]; then
        echo "Please provide text to predict, e.g. just predict text='Hello world'"
        exit 1
    fi

    response=$(curl -s -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d "{\"text\": \"{{ text }}\"}")
    echo "Prediction response: $response"

health:
    #!/usr/bin/env bash
    set -euo pipefail
    max_attempts=10
    attempt=1

    while [ "$attempt" -le "$max_attempts" ]; do
        response=$(curl -s -w "\n%{http_code}" --max-time 3 http://localhost:5000/health || true)
        status_code=$(echo "$response" | tail -n1)
        body=$(echo "$response" | sed '$d')

        if [ "$status_code" = "200" ]; then
            echo "Health check response: $body"
            exit 0
        fi

        sleep 1
        attempt=$((attempt + 1))
    done

    echo "Health check failed after $max_attempts attempts (last status: $status_code). Run: just run"
    exit 1
