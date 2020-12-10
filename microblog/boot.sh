#!/bin/sh
source venv/bin/activate
flask db upgrade
flask run --host=0.0.0.0 --port=8080
