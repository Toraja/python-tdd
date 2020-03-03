FROM python:3.6-alpine

ARG user
RUN adduser --disabled-password --gecos '' ${user}
USER ${user}

ENV PATH /home/${user}/.local/bin:${PATH}
COPY --chown=${user}:${user} requirements.txt /home/${user}/sites/
# WORKDIR creates dir with its owner as root by default even if `USER` command is preceded
# so it is placed after COPY which creates the target dir.
WORKDIR /home/${user}/sites/
RUN pip install --upgrade pip && \
	pip install --no-cache-dir --requirement requirements.txt

COPY --chown=${user}:${user} . /home/${user}/sites/

RUN python manage.py migrate --noinput

EXPOSE 8000

CMD ["gunicorn", "-b", "0.0.0.0:8000", "superlists.wsgi:application"]
