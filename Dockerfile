FROM library/python:alpine3.7

ENV PYTHONPATH /app
ENV RHEIA_SQLITE_DB_PATH /app/db.sqlite

COPY requirements.txt /app/
COPY dist/*.whl /app/
WORKDIR /app

RUN pip install -r requirements.txt
RUN pip install *.whl

EXPOSE 8000

CMD rheia-manage runserver 0:8000 1>/dev/null
