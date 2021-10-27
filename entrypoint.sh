#!/bin/sh
/wait
flask db upgrade
gunicorn -c ./core/gunicorn.conf.py core.wsgi_app:app --reload
exec "$@"
