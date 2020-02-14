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
