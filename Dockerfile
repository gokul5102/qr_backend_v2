FROM  python:3-alpine

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev



COPY requirements.txt requirements.txt

RUN apk add build-base linux-headers
RUN pip3 install psutil
RUN pip3 install -r requirements.txt


# COPY . .

# CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]