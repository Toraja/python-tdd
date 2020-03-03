FROM nginx:latest

COPY conf.template ep.sh /tmp/
COPY static /opt/app/static

CMD ["/tmp/ep.sh"]
