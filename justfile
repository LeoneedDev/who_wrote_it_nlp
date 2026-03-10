[private]
list:
    just --list

init:
    cp .env.example .env
    source .env

    echo "Dont forget to fill in the .env file with your WANDB_TOKEN"

    # Check if python command exists
    if ! command -v python &> /dev/null; then
        echo "Python is not installed. Please install Python to continue."
        exit 1
    fi
    
    # Check Python version is 3.13
    PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
    if [[ ! "$PYTHON_VERSION" =~ ^3\.13 ]]; then
        echo "Python 3.13 is required, but found version $PYTHON_VERSION"
        
        # Try to find python3.13 binary
        if command -v python3.13 &> /dev/null; then
            echo "Found python3.13, using it instead"
            alias python=python3.13
        else
            echo "Python 3.13 not found. Please install Python 3.13 to continue."
            exit 1
        fi
    fi
    
    # Check if pip is installed
    if ! command -v pip &> /dev/null; then
        echo "pip is not installed. Please install pip to continue."
        exit 1
    fi

    # Check if venv is created
    if [ ! -d "venv" ]; then
        python -m venv venv
    fi
    source venv/bin/activate

    pip install --upgrade pip
    pip install -r requirements.txt