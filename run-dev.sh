# 1. Make the migrations
python manage.py makemigrations
python manage.py makemigrations users brands contacts customers companies
python manage.py migrate

# 2. Collect static files (used for cloud storage)
python manage.py collectstatic --no-input

# 3. Remove all previous brand files (if any)
python manage.py load_brands_from_cloud_storage

# 4. Create superuser and Run server (no care about errors on superuser creation)
python manage.py createsuperuser --no-input && (python manage.py runserver 0.0.0.0:8000) || (python manage.py runserver 0.0.0.0:8000)
