FROM python:3.6-alpine

ARG user=${user:-elspeth}
ARG ENV_TYPE

ENV ENV_TYPE ${ENV_TYPE}

RUN adduser --disabled-password --gecos '' ${user}

USER ${user}
COPY --chown=${user}:${user} . /home/${user}/sites/
# WORKDIR creates dir with its owner as root by default even if `USER` command is preceded
# so it is placed after COPY which creates the target dir.
WORKDIR /home/${user}/sites/

ENV PATH /home/${user}/.local/bin:${PATH}

RUN pip install \
	django==1.11 \
	gunicorn \
	toml

RUN python manage.py migrate --noinput

CMD ["gunicorn", "-b", "0.0.0.0:8000", "superlists.wsgi:application"]
