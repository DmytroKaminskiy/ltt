#!/usr/bin/env bash

git pull origin master &&
docker-compose up -d --build &&
docker exec backend python ./src/manage.py migrate &&
docker exec backend python ./src/manage.py collecstatic --noinput &&
docker exec -it backend pytest ./src/tests -s -x --cov=src --cov-report html
