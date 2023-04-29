FROM python:3.9.5

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python3", "manage.py", "runserver"]