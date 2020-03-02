# Test-Driven Development with Python
[Book's github URL](https://github.com/hjwp/Book-TDD-Web-Dev-Python)

## Installation

### Prerequisite
- python3 (including pip and virtualenv)
- geckodriver
- docker, docker-compose

To install geckodriver:  
**Ubuntu**  
```sh
apt install firefox-geckodriver
```

**Manual**  
```sh
# Find your desired version at https://github.com/mozilla/geckodriver/releases
wget -O /tmp/gecko https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
tar -xzvf /tmp/gecko
mv ./geckodriver /usr/local/bin/ # or any directory in your PATH
```

### For Server
```sh
cd app/
python3 -m venv virtualenv
# append .csh or .fish depending on your needs
source virtualenv/bin/activate
pip install -r requirements.txt
```

### For Test
```sh
# run inside virtual env
pip install -r requirements_test.txt
```

## Usage

### Start server

To start django only:
```sh
python manage.py runserver
```
To launch full stack
```sh
docker-compose up
```

### UT
```sh
## {app} is app name such as 'list'
python manage.py test {app}
```

### FT
```sh
python manage.py test functional_tests

# To run specific test
python manage.py test functional_tests.test.{Test class name}.{Test function name}
# e.g.
python app/manage.py test functional_tests.test.NewVisitorTest.test_can_start_a_list_for_one_user
```
django (`LiveServerTestCase` class) starts the server automatically on the
localhost, so there is no need to start the server manually.  

To test against docker container, set environment variables in `.env` before
starting up docker containers (or restart them if already running).  
Make sure the domain is added to `/etc/hosts`.  

### Deploy
Make sure docker is in swarm mode. To find out, issue the command below and see
if the output is `active`.
```sh
docker info -f '{{ .Swarm.LocalNodeState }}'
```

The stack uses label to distribute tasks to desired nodes. Add `app=yes` label
to nodes for app, and `web=yes` to nodes for webserver.  
Note that labels are not mandatory, in which case docker arbitrarily distribute
tasks to nodes.  
To find out what labels a node has, run the command below.  
Run with `self` for the current node or with node ID or hostname for others,
which can be found out by running `docker node ls`.
```sh
docker node inspect -f '{{range $k, $v := .Spec.Labels }}{{ printf "%s: %s\n" $k $v }}{{end}}' <NODE>
```
To add labels to nodes, run the command below.
```sh
docker node update --label-add <LABELS...> <NODE>
```

Run the command below to deploy the stack.
```sh
docker stack deploy --with-registry-auth --compose-file=docker-compose.yml --compose-file=docker-stack.yml python-tdd
```

## Note

### Volume sharing
Tried below methods, but none worked.

#### master as NFS server, app and webserver as client
This does not work as binding NFS covers up the contents of destination
directory. Running `collectstatic` at run time does not work either as
`collectstatic` tries to lock files but NFS does not allow a client to do it.  
`cp` should work but I have not tried and am not sure what the consequense of
concurrent write to NFS mount directory is.

#### app as NFS server, webserver as client
This requires bind mount of NFS share to static directory. As this also covers
up the directory, running `collectstatic` at run time is required.
`collectstatic` succeeds, but somehow nginx respond with `502 Bad Gateway`.

#### Third party volumm driver

##### Rexray
Rexray is not meant for data sharing between nodes, but rather for backup and
restoring when nodes shutdown/fail and are restored.  
Reference: [How to setup rexray](https://autoize.com/persistent-storage-for-docker-swarms-with-rex-ray/)
