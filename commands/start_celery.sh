#!/bin/bash

rm $PROJECT_ROOT/tmp/celery.pid

celery -A settings worker -E \
       --loglevel=info \
       --workdir=$PROJECT_ROOT/src \
       --pidfile=$PROJECT_ROOT/tmp/celery.pid
