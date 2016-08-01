@ECHO OFF

set BUILDDIR=%cd%
set VIRTUALENV=env\Scripts\activate.bat
set PYTHONPATH=.

:start

if "%1" == "help" (
	:help
	echo.Welcome to ==RHEIA==
	echo.
	echo.Use `make ^<target^>` where ^<target^> is one of:
	echo.
	echo.  virtualenv       Create the Python virtual environment.
    echo.  build            Build the project.
    echo.  serve            Run the Django server on port 8000.
    echo.  db               Syncronize the relational database, and run the migrations.
    echo.  user             Create a new superuser.
	echo.  clean            Clean all build directories, but keep the data.
	echo.
	goto:repl
)

if "%1" == "clean" (
	for /d %%i in (env docs\build) do rmdir /q /s %%i
	goto:eof
)

if "%1" == "virtualenv" (
    :virtualenv
    call virtualenv -q env
	call %VIRTUALENV%
	call pip install --upgrade setuptools
	goto:eof
)

if "%1" == "build" (
	:build
	call %VIRTUALENV%
    call pip install -r requirements.txt
	goto:eof
)

if "%1" == "tests" (
   call %VIRTUALENV%
   call python scripts\manage.py test
   goto:eof
)

if "%1" == "serve" (
   call %VIRTUALENV%
   call python scripts\manage.py runserver localhost:8000
   goto:eof
)

if "%1" == "db" (
   call %VIRTUALENV%
   call python scripts\manage.py syncdb --noinput
   call python scripts\manage.py migrate
)

if "%1" == "user" (
   call %VIRTUALENV%
   call python scripts\manage.py createsuperuser
)

if "%1" == "" (
    goto help
	:repl
	pause
)

:end
