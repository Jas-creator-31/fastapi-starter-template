#!/bin/bash
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

gnome-terminal --tab --title="BACKEND" -- bash -c "cd '$ROOT_DIR'; source .venv/bin/activate; uvicorn src.main:app --host='0.0.0.0' --ssl-keyfile='./localhost+2-key.pem' --ssl-certfile='./localhost+2.pem' --port=5000 --reload --log-level debug; exec bash"
