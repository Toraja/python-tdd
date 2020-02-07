FROM python:3.6-alpine

ARG user=${user:-elspeth}

RUN adduser --disabled-password --gecos '' ${user}

USER ${user}
COPY --chown=${user}:${user} . /home/${user}/sites/
# WORKDIR creates dir with its owner as root by default even if `USER` command is preceded
# so it is placed after COPY which creates the target dir.
WORKDIR /home/${user}/sites/

RUN python3 -m venv virtualenv
RUN ./virtualenv/bin/pip3 install \
	django==1.11 \
	gunicorn \
	toml
RUN ./virtualenv/bin/python manage.py migrate --noinput

CMD ["./virtualenv/bin/gunicorn", "-b", "0.0.0.0:8000", "superlists.wsgi:application"]
