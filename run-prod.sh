# 1. Collect static files (used for cloud storage)
python manage.py collectstatic --no-input

# 2. Make the migrations
python manage.py makemigrations
python manage.py makemigrations users brands contacts customers companies
python manage.py migrate

# 3. Load all brands from cloud storage
python manage.py load_brands_from_cloud_storage

# 4. Create superuser and Run server (no care about errors on superuser creation)
python manage.py createsuperuser --no-input && (python -m gunicorn tractors_be.asgi:application --bind :8000 -k uvicorn.workers.UvicornWorker) || (python -m gunicorn tractors_be.asgi:application --bind :8000 -k uvicorn.workers.UvicornWorker)
