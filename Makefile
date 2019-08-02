.PHONY: python-packages install run


python-packages:
	pip install -r requirements.txt

install: python-packages

run:
	uwsgi --ini app.ini

