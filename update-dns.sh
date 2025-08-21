#!/usr/bin/env bash
SCRIPT_DIR=$(dirname -- "$(readlink -f "${BASH_SOURCE}")") 
source "${SCRIPT_DIR}/venv/bin/activate"
python "${SCRIPT_DIR}/main.py"
