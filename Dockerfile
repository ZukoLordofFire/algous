FROM python:3.13-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY algousTESTTask/ /app

WORKDIR /app

CMD ["python3", "manage.py", "runserver", "0:8000"]