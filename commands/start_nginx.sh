#!/bin/sh

envsubst < /etc/nginx/default.template > /etc/nginx/conf.d/default.conf && exec nginx -g 'daemon off;'
