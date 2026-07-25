
# Requirements

- Python 3.11
- PostgreSQL (Supabase)

## Install

pip install -r requirements.txt

## Configure

Create a `.env` file:

DATABASE_URL=...

## Run Migrations

alembic upgrade head

## Seed Data

python scripts/seed.py
