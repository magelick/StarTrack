#!/bin/sh

# Checking, migration 'initial' exists or not. If not, create this migration.
alembic history | grep 'initial' || alembic revision --autogenerate -m "initial"

# Applying all migrations
alembic upgrade head

# Start the application
python3 main.py