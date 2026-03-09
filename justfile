[private]
list:
    just --list

init:
    if [ -z "$(which python)" || -z]; then
        echo "Python is not installed. Please install Python to continue."
        exit 1
    fi
    if [ -z "$(which pip)" ]; then
        echo "pip is not installed. Please install pip to continue."
        exit 1
    fi

    if [ "$(python --version)"]
