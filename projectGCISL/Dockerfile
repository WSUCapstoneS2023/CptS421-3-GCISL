FROM python:3.9.5

ENV PYTHONUNBUFFERED=1

WORKDIR /django

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD python3 manage.py runserver 0.0.0.0:8000

