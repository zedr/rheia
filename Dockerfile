FROM library/python:alpine3.7
ENV PYTHONPATH /app

COPY . /app
WORKDIR /app

RUN apk add make gcc musl-dev
RUN pip install -r requirements.txt

EXPOSE 8000

CMD python scripts/manage.py runserver 0:8000 1>/dev/null
