release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn craigslist_ish.wsgi --log-file