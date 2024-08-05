web: gunicorn -b :6000 store.wsgi --log-file
web: python manage.py migrate && gunicorn store.wsg