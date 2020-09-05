#!/bin/bash

rm $PROJECT_ROOT/tmp/celerybeat-schedule $PROJECT_ROOT/tmp/celerybeat.pid

celery -A settings beat \
       --loglevel=info \
       --workdir=$PROJECT_ROOT/src \
       --schedule=$PROJECT_ROOT/tmp/celerybeat-schedule \
       --pidfile=$PROJECT_ROOT/tmp/celerybeat.pid
