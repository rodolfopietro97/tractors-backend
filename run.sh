# 1. Load brands

# 1.1 Remove all previous fixtures
rm -rf ./brands/fixtures/*.json

# 1.2 Load brands from cloud storage. This command will create a new fixture file in the brands/fixtures folder
python load_brands_from_cloud_storage.py

# 2. Make the migrations
python manage.py makemigrations
python manage.py makemigrations users brands contacts customers companies
python manage.py migrate

# 3. Collect static files (used for cloud storage)
python manage.py collectstatic --no-input

# 4. Remove all previous brand files (if any)
python manage.py clean_brands

# 5. Load brands online and files fixtures
python manage.py loaddata brands.json
python manage.py loaddata brand_files.json
python manage.py loaddata brand_online_credentials.json

# 6. Create superuser and Run server (no care about error)
python manage.py createsuperuser --no-input && (python manage.py runserver 0.0.0.0:8000) || (python manage.py runserver 0.0.0.0:8000)
