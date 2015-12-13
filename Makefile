virtualenv=. env/bin/activate;

default: virtualenv build

virtualenv:
	virtualenv -q -p python2.7 env || true

build: requirements.txt env
	$(virtualenv) pip install -r requirements.txt

db:
	$(virtualenv) python manage.py migrate

doc:
	$(virtualenv) cd docs && make html

clean:
	@rm -rf env
