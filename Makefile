virtualenv=. env/bin/activate;
manage= PYTHONPATH=. python scripts/manage.py

default: virtualenv build

virtualenv:
	@virtualenv -q -p python2.7 env || true

build: requirements.txt env
	$(virtualenv) pip install -r requirements.txt

db: env
	$(virtualenv) $(manage) migrate

sync: env
	$(virtualenv) $(manage) makemigrations

doc: env
	$(virtualenv) cd docs && make html

serve: env
	$(virtualenv) $(manage) runserver 127.1:8000

test: env
	$(virtualenv) $(manage) test rheia

superuser: env
	$(virtualenv) $(manage) createsuperuser

clean:
	@rm -rf env
