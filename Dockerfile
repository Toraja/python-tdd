FROM ubuntu:latest

ARG user=${user:-elspeth}

RUN adduser --disabled-password --gecos '' ${user}

RUN apt-get update && apt-get install --yes \
    python3 \
    python3-venv \
    iproute2 \
    && rm -rf /var/lib/apt/lists/*

USER ${user}
# Placing below 2 command before apt-get somehow trigger apt-get to run everytime
# and cache is not used
COPY --chown=${user}:${user} . /home/${user}/sites/
# WORKDIR creates dir with its owner as root by default even if `USER` command is preceded
# so it is placed after COPY which creates the target dir.
WORKDIR /home/${user}/sites/

RUN python3 -m venv virtualenv
RUN ./virtualenv/bin/pip3 install \
	django==1.11 \
	toml
RUN ./virtualenv/bin/python manage.py migrate --noinput

ENTRYPOINT ["./virtualenv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
