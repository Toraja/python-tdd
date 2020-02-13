#!/bin/sh

DOLLAR='$' envsubst < /tmp/conf.template > /etc/nginx/conf.d/default.conf

nginx -g "daemon off;"
