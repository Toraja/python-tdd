.PHONY: all webserver app

all: webserver app

webserver:
	@app/virtualenv/bin/python app/manage.py collectstatic --noinput
	@-rm --recursive --force nginx/static
	@cp --recursive app/static nginx/
	@docker-compose build webserver

app:
	@docker-compose build app
