release: sh /app/bin/install_wkhtmltopdf.sh
web: gunicorn cover_me.wsgi
worker: celery -A cover_me worker -l info
