virtualenv=. env/bin/activate;

default: virtualenv build

virtualenv:
	virtualenv -p python2.7 env

build: requirements.txt env
	$(virtualenv) pip install -r requirements.txt

db:
	$(virtualenv) python manage.py migrate

clean:
	@rm -rf env
