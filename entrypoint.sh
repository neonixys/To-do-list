#!/bin/bash
python manage.py migrate --check
status=$?
if [[ $status != 0 ]]; then
  python manage.py migrate
fi
exec "$@"



# export FLASK_APP=app.py
# flask run -h 0.0.0.0 -p 80
