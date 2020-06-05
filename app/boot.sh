#!/usr/bin/env bash

python3 run.py create_db
python3 run.py initial_ingest --config=config/config.yml
python3 app.py