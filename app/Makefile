.PHONY: test ft ftff

test:
	virtualenv/bin/python manage.py test $(arg)

ft:
	virtualenv/bin/python manage.py test functional_tests $(arg)

ftff:
	virtualenv/bin/python manage.py test functional_tests --failfast $(arg)
