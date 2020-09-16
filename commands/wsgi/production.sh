#!/bin/bash

gunicorn \
    -w $WSGI_WORKERS \
    -b 0.0.0.0:$WSGI_PORT \
    --chdir $PROJECT_ROOT/src settings.wsgi \
    --timeout $WSGI_TIMEOUT \
    --max-requests 1000
