# 1. Make the migrations
python manage.py makemigrations
python manage.py makemigrations users brands contacts customers companies
python manage.py migrate

# 2. Load all brands from cloud storage
python manage.py load_brands_from_cloud_storage

# 3. Create superuser and Run server (no care about errors on superuser creation)
python manage.py createsuperuser --no-input && (python manage.py runserver 0.0.0.0:8000 --nostatic) || (python manage.py runserver 0.0.0.0:8000 --nostatic)
