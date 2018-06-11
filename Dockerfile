FROM python:3.6-jessie

RUN useradd critical_numbers

WORKDIR /home/hot-tm-critical_numbers

COPY readme.md readme.md
COPY requirements.txt requirements.txt
COPY setup.py setup.py
COPY cli.py cli.py
COPY critical_numbers critical_numbers

RUN apt-get update
RUN yes | apt-get install libgeos++
RUN pip install .
RUN chown -R critical_numbers:critical_numbers ./

USER critical_numbers

EXPOSE 5000

ENTRYPOINT gunicorn -b :5000 --access-logfile - --error-logfile - -t 300 critical_numbers:app
