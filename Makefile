.PHONY: build db sync doc serve shell test superuser

virtualenv=. env/bin/activate;
manage= PYTHONPATH=. python scripts/manage.py

default: env build

env:
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
	$(virtualenv) $(manage) runserver 0:8000

shell: env
	$(virtualenv) $(manage) shell

test: default
	$(virtualenv) $(manage) test rheia

superuser: env
	$(virtualenv) $(manage) createsuperuser

clean:
	@rm -rf env
