#!/bin/bash
# export FLASK_APP=admin.run:app
# export FLASK_ENV=production
# export FLASK_DEBUG=0
echo poetry run flask run -h 0.0.0.0
# poetry run flask db upgrade
# poetry run flask run -h 0.0.0.0 -p 5000

#for deploy
# poetry run gunicorn admin.run:app -b :5000 --log-level debug
gunicorn admin.run:app -b :5000 --log-level debug
