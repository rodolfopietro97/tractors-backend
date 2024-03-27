#!/usr/bin/env bash
# 1. Exit on error
set -o errexit

# 2. Install requirements
pip install -r requirements.txt

# 3. Collect static files (used for cloud storage)
python manage.py collectstatic --no-input

# 4. Make the migrations
python manage.py makemigrations
python manage.py makemigrations users brands contacts customers companies
python manage.py migrate

# 5. Load all brands from cloud storage
python manage.py load_brands_from_cloud_storage

# 6. Create superuser
python manage.py createsuperuser --no-input && (exit 0) || (exit 0)
