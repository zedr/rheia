# Rheia - the time-saving time tracker
Rheia is a time tracker application written in Python, using the Django
web framework.

[![Build Status](https://travis-ci.com/zedr/rheia.svg?branch=master)](https://travis-ci.com/zedr/rheia)

## Pre-requisites
- Python 2.7: https://www.python.org/downloads/release/python-2711/
- VirtualEnv: https://pip.pypa.io/en/stable/installing/
- Pip: https://virtualenv.pypa.io/en/latest/installation.html

### Windows
On Windows, make sure the interpreter is available on the system "PATH". This
can be configured in the Control Panel:
    System and Security -> System -> Advanced System Settings: Environment Variables

Add these two paths, separated by a semicolon, to the user variable PATH:
    C:\Python27;C:\Python27\Scripts

Next, install Pip, a Python package manager:
    1. Visit Pip's Installation Guide (see above)
    2. Download the "get-pip.py" file
    3. Run "python get-pip.py" from the Command Line

You need Virtualenv next. Open a Command Line prompt and run "pip install virtualenv".

## Installation

### Windows
Perform the following steps:
    1. Open a command prompt from Rheia's root folder (where the make.bat file is located).
    2. Run the command "make virtualenv"
    3. Run the command "make build" (if the process terminates in a WindowsError, ignore it - this is a bug in Pip)
    4. Run the command "make db"
    5. Run the command "make user", and create your user's credentials
    6. Run the command "make serve"

Rheia will be available on http://localhost:8000 . Open your browser and visit the URL.

To build the documentation:
    1. "cd" into the "docs" folder
    2. Run the command "make html"
    3. Open the "index.html" in the newly generated build/html folder

## Configuration and usage
    1. Log into Rheia with your superuser account
    2. Click on the Admin link on the top right corner
    3. Add a new Client
    4. Add a new Team
    5. Add yourself and the new client to the new team
    6. Add a new Project
    7. Add one or more new Activities
    8. Go back to the main site
    9. You should now be able to log time
